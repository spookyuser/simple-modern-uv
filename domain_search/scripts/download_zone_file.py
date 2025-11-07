#!/usr/bin/env python3
"""
Download .com zone file from ICANN CZDS using the czds Python library.

Usage:
    python download_zone_file.py

This script will:
1. Authenticate with CZDS
2. List all available zone files
3. Download the .com zone file
4. Save it to the data/ directory
"""

import os
from pathlib import Path

from czds import CZDS

# Configuration
USERNAME = os.environ.get("CZDS_USERNAME", "calebrud@gmail.com")
PASSWORD = os.environ.get("CZDS_PASSWORD", "qynzep-jugjo0-cygGek")
SAVE_DIR = Path(__file__).parent.parent / "data"

# Create save directory
SAVE_DIR.mkdir(exist_ok=True)

print("=" * 60)
print("CZDS Zone File Downloader")
print("=" * 60)
print(f"Username: {USERNAME}")
print(f"Save directory: {SAVE_DIR}")
print()

# Initialize CZDS client
print("Authenticating with CZDS...")
client = CZDS(username=USERNAME, password=PASSWORD, save_directory=str(SAVE_DIR))

# List available zone files
print("\nListing available zone files...")
try:
    links = client.list_links()
    print(f"Found {len(links)} available zone files:")

    # Find .com zone file
    com_link = None
    for link in links:
        if "com.txt" in link or link.endswith("/com"):
            print(f"  -> .com zone file: {link}")
            com_link = link
        else:
            print(f"     {link.split('/')[-1]}")

    if not com_link:
        print("\nWarning: .com zone file not found in available links!")
        print("You may need to request access to .com zone file in CZDS.")
        print("\nDownloading all available zone files instead...")
        result = client.get_zone()
        print(f"\nDownload complete! Files saved to: {SAVE_DIR}")
    else:
        # Download .com zone file
        print(f"\nDownloading .com zone file...")
        print("This may take several minutes (file is ~4-5 GB compressed)...")
        result = client.get_zone(link=com_link)
        print(f"\nDownload complete! File saved to: {SAVE_DIR}")

        # List downloaded files
        print("\nDownloaded files:")
        for file in SAVE_DIR.glob("*"):
            size_mb = file.stat().st_size / (1024 * 1024)
            print(f"  {file.name}: {size_mb:.1f} MB")

except Exception as e:
    print(f"\nError: {e}")
    print("\nTroubleshooting:")
    print("1. Verify your credentials are correct")
    print("2. Check that your CZDS account has been approved")
    print("3. Ensure you have requested access to the .com zone file")
    print("4. Visit https://czds.icann.org/ to manage your access")
    raise

print("\n" + "=" * 60)
print("Next steps:")
print("1. Gunzip the downloaded file if needed")
print("2. Run: python scripts/parse_domains.py data/com.txt domains.txt")
print("3. Run: python scripts/build_database.py domains.txt domains.db")
print("=" * 60)
