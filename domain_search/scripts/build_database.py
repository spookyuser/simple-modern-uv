#!/usr/bin/env python3
"""
Build SQLite database from domains.txt.

This script loads the parsed domains from domains.txt into a SQLite database
with an index for fast lookups.

Usage:
    python build_database.py <domains_file> <database_file>

Example:
    python build_database.py domains.txt domains.db
"""

import sqlite3
import sys
from pathlib import Path


def build_database(domains_file: Path, db_file: Path) -> None:
    """
    Build SQLite database from domains file.

    Args:
        domains_file: Path to domains.txt
        db_file: Path to output domains.db
    """
    if not domains_file.exists():
        print(f"Error: {domains_file} not found")
        sys.exit(1)

    # Remove existing database
    if db_file.exists():
        print(f"Removing existing database: {db_file}")
        db_file.unlink()

    print(f"Creating database: {db_file}")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create table
    print("Creating domains table...")
    cursor.execute("CREATE TABLE domains (domain TEXT)")

    # Import domains
    print(f"Importing domains from {domains_file}...")
    count = 0
    with open(domains_file) as f:
        batch = []
        for line_num, line in enumerate(f, 1):
            domain = line.strip()
            if domain:
                batch.append((domain,))
                count += 1

            # Batch insert for better performance
            if len(batch) >= 10_000:
                cursor.executemany("INSERT INTO domains VALUES (?)", batch)
                batch = []
                if count % 1_000_000 == 0:
                    print(f"Imported {count:,} domains...")
                    conn.commit()

        # Insert remaining
        if batch:
            cursor.executemany("INSERT INTO domains VALUES (?)", batch)

    conn.commit()
    print(f"Imported {count:,} domains")

    # Create index
    print("Creating index (this may take a while)...")
    cursor.execute("CREATE INDEX idx_domain ON domains(domain)")
    conn.commit()

    print("Done! Database is ready to use.")

    # Show stats
    cursor.execute("SELECT COUNT(*) FROM domains")
    total = cursor.fetchone()[0]
    print(f"\nDatabase statistics:")
    print(f"  Total domains: {total:,}")
    print(f"  Database size: {db_file.stat().st_size / (1024**2):.1f} MB")

    conn.close()


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    domains_file = Path(sys.argv[1])
    db_file = Path(sys.argv[2])

    build_database(domains_file, db_file)


if __name__ == "__main__":
    main()
