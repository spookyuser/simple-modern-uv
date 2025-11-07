#!/usr/bin/env python3
"""
Parse com.txt zone file and extract unique domain names.

This script processes the ICANN zone file (com.txt) and extracts unique
domain names, outputting them to domains.txt.

Usage:
    python parse_domains.py <input_file> <output_file>

Example:
    python parse_domains.py com.txt domains.txt
"""

import sys
from pathlib import Path


def parse_domains(input_file: Path, output_file: Path) -> None:
    """
    Parse the com.txt zone file and extract unique domains.

    Args:
        input_file: Path to com.txt
        output_file: Path to output domains.txt
    """
    if not input_file.exists():
        print(f"Error: {input_file} not found")
        sys.exit(1)

    print(f"Processing {input_file}...")
    print(f"This may take a while for large files...")

    domain = ""
    count = 0

    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for line_num, line in enumerate(infile, 1):
            if line_num % 1_000_000 == 0:
                print(f"Processed {line_num:,} lines, found {count:,} unique domains")

            # Find .com in the line
            idx = line.find(".com")
            if idx == -1:
                continue

            # Extract domain name before .com
            temp = line[:idx]

            # Skip if same as previous domain
            if temp == domain:
                continue

            domain = temp
            outfile.write(domain + "\n")
            count += 1

    print(f"\nDone! Extracted {count:,} unique domains to {output_file}")


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])

    parse_domains(input_file, output_file)


if __name__ == "__main__":
    main()
