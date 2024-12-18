import csv
import requests
import time
from urllib.parse import quote
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Thread-safe print lock and rate limit semaphore
print_lock = threading.Lock()
rate_limit_semaphore = threading.Semaphore(5)

def safe_print(*args, **kwargs):
    with print_lock:
        print(*args, **kwargs)

def clean_set_name(set_name):
    """Clean set name for matching with Scryfall data."""
    return set_name.replace("_", " ").strip()

def get_scryfall_data(name: str, set_name: str, collector_number: str = None) -> dict:
    """Query Scryfall API to get card data."""
    with rate_limit_semaphore:
        try:
            # Rate limiting - Scryfall asks for 50-100ms between requests
            time.sleep(0.1)
            
            # Encode the card name for the URL
            encoded_name = quote(f'!"{name}"')
            url = f"https://api.scryfall.com/cards/search?q={encoded_name}"
            response = requests.get(url)
            
            # Handle rate limiting
            if response.status_code == 429:  # Too Many Requests
                time.sleep(1)
                return get_scryfall_data(name, set_name, collector_number)
                
            if response.status_code == 200:
                data = response.json()
                if data["total_cards"] > 0:
                    # Clean the set name for comparison
                    clean_name = clean_set_name(set_name)
                    
                    # Try to find exact match in the returned cards
                    for card in data["data"]:
                        # Compare set names
                        if clean_name.lower() in card["set_name"].lower():
                            # If we have a collector number, verify it matches
                            if collector_number and str(card["collector_number"]) != str(collector_number):
                                continue
                            
                            return {
                                "id": card["id"],
                                "collector_number": card["collector_number"],
                                "set": card["set"],
                                "rarity": card["rarity"]
                            }
                    
                    # If no exact set match found, use the first result
                    card_data = data["data"][0]
                    return {
                        "id": card_data["id"],
                        "collector_number": card_data["collector_number"],
                        "set": card_data["set"],
                        "rarity": card_data["rarity"]
                    }
                    
            return None
        except Exception as e:
            if "rate limit" in str(e).lower():
                time.sleep(1)
                return get_scryfall_data(name, set_name, collector_number)
            safe_print(f"Error getting data for {name}: {str(e)}")
            return None

def process_set_file(input_file):
    safe_print(f"\nProcessing {input_file}...")
    
    set_name = Path(input_file).stem
    safe_print(f"Processing set: {set_name}")
    
    output_file = str(input_file).replace(".csv", "_with_scryfall.csv")
    
    try:
        with open(input_file, "r", encoding="utf-8") as infile:
            reader = csv.DictReader(infile)
            
            if "Name" not in reader.fieldnames:
                safe_print(f"Skipping {input_file} - not a card file")
                return
                
            headers = reader.fieldnames + ["scryfall_id", "collector_number", "scryfall_set", "scryfall_rarity"]
            
            rows = []
            total_cards = 0
            matched_cards = 0
            
            for row in reader:
                total_cards += 1
                # Try to get collector number from the row
                collector_number = row.get("Number", "")
                card_data = get_scryfall_data(row["Name"], set_name, collector_number)
                
                if card_data:
                    matched_cards += 1
                    row["scryfall_id"] = card_data["id"]
                    row["collector_number"] = card_data["collector_number"]
                    row["scryfall_set"] = card_data["set"]
                    row["scryfall_rarity"] = card_data["rarity"]
                else:
                    row["scryfall_id"] = ""
                    row["collector_number"] = ""
                    row["scryfall_set"] = ""
                    row["scryfall_rarity"] = ""
                
                rows.append(row)
                
                if total_cards % 10 == 0:
                    safe_print(f"{set_name}: Processed {total_cards} cards. Successfully matched: {matched_cards}")
            
            with open(output_file, "w", encoding="utf-8", newline="") as outfile:
                writer = csv.DictWriter(outfile, fieldnames=headers)
                writer.writeheader()
                writer.writerows(rows)
            
            safe_print(f"\nResults for {set_name}:")
            safe_print(f"Total cards processed: {total_cards}")
            safe_print(f"Successfully matched: {matched_cards}")
            safe_print(f"Failed to match: {total_cards - matched_cards}")
            safe_print(f"Success rate: {(matched_cards/total_cards)*100:.2f}%")
            safe_print(f"Output saved to: {output_file}")
            
            return {
                "set_name": set_name,
                "total": total_cards,
                "matched": matched_cards
            }
            
    except Exception as e:
        safe_print(f"Error processing {input_file}: {str(e)}")
        return None

def process_all_sets():
    base_dir = "organized_sets"
    skip_files = ["sets_summary.csv", "type_summary.csv"]
    set_files = []
    
    # Only process standard and supplemental folders
    target_folders = ["standard", "supplemental"]
    
    # Collect all set files from target folders
    for root, dirs, files in os.walk(base_dir):
        folder_name = os.path.basename(root)
        if folder_name in target_folders:
            for file in files:
                if file.endswith(".csv") and not file.endswith("_with_scryfall.csv") and file not in skip_files:
                    # Only process files that come after "Portal" alphabetically
                    if file >= "Portal.csv":
                        set_files.append(os.path.join(root, file))
    
    # Sort files to ensure we process them in order
    set_files.sort()
    
    results = []
    # Process sets in parallel using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=3) as executor:  # Using 3 workers for better rate limiting
        future_to_file = {executor.submit(process_set_file, file): file for file in set_files}
        for future in as_completed(future_to_file):
            file = future_to_file[future]
            try:
                result = future.result()
                if result:
                    results.append(result)
            except Exception as e:
                safe_print(f"Error processing {file}: {str(e)}")
    
    # Print final summary
    safe_print("\nFinal Summary:")
    if results:
        total_cards = sum(r["total"] for r in results)
        total_matched = sum(r["matched"] for r in results)
        safe_print(f"Total sets processed: {len(results)}")
        safe_print(f"Total cards processed: {total_cards}")
        safe_print(f"Total cards matched: {total_matched}")
        safe_print(f"Overall success rate: {(total_matched/total_cards)*100:.2f}%")
    else:
        safe_print("No sets were processed")

if __name__ == "__main__":
    print("Starting to add Scryfall IDs to standard and supplemental sets from Portal onwards...")
    process_all_sets()
    print("\nProcess complete!")
