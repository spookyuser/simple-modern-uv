# Domain Search Web Application

A modern web application for finding available .com domain names using the ICANN zone file database. Based on the method described by [Derek Sivers](https://sive.rs/com).

![Domain Search](https://img.shields.io/badge/status-active-success)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green)

## Features

- 🔍 **Single Domain Search** - Check if a specific domain is available
- 📚 **Dictionary Word Search** - Find available dictionary words
- 🔤 **Word Combinations** - Search for combinations of two words
- 🎯 **Short Word Combos** - Find combinations of short (3-4 letter) words
- 🔢 **Letter-Number Patterns** - Discover available domains like q7r7.com
- ⚡ **Fast SQLite Database** - Indexed for quick lookups
- 🎨 **Modern UI** - Clean, responsive web interface

## How It Works

This application uses the ICANN Centralized Zone Data Service (CZDS) to get a complete list of registered .com domains, then allows you to search for available domains using various strategies.

The method:
1. Download the official .com zone file from ICANN (~4.6GB compressed)
2. Parse and extract unique domain names (~162 million domains)
3. Load into SQLite database with index for fast lookups
4. Search for available names using dictionary words, combinations, or patterns

## Prerequisites

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- ICANN CZDS access (free, but requires approval)

## Installation

### 1. Install uv (if not already installed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone and setup the project

```bash
git clone <your-repo-url>
cd simple-modern-uv
uv sync
```

## Getting the Domain Data

### Step 1: Apply for ICANN Zone File Access

1. Go to [ICANN CZDS](https://czds.icann.org/)
2. Create an account and apply for access to the .com zone file
3. Wait for approval (usually takes a few days)
4. More info: [Verisign Zone File Access](https://www.verisign.com/en_US/channel-resources/domain-registry-products/zone-file/index.xhtml)

### Step 2: Download the Zone File

Once approved:

1. Log in to [CZDS](https://czds.icann.org/)
2. Download **com.txt.gz** (approximately 4.6GB compressed)
3. Decompress it:

```bash
gunzip com.txt.gz
# Result: com.txt (~23GB uncompressed)
```

### Step 3: Parse the Zone File

Extract unique domain names from the zone file:

```bash
cd domain_search
uv run python scripts/parse_domains.py /path/to/com.txt domains.txt
```

This will create `domains.txt` with approximately 162 million unique domain names (~2.2GB).

**Note:** This step can take 30-60 minutes depending on your system.

### Step 4: Build the SQLite Database

Load the domains into a SQLite database with an index:

```bash
uv run python scripts/build_database.py domains.txt domains.db
```

This creates `domains.db` with an indexed table for fast lookups.

**Note:** This step can take 15-30 minutes. The resulting database will be several GB.

## Running the Application

### Start the web server

```bash
cd domain_search
uv run python main.py
```

Or using uvicorn directly:

```bash
uv run uvicorn domain_search.main:app --reload
```

The application will start at: **http://localhost:8000**

### Using the Web Interface

Open your browser and navigate to `http://localhost:8000`. You'll see several search options:

1. **Single Domain** - Enter any domain name to check availability
2. **Dictionary Words** - Find available dictionary words up to a specified length
3. **Word Combinations** - Check if a combination of two specific words is available
4. **Short Word Combinations** - Generate available combinations of short words
5. **Letter-Number Patterns** - Find 4-character domains with alternating letters and numbers

## API Endpoints

The application provides a REST API:

### Check Single Domain
```
GET /api/search/single?word=example
```

### Search Dictionary Words
```
GET /api/search/dictionary?max_length=8
```

### Check Word Combination
```
GET /api/search/combinations?word1=hello&word2=world
```

### Search Short Combinations
```
GET /api/search/short-combinations?max_word_length=4&limit=100
```

### Search Letter-Number Patterns
```
GET /api/search/letter-number?limit=100
```

### Health Check
```
GET /api/health
```

## Development

### Install development dependencies

```bash
uv sync --dev
```

### Format code

```bash
uv run ruff format .
```

### Lint code

```bash
uv run ruff check .
```

## Project Structure

```
domain_search/
├── main.py                 # FastAPI application
├── scripts/
│   ├── parse_domains.py   # Extract domains from zone file
│   └── build_database.py  # Build SQLite database
├── static/
│   ├── style.css          # Web interface styles
│   └── script.js          # Frontend JavaScript
├── templates/
│   └── index.html         # Main web page
└── domains.db             # SQLite database (created after setup)
```

## Performance Notes

- **Database size**: ~3-5 GB for 162 million domains
- **Lookup speed**: Typically < 10ms per query with index
- **Memory usage**: ~50-100 MB during operation
- **Initial setup time**: 1-2 hours total (download + processing)

## Important Notes

⚠️ **Limitations:**
- The zone file doesn't include domains on hold, pending deletion, or without name servers
- Some domains may appear available but are actually reserved or recently registered
- Always verify availability with an actual domain registrar before purchasing
- The zone file is updated daily, so data may be slightly stale

💡 **Recommendations:**
- Download fresh zone file data periodically (monthly or quarterly)
- Keep the database file backed up to avoid reprocessing
- Use a domain registrar like [Porkbun](https://porkbun.com/) to verify and purchase domains

## Credits

This method is based on Derek Sivers' article: [Find a good available .com domain](https://sive.rs/com)

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
