#!/usr/bin/env python3
import zipfile
import os
from pathlib import Path

def extract_all_zips(root_zip: Path, extract_to: Path = None, delete_zips: bool = True):
    """
    Extracts all files from nested ZIP archives in one operation.
    
    Args:
        root_zip: Path to the root ZIP file
        extract_to: Optional target directory (defaults to parent directory)
        delete_zips: Whether to delete ZIP files after extraction (default: True)
    """
    # Set default extraction directory if not specified
    if extract_to is None:
        extract_to = root_zip.parent / root_zip.stem
    
    # Create output directory if it doesn't exist
    extract_to.mkdir(exist_ok=True)
    
    # Process queue of ZIP files to extract
    zip_queue = [root_zip]
    processed_zips = set()
    
    while zip_queue:
        current_zip = zip_queue.pop(0)
        
        # Skip if already processed or doesn't exist
        if current_zip in processed_zips or not current_zip.exists():
            continue
            
        try:
            # Extract the current ZIP
            with zipfile.ZipFile(current_zip, 'r') as zip_ref:
                # Determine extraction path (root ZIP goes to extract_to, others to their parent)
                target_path = extract_to if current_zip == root_zip else current_zip.parent
                
                print(f"📦 Extracting {current_zip.name} to {target_path}")
                zip_ref.extractall(target_path)
                processed_zips.add(current_zip)
                
                # Add any extracted ZIPs to the queue
                for extracted in zip_ref.namelist():
                    extracted_path = target_path / extracted
                    if extracted_path.suffix.lower() == '.zip' and extracted_path.exists():
                        zip_queue.append(extracted_path)
                        
            # Delete the ZIP if requested (and it's not the original root ZIP)
            if delete_zips and current_zip != root_zip:
                current_zip.unlink()
                
        except zipfile.BadZipFile as e:
            print(f"⚠️  Skipping corrupt ZIP: {current_zip} - {e}")
            continue

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python extract_all.py <archive.zip> [output_directory] [--keep-zips]")
        print("Options:")
        print("  --keep-zips   Don't delete ZIP files after extraction")
        sys.exit(1)
    
    input_zip = Path(sys.argv[1])
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else None
    delete_zips = '--keep-zips' not in sys.argv
    
    if not input_zip.exists():
        print(f"❌ Error: File not found - {input_zip}")
        sys.exit(1)
    
    try:
        extract_all_zips(input_zip, output_dir, delete_zips)
        print(f"✅ Extraction complete! Files are in: {output_dir or input_zip.parent/input_zip.stem}")
    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
