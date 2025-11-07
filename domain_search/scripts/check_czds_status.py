#!/usr/bin/env python3
"""Check CZDS account status and available downloads."""

import requests

USERNAME = "calebrud@gmail.com"
PASSWORD = "qynzep-jugjo0-cygGek"

print("=" * 70)
print("CZDS Account Status Checker")
print("=" * 70)
print()

# Authenticate
auth_url = "https://account-api.icann.org/api/authenticate"
headers = {"Accept": "application/json", "Content-Type": "application/json"}
auth_response = requests.post(
    auth_url, json={"username": USERNAME, "password": PASSWORD}, headers=headers
)

if auth_response.status_code != 200:
    print(f"✗ Authentication failed: {auth_response.status_code}")
    print(auth_response.text)
    exit(1)

token = auth_response.json().get("accessToken")
print(f"✓ Authenticated successfully")
print()

# Set auth header
headers["Authorization"] = f"Bearer {token}"

# Check various endpoints
endpoints = {
    "Zone File Links": "https://czds-api.icann.org/czds/downloads/links",
    "User Info": "https://czds-api.icann.org/czds/user/info",
    "Requests": "https://czds-api.icann.org/czds/requests/all",
    "Zone Files": "https://czds-api.icann.org/czds/downloads",
}

for name, url in endpoints.items():
    print(f"Checking {name}...")
    print(f"  URL: {url}")

    try:
        response = requests.get(url, headers=headers)
        print(f"  Status: {response.status_code}")

        if response.status_code == 200:
            content = response.text
            if content:
                try:
                    data = response.json()
                    if isinstance(data, list):
                        print(f"  Result: List with {len(data)} items")
                        if data:
                            print(f"  Sample: {data[0] if len(str(data[0])) < 100 else str(data[0])[:100] + '...'}")
                    elif isinstance(data, dict):
                        print(f"  Result: Dict with keys: {list(data.keys())}")
                    else:
                        print(f"  Result: {type(data)}")
                except:
                    print(f"  Content: {content[:200]}")
            else:
                print(f"  Result: Empty response (no zone files approved yet)")
        elif response.status_code == 404:
            print(f"  Result: Endpoint not found")
        elif response.status_code == 403:
            print(f"  Result: Access forbidden")
        else:
            print(f"  Result: {response.text[:200] if response.text else 'No content'}")

    except Exception as e:
        print(f"  Error: {e}")

    print()

print("=" * 70)
print("Summary:")
print("=" * 70)
print()
print("If you see empty results above, it means:")
print("  1. Your account has been created successfully")
print("  2. BUT you haven't been granted access to any zone files yet")
print()
print("To request access:")
print("  1. Go to https://czds.icann.org/")
print("  2. Log in with your credentials")
print("  3. Navigate to 'Zone File Access' or 'Request Access'")
print("  4. Request access to the .com zone file")
print("  5. Wait for approval (can take a few days)")
print()
print("Once approved, you'll be able to download the zone files!")
print("=" * 70)
