#!/usr/bin/env python3
"""Test CZDS authentication and API access."""

import requests

USERNAME = "calebrud@gmail.com"
PASSWORD = "qynzep-jugjo0-cygGek"

print("Testing CZDS Authentication...")
print(f"Username: {USERNAME}")
print()

# Step 1: Authenticate
print("Step 1: Authenticating...")
auth_url = "https://account-api.icann.org/api/authenticate"
headers = {"Accept": "application/json", "Content-Type": "application/json"}

auth_response = requests.post(
    auth_url, json={"username": USERNAME, "password": PASSWORD}, headers=headers
)

print(f"Auth Status Code: {auth_response.status_code}")
print(f"Auth Response Headers: {dict(auth_response.headers)}")
print(f"Auth Response Text: {auth_response.text[:500]}")
print()

if auth_response.status_code == 200:
    try:
        token = auth_response.json().get("accessToken")
        print(f"✓ Authentication successful!")
        print(f"  Token: {token[:50]}..." if token else "  No token in response")
        print()

        # Step 2: Try to list zone links
        print("Step 2: Listing available zone files...")
        links_url = "https://czds-api.icann.org/czds/downloads/links"
        headers["Authorization"] = f"Bearer {token}"

        links_response = requests.get(links_url, headers=headers)
        print(f"Links Status Code: {links_response.status_code}")
        print(f"Links Response Text: {links_response.text[:1000]}")
        print()

        if links_response.status_code == 200:
            try:
                links = links_response.json()
                print(f"✓ Found {len(links)} available zone files:")
                for link in links:
                    print(f"  - {link}")
            except Exception as e:
                print(f"✗ Error parsing links JSON: {e}")
        else:
            print(f"✗ Failed to get links")
            print("Possible reasons:")
            print("  - Account not approved yet")
            print("  - No zone file access granted")
            print("  - Need to request access to specific zones")

    except Exception as e:
        print(f"✗ Error: {e}")

elif auth_response.status_code == 401:
    print("✗ Authentication failed - Invalid credentials")
    print("Please check your username and password")

elif auth_response.status_code == 403:
    print("✗ Access forbidden - Account may not be approved yet")
    print("Please check your CZDS account status at https://czds.icann.org/")

else:
    print(f"✗ Unexpected status code: {auth_response.status_code}")
    print("Please visit https://czds.icann.org/ to check your account")
