import os
from pathlib import Path

def cleanup_csvs(base_dir):
    """Remove original CSV files except those in supplemental folder, keeping only the _with_scryfall versions."""
    removed_count = 0
    supplemental_path = os.path.join(base_dir, "supplemental")
    
    print("Starting CSV cleanup...")
    for root, _, files in os.walk(base_dir):
        # Skip the supplemental folder and its subfolders
        if root.startswith(supplemental_path):
            continue
            
        csv_files = [f for f in files if f.endswith('.csv')]
        for file in csv_files:
            if not file.endswith('_with_scryfall.csv'):
                file_path = os.path.join(root, file)
                scryfall_file = file.replace('.csv', '_with_scryfall.csv')
                scryfall_path = os.path.join(root, scryfall_file)
                
                # Only remove if the _with_scryfall version exists
                if scryfall_file in csv_files:
                    print(f"Removing: {file}")
                    os.remove(file_path)
                    removed_count += 1
    
    print(f"\nCleanup complete! Removed {removed_count} original CSV files.")
    print("Preserved all files in supplemental folder.")

if __name__ == "__main__":
    cleanup_csvs("organized_sets")
