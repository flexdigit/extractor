#!/usr/bin/env python3
import zipfile
import shutil
from pathlib import Path

def extract_zip(zip_path: Path, extract_to: Path):
    """Extract a ZIP file to specified directory"""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Extract preserving all paths
        for member in zip_ref.namelist():
            try:
                zip_ref.extract(member, extract_to)
            except zipfile.BadZipFile:
                print(f"Warning: Could not extract {member} from {zip_path}")
                continue

def process_nested_zips(directory: Path):
    """Process all ZIP files in directory"""
    # Find all ZIP files
    for zip_file in directory.glob('*.zip'):
        # Create target folder (same name without .zip)
        target_folder = directory / zip_file.stem
        target_folder.mkdir(exist_ok=True)
        
        # Extract ZIP contents directly to target folder
        extract_zip(zip_file, target_folder)
        
        # Remove the ZIP file
        zip_file.unlink()
        
        # Process any new ZIPs in the target folder
        process_nested_zips(target_folder)

def main(main_zip_path: Path, output_dir: Path):
    """Main function to handle extraction"""
    # Create output directory if needed
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Extract main ZIP
    extract_zip(main_zip_path, output_dir)
    
    # Process all nested ZIPs
    process_nested_zips(output_dir)
    
    print(f"Successfully extracted to: {output_dir}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python extract_zips.py <input.zip> [output_dir]")
        sys.exit(1)
    
    input_zip = Path(sys.argv[1])
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.cwd() / input_zip.stem
    
    if not input_zip.exists():
        print(f"Error: Input file not found - {input_zip}")
        sys.exit(1)
    
    main(input_zip, output_dir)

