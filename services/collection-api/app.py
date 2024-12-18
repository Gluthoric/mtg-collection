from flask import Flask, render_template, jsonify, request, make_response
import sqlite3
import json
import csv
import os
from datetime import datetime
from functools import wraps
from threading import Lock
from cachetools import TTLCache

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE = os.path.join(BASE_DIR, 'collection.db')

# Add connection pooling
DB_POOL = {}
DB_POOL_LOCK = Lock()
STATS_CACHE = TTLCache(maxsize=1, ttl=5)  # Cache stats for 5 seconds

def enable_cors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(f"Handling request to: {request.path}")
        print(f"Request headers: {dict(request.headers)}")
        
        response = make_response(f(*args, **kwargs))
        
        # Log response headers for debugging
        print(f"Setting response headers for {request.path}:")
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
        print(f"- Added Access-Control-Allow-Origin: {response.headers['Access-Control-Allow-Origin']}")
        
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,Accept,Origin')
        print(f"- Added Access-Control-Allow-Headers: {response.headers['Access-Control-Allow-Headers']}")
        
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        print(f"- Added Access-Control-Allow-Methods: {response.headers['Access-Control-Allow-Methods']}")
        
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        print(f"- Added Access-Control-Allow-Credentials: {response.headers['Access-Control-Allow-Credentials']}")
        
        response.headers.add('Access-Control-Max-Age', '3600')
        print(f"- Added Access-Control-Max-Age: {response.headers['Access-Control-Max-Age']}")
        
        response.headers.add('Vary', 'Origin')
        print(f"- Added Vary: {response.headers['Vary']}")
        
        print(f"Final response headers: {dict(response.headers)}")
        return response
    return decorated_function

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,Accept,Origin')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Max-Age', '3600')
        response.headers.add('Vary', 'Origin')
        return response
SCHEMA_VERSION = 2  # Increment this when schema changes
SCRYFALL_DATA = '../default-cards.json'  # Updated to use parent directory

def get_db_version(conn):
    """Get current database version"""
    try:
        return conn.execute('SELECT version FROM schema_version').fetchone()[0]
    except sqlite3.OperationalError:
        return 0

def needs_import(conn):
    """Check if database needs card import"""
    try:
        count = conn.execute('SELECT COUNT(*) FROM cards').fetchone()[0]
        return count == 0
    except sqlite3.OperationalError:
        return True

