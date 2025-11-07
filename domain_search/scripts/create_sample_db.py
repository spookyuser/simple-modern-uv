#!/usr/bin/env python3
"""
Create a sample database for testing the application.

This creates a small database with some popular domains so you can test
the application without downloading the full ICANN zone file.

Usage:
    python create_sample_db.py
"""

import sqlite3
from pathlib import Path

# Common words and domains to include in the sample
SAMPLE_DOMAINS = [
    # Common dictionary words
    "cat",
    "dog",
    "house",
    "car",
    "tree",
    "book",
    "hello",
    "world",
    "python",
    "code",
    # Popular tech companies
    "google",
    "facebook",
    "amazon",
    "apple",
    "microsoft",
    "twitter",
    "github",
    "stackoverflow",
    # Common name patterns
    "test",
    "demo",
    "example",
    "sample",
    "mysite",
    "website",
    # Some combinations
    "helloworld",
    "codebase",
    "webapp",
    "homepage",
    # Letter-number patterns (some taken, some available)
    "a1b2",
    "x9y9",
    "m5n5",
]


def create_sample_db():
    """Create a sample database for testing."""
    db_path = Path(__file__).parent.parent / "domains.db"

    print("Creating sample database for testing...")

    # Remove existing database
    if db_path.exists():
        print(f"Removing existing database: {db_path}")
        db_path.unlink()

    # Create new database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create table
    cursor.execute("CREATE TABLE domains (domain TEXT)")

    # Insert sample domains
    for domain in SAMPLE_DOMAINS:
        cursor.execute("INSERT INTO domains VALUES (?)", (domain,))

    conn.commit()

    # Create index
    print("Creating index...")
    cursor.execute("CREATE INDEX idx_domain ON domains(domain)")
    conn.commit()

    # Show stats
    cursor.execute("SELECT COUNT(*) FROM domains")
    total = cursor.fetchone()[0]

    print(f"\nSample database created successfully!")
    print(f"  Location: {db_path}")
    print(f"  Total domains: {total:,}")
    print(f"  Database size: {db_path.stat().st_size / 1024:.1f} KB")
    print("\nThis is a SAMPLE database for testing only.")
    print("For production use, follow the instructions in DOMAIN_SEARCH_README.md")
    print("to download and process the full ICANN zone file.")

    conn.close()


if __name__ == "__main__":
    create_sample_db()
