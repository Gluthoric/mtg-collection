import csv
import os
from pathlib import Path

def load_csv(file_path):
    """Load CSV file and return the number of rows."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return len(list(csv.DictReader(f)))

def compare_records(original_file, scryfall_file):
    """Compare row counts between original and scryfall versions."""
    original_count = load_csv(original_file)
    scryfall_count = load_csv(scryfall_file)
    
    if original_count != scryfall_count:
        return f"Row count mismatch: Original={original_count}, Scryfall={scryfall_count}"
    return None

def find_csv_pairs(base_dir):
    """Find pairs of original and _with_scryfall CSVs."""
    pairs = []
    for root, _, files in os.walk(base_dir):
        csv_files = [f for f in files if f.endswith('.csv')]
        for file in csv_files:
            if not file.endswith('_with_scryfall.csv'):
                scryfall_file = file.replace('.csv', '_with_scryfall.csv')
                if scryfall_file in csv_files:
                    pairs.append((
                        os.path.join(root, file),
                        os.path.join(root, scryfall_file)
                    ))
    return pairs

def verify_all_sets():
    """Verify all sets in the organized_sets directory."""
    base_dir = "organized_sets"
    pairs = find_csv_pairs(base_dir)
    
    print(f"Found {len(pairs)} CSV pairs to verify")
    print("\nStarting verification...")
    
    issues = {}
    total_records = 0
    
    for original_file, scryfall_file in pairs:
        set_name = Path(original_file).stem
        print(f"\nVerifying {set_name}...")
        
        try:
            row_count = load_csv(original_file)
            total_records += row_count
            
            issue = compare_records(original_file, scryfall_file)
            if issue:
                issues[set_name] = issue
                print("❌ " + issue)
            else:
                print("✓ Matching row counts")
                
        except Exception as e:
            print(f"Error processing {set_name}: {str(e)}")
            issues[set_name] = f"Error: {str(e)}"
    
    # Print summary
    print("\n" + "="*50)
    print("VERIFICATION SUMMARY")
    print("="*50)
    print(f"Total sets verified: {len(pairs)}")
    print(f"Total records processed: {total_records}")
    print(f"Sets with mismatches: {len(issues)}")
    
    # Print detailed issues
    if issues:
        print("\nDETAILED MISMATCHES")
        print("="*50)
        for set_name, issue in issues.items():
            print(f"\n{set_name}:")
            print(f"  - {issue}")
    else:
        print("\nAll sets have matching row counts! 🎉")

if __name__ == "__main__":
    print("Starting verification of Scryfall data...")
    verify_all_sets()
    print("\nVerification complete!")
