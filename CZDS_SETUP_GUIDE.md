# CZDS Setup Guide

## Current Status

✓ Your CZDS account is created and authenticated successfully!
⚠️ You need to request access to zone files

## Step-by-Step Instructions

### Step 1: Log in to CZDS

1. Go to **https://czds.icann.org/**
2. Log in with your credentials:
   - Username: `calebrud@gmail.com`
   - Password: `qynzep-jugjo0-cygGek`

### Step 2: Request Access to Zone Files

Once logged in:

1. Look for **"Zone File Access"** or **"Request Access"** in the navigation menu
2. Find **.com** in the list of available TLDs
3. Click **"Request Access"** for .com
4. Fill out the request form:
   - **Reason for access**: Select an appropriate reason (research, academic, business analysis, etc.)
   - **Description**: Provide a brief description of your intended use
     - Example: "Domain name research and availability analysis for personal project"
5. Submit the request

### Step 3: Wait for Approval

- **Timeline**: Approval typically takes 1-3 business days, but can take up to a week
- **Email notification**: You'll receive an email when your request is approved
- **Status check**: You can check your request status by logging into CZDS

### Step 4: Download Zone File

Once approved, you have two options:

#### Option A: Use the automated script (recommended)

```bash
cd domain_search
uv run python scripts/download_zone_file.py
```

This will:
- Authenticate with CZDS
- Download the .com zone file
- Save it to `domain_search/data/`

#### Option B: Manual download

1. Log in to https://czds.icann.org/
2. Navigate to "Downloads" or "My Zone Files"
3. Download the .com zone file (com.txt.gz)
4. Save to `domain_search/data/`

### Step 5: Process the Data

Once you have the zone file:

```bash
# If the file is compressed
gunzip data/com.txt.gz

# Parse the zone file (extracts unique domains)
uv run python scripts/parse_domains.py data/com.txt data/domains.txt

# Build the database (creates SQLite database with index)
uv run python scripts/build_database.py data/domains.txt domains.db
```

**Note**: Processing can take 1-2 hours total depending on your system.

### Step 6: Run the Application

```bash
# From the domain_search directory
uv run python main.py

# Or from the project root
./run.sh
```

Then open http://localhost:8000 in your browser!

## Testing the Scripts Now

While waiting for approval, you can test the application with the sample database:

```bash
# Verify authentication works
uv run python scripts/check_czds_status.py

# Run the web application with sample data
uv run python main.py
```

## Troubleshooting

### "Empty response" when checking status

This is normal if you haven't requested access yet or if your request is pending.

### Request denied

If your request is denied:
- Check the reason in the email notification
- Provide more details about your use case
- Try submitting a new request with better justification

### Download fails after approval

- Check that you're using the correct credentials
- Verify your access hasn't expired (zone file access may need periodic renewal)
- Try the manual download option from the CZDS website

## Alternative: Use Sample Data

If you can't wait for CZDS approval or just want to test the application:

1. The application already includes a sample database with ~30 domains
2. You can also use the Tranco top 1M list (already downloaded):
   ```bash
   # The application will work with any list of registered domains
   # You just won't have the complete 162M .com domains
   ```

## Additional Resources

- **CZDS Portal**: https://czds.icann.org/
- **CZDS Help**: https://czds.icann.org/help
- **Verisign Zone File Info**: https://www.verisign.com/en_US/channel-resources/domain-registry-products/zone-file/index.xhtml
- **Original Method**: https://sive.rs/com

## Questions?

If you have any issues:
1. Run the diagnostic script: `uv run python scripts/check_czds_status.py`
2. Check your CZDS account at https://czds.icann.org/
3. Review the error messages carefully - they usually indicate the exact issue