def init_db():
    """Initialize or upgrade database"""
    with sqlite3.connect(DATABASE) as conn:
        current_version = get_db_version(conn)
        needs_card_import = needs_import(conn)
        
        if current_version == 0:
            # Fresh install
            print("Creating new database...")
            conn.execute('CREATE TABLE schema_version (version INTEGER)')
            conn.execute('INSERT INTO schema_version VALUES (?)', [SCHEMA_VERSION])
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS cards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    scryfall_id TEXT UNIQUE,
                    name TEXT NOT NULL,
                    set_name TEXT NOT NULL,
                    collector_number TEXT,
                    rarity TEXT,
                    quantity INTEGER DEFAULT 0,
                    foil_quantity INTEGER DEFAULT 0,
                    price REAL,
                    foil_price REAL,
                    image_normal TEXT,
                    image_art_crop TEXT,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create indices
            conn.execute('CREATE INDEX IF NOT EXISTS idx_scryfall_id ON cards(scryfall_id)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_name ON cards(name)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_set ON cards(set_name)')
            
            return True  # Needs import
            
        elif current_version < SCHEMA_VERSION:
            # Upgrade existing database
            print(f"Upgrading database from version {current_version} to {SCHEMA_VERSION}...")
            if current_version == 1:
                # Example upgrade from version 1 to 2
                # Backup existing data
                conn.execute('CREATE TABLE cards_backup AS SELECT * FROM cards')
                
                # Drop existing table
                conn.execute('DROP TABLE cards')
                
                # Create new schema
                conn.execute('''
                    CREATE TABLE cards (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        scryfall_id TEXT UNIQUE,
                        name TEXT NOT NULL,
                        set_name TEXT NOT NULL,
                        collector_number TEXT,
                        rarity TEXT,
                        quantity INTEGER DEFAULT 0,
                        foil_quantity INTEGER DEFAULT 0,
                        price REAL,
                        foil_price REAL,
                        image_normal TEXT,
                        image_art_crop TEXT,
                        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Restore data
                conn.execute('''
                    INSERT INTO cards (
                        scryfall_id, name, set_name, collector_number,
                        rarity, quantity, foil_quantity, price, foil_price,
                        last_updated
                    )
                    SELECT 
                        scryfall_id, name, set_name, collector_number,
                        rarity, quantity, foil_quantity, price, foil_price,
                        last_updated
                    FROM cards_backup
                ''')
                
                # Drop backup
                conn.execute('DROP TABLE cards_backup')
                
                # Recreate indices
                conn.execute('CREATE INDEX IF NOT EXISTS idx_scryfall_id ON cards(scryfall_id)')
                conn.execute('CREATE INDEX IF NOT EXISTS idx_name ON cards(name)')
                conn.execute('CREATE INDEX IF NOT EXISTS idx_set ON cards(set_name)')
            
            # Update schema version
            conn.execute('UPDATE schema_version SET version = ?', [SCHEMA_VERSION])
            
            return needs_import(conn)  # Check if we need to import after upgrade
        
        return needs_card_import  # Return initial import check result

def get_db():
    """Get database connection from pool or create new one"""
    try:
        with DB_POOL_LOCK:
            if 'conn' not in DB_POOL:
                print(f"Creating new database connection at: {DATABASE}")
                if not os.path.exists(DATABASE):
                    print(f"Database file not found at: {DATABASE}")
                    raise FileNotFoundError(f"Database file not found at: {DATABASE}")
                
                conn = sqlite3.connect(DATABASE, check_same_thread=False)
                conn.row_factory = sqlite3.Row
                DB_POOL['conn'] = conn
            return DB_POOL['conn']
    except sqlite3.Error as e:
        print(f"Database connection error: {str(e)}")
        raise

@app.route('/')
def index():
    """Render main page with sets"""
    return render_template('index.html')

@app.route('/set/<set_name>')
def set_view(set_name):
    """Render set-specific page"""
    return render_template('set.html')

@app.route('/api/stats')
@enable_cors
def get_stats():
    """Get overall collection statistics with caching"""
    try:
        # Check cache first
        if 'stats' in STATS_CACHE:
            return jsonify(STATS_CACHE['stats'])

        print("Cache miss - fetching fresh stats")
        db = get_db()
        stats = {
            'total_cards': db.execute(
                    'SELECT SUM(quantity + foil_quantity) FROM cards'
                ).fetchone()[0] or 0,
            'unique_cards': db.execute(
                'SELECT COUNT(*) FROM cards WHERE quantity > 0 OR foil_quantity > 0'
            ).fetchone()[0] or 0,
            'total_possible': db.execute(
                'SELECT COUNT(*) FROM cards'
            ).fetchone()[0] or 0,
            'total_value': db.execute('''
                SELECT SUM(
                    quantity * COALESCE(price, 0) + 
                    foil_quantity * COALESCE(foil_price, 0)
                ) FROM cards
            ''').fetchone()[0] or 0,
            'by_rarity': {}
        }
        
        # Get rarity breakdown
        rarities = db.execute('''
            SELECT rarity, 
                   COUNT(*) as total_cards,
                   SUM(CASE WHEN quantity > 0 OR foil_quantity > 0 THEN 1 ELSE 0 END) as owned_cards,
                   SUM(quantity + foil_quantity) as total_copies
            FROM cards 
            GROUP BY rarity
        ''')
        for row in rarities:
            if row['rarity']:
                stats['by_rarity'][row['rarity']] = {
                    'total': row['total_cards'],
                    'owned': row['owned_cards'],
                    'copies': row['total_copies']
                }
        
        # Cache the results
        STATS_CACHE['stats'] = stats
        return jsonify(stats)
    except Exception as e:
        print(f"Error getting stats: {str(e)}")
        return jsonify({'error': 'Failed to get collection stats'}), 500

@app.route('/api/set/<set_name>/stats')
def get_set_stats(set_name):
    """Get set-specific statistics"""
    with get_db() as db:
        stats = {
            'total_cards': db.execute(
                'SELECT SUM(quantity + foil_quantity) FROM cards WHERE set_name = ?',
                [set_name]
            ).fetchone()[0] or 0,
            'unique_cards': db.execute(
                'SELECT COUNT(*) FROM cards WHERE set_name = ? AND (quantity > 0 OR foil_quantity > 0)',
                [set_name]
            ).fetchone()[0] or 0,
            'total_possible': db.execute(
                'SELECT COUNT(*) FROM cards WHERE set_name = ?',
                [set_name]
            ).fetchone()[0] or 0,
            'total_value': db.execute('''
                SELECT SUM(
                    quantity * COALESCE(price, 0) + 
                    foil_quantity * COALESCE(foil_price, 0)
                ) FROM cards 
                WHERE set_name = ?
            ''', [set_name]).fetchone()[0] or 0,
            'by_rarity': {}
        }
        
        # Get rarity breakdown for set
        rarities = db.execute('''
            SELECT rarity, 
                   COUNT(*) as total_cards,
                   SUM(CASE WHEN quantity > 0 OR foil_quantity > 0 THEN 1 ELSE 0 END) as owned_cards,
                   SUM(quantity + foil_quantity) as total_copies
            FROM cards 
            WHERE set_name = ?
            GROUP BY rarity
        ''', [set_name])
        for row in rarities:
            if row['rarity']:
                stats['by_rarity'][row['rarity']] = {
                    'total': row['total_cards'],
                    'owned': row['owned_cards'],
                    'copies': row['total_copies']
                }
        
        return jsonify(stats)

@app.route('/api/sets')
def get_sets():
    """Get list of sets in collection"""
    sort = request.args.get('sort', 'name')  # name, completion, value
    order = request.args.get('order', 'asc')  # asc, desc
    
    order_sql = 'ASC' if order == 'asc' else 'DESC'
    
    sort_clauses = {
        'name': 'set_name',
        'completion': 'CAST(owned_cards AS FLOAT) / CAST(total_possible AS FLOAT)',
        'value': 'total_value',
        'cards': 'total_copies'
    }
    
    sort_sql = sort_clauses.get(sort, 'set_name')
    
    with get_db() as db:
        sets = db.execute(f'''
            SELECT 
                set_name,
                COUNT(*) as total_possible,
                SUM(CASE WHEN quantity > 0 OR foil_quantity > 0 THEN 1 ELSE 0 END) as owned_cards,
                SUM(quantity + foil_quantity) as total_copies,
                SUM(
                    quantity * COALESCE(price, 0) + 
                    foil_quantity * COALESCE(foil_price, 0)
                ) as total_value
            FROM cards 
            GROUP BY set_name
            ORDER BY {sort_sql} {order_sql}
        ''').fetchall()
        return jsonify([dict(s) for s in sets])

@app.route('/api/set/<set_name>/cards')
def get_set_cards(set_name):
    """Get cards for a specific set with filtering"""
    search = request.args.get('search', '')
    rarity = request.args.get('rarity', '')
    owned = request.args.get('owned', 'all')
    
    query = 'SELECT * FROM cards WHERE set_name = ?'
    params = [set_name]
    
    if search:
        query += ' AND name LIKE ?'
        params.append(f'%{search}%')
    if rarity:
        query += ' AND rarity = ?'
        params.append(rarity)
    if owned == 'owned':
        query += ' AND (quantity > 0 OR foil_quantity > 0)'
    elif owned == 'missing':
        query += ' AND quantity = 0 AND foil_quantity = 0'
    
    query += ' ORDER BY CAST(collector_number AS INTEGER)'
    
    with get_db() as db:
        cards = db.execute(query, params).fetchall()
        return jsonify([dict(card) for card in cards])

@app.route('/api/card/<scryfall_id>', methods=['PUT'])
def update_card(scryfall_id):
    """Update card quantities"""
    data = request.json
    with get_db() as db:
        db.execute('''
            UPDATE cards 
            SET quantity = ?,
                foil_quantity = ?,
                last_updated = CURRENT_TIMESTAMP
            WHERE scryfall_id = ?
        ''', [
            data.get('quantity', 0),
            data.get('foil_quantity', 0),
            scryfall_id
        ])
        db.commit()
        return jsonify({'status': 'success'})

def import_collection():
    """Import collection data"""
    print("Loading Scryfall data...")
    with open(SCRYFALL_DATA, 'r', encoding='utf-8') as f:
        scryfall_cards = {card['id']: card for card in json.load(f)}
    
    print("Processing collection...")
    with get_db() as db:
        # First, add all cards from Scryfall with 0 quantities
        for card_id, card_data in scryfall_cards.items():
            if 'games' in card_data and 'paper' in card_data['games']:
                image_uris = card_data.get('image_uris', {})
                if not image_uris and 'card_faces' in card_data:
                    image_uris = card_data['card_faces'][0].get('image_uris', {})
                
                db.execute('''
                    INSERT OR IGNORE INTO cards (
                        scryfall_id, name, set_name, collector_number,
                        rarity, quantity, foil_quantity, price, foil_price,
                        image_normal, image_art_crop
                    ) VALUES (?, ?, ?, ?, ?, 0, 0, ?, ?, ?, ?)
                ''', [
                    card_id,
                    card_data['name'],
                    card_data.get('set_name', ''),
                    card_data.get('collector_number', ''),
                    card_data.get('rarity', ''),
                    float(card_data.get('prices', {}).get('usd', 0) or 0),
                    float(card_data.get('prices', {}).get('usd_foil', 0) or 0),
                    image_uris.get('normal', ''),
                    image_uris.get('art_crop', '')
                ])
        
        # Then update quantities from collection CSVs
        for root, _, files in os.walk('../organized_sets'):  # Updated to use parent directory
            for file in files:
                if file.endswith('_with_scryfall.csv'):
                    filepath = os.path.join(root, file)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            scryfall_id = row['scryfall_id']
                            if not scryfall_id or scryfall_id not in scryfall_cards:
                                continue
                            
                            db.execute('''
                                UPDATE cards 
                                SET quantity = ?,
                                    foil_quantity = ?
                                WHERE scryfall_id = ?
                            ''', [
                                int(row['Qty']) if row['Foil'].upper() != 'TRUE' else 0,
                                int(row['Qty']) if row['Foil'].upper() == 'TRUE' else 0,
                                scryfall_id
                            ])
        db.commit()

if __name__ == '__main__':
    print("Initializing database...")
    needs_card_import = init_db()  # This will create or upgrade the database as needed
    if needs_card_import:
        print("Database empty, importing cards...")
        import_collection()
        print("Import complete!")
    else:
        print("Database ready!")
    app.run(debug=True)
