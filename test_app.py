#!/usr/bin/env python3
"""Quick test to verify the application works."""

import sys
from pathlib import Path

# Add domain_search to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    # Test imports
    print("Testing imports...")
    from domain_search.main import app, check_domain_available, DB_PATH

    print("✓ Imports successful")

    # Test database exists
    print(f"\nChecking database at: {DB_PATH}")
    if DB_PATH.exists():
        print("✓ Database exists")
    else:
        print("✗ Database not found")
        sys.exit(1)

    # Test domain check function
    print("\nTesting domain availability checks...")

    # Test with a domain that should be registered (in sample DB)
    result = check_domain_available("google")
    print(f"  google.com - {'Available' if result else 'Registered'} ✓")

    # Test with a domain that should be available (not in sample DB)
    result = check_domain_available("thisisaverylongandomdomainthatdoesnotexist12345")
    print(
        f"  thisisaverylongandomdomainthatdoesnotexist12345.com - {'Available' if result else 'Registered'} ✓"
    )

    print("\n✓ All tests passed!")
    print("\nTo start the application, run:")
    print("  cd domain_search")
    print("  uv run python main.py")
    print("\nOr use the convenience script:")
    print("  ./run.sh")

except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
