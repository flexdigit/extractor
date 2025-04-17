#!/usr/bin/env python3
import zipfile
import os
from pathlib import Path

def extract_zip(zip_path: Path, extract_to: Path):
    """Extract a ZIP file while preserving its structure"""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Extract all files, preserving paths
        zip_ref.extractall(extract_to)

def process_directory(directory: Path):
    """Process all ZIP files in directory and subdirectories"""
    # First gather all ZIP files to process
    zip_files = list(directory.glob('**/*.zip'))
    
    for zip_file in zip_files:
        # Skip if file was already processed/deleted
        if not zip_file.exists():
            continue
            
        # Create target path (same location as ZIP)
        target_path = zip_file.parent
        
        # Extract contents (preserving internal structure)
        extract_zip(zip_file, target_path)
        
        # Delete the ZIP file after successful extraction
        zip_file.unlink()
        
        # Process any new ZIPs that were extracted
        process_directory(target_path)

def main(input_zip: Path):
    """Main extraction function"""
    # Create output directory (same name as ZIP without extension)
    output_dir = input_zip.parent / input_zip.stem
    output_dir.mkdir(exist_ok=True)
    
    # Extract main ZIP first
    extract_zip(input_zip, output_dir)
    
    # Process all nested ZIPs
    process_directory(output_dir)
    
    print(f"✅ Extraction complete! All files are in: {output_dir}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python extract_all.py <archiveAll.zip>")
        sys.exit(1)
    
    input_zip = Path(sys.argv[1])
    
    if not input_zip.exists():
        print(f"❌ Error: File not found - {input_zip}")
        sys.exit(1)
    
    try:
        main(input_zip)
    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        sys.exit(1)

        
