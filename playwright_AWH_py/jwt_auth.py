import jwt
import time
import requests
import os
from dotenv import load_dotenv

# =========================
# SALESFORCE CONFIG
# =========================

load_dotenv("conEnviron.env")

LOGIN_URL = os.getenv("SF_Login_url")
CLIENT_ID = os.getenv("SF_client_id")
USERNAME = os.getenv("SF_Username")

# Path to your private key file
PRIVATE_KEY_FILE = os.path.join(os.path.dirname(__file__), "server.key")


# =========================
# GET ACCESS TOKEN USING JWT
# =========================

def get_access_token():

    if not os.path.exists(PRIVATE_KEY_FILE):
        raise FileNotFoundError(f"server.key not found at {PRIVATE_KEY_FILE}")

    with open(PRIVATE_KEY_FILE, "r") as key_file:
        private_key = key_file.read()

    # JWT payload
    payload = {
        "iss": CLIENT_ID,                 # Consumer Key
        "sub": USERNAME,                  # Salesforce username
        "aud": LOGIN_URL,                 # login URL
        "exp": int(time.time()) + 300     # token valid for 5 minutes
    }

    # Create JWT token
    jwt_token = jwt.encode(payload, private_key, algorithm="RS256")

    # Call Salesforce OAuth endpoint
    response = requests.post(
        f"{LOGIN_URL}/services/oauth2/token",
        data={
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": jwt_token
        }
    )

    # Debug logs (VERY IMPORTANT for troubleshooting)
    print("\n================ JWT AUTH RESPONSE ================\n")
    print("Status Code:", response.status_code)
    print("Response:", response.text)
    print("\n===================================================\n")

    # Error handling
    if response.status_code != 200:
        raise Exception(f"JWT Authentication Failed: {response.text}")

    result = response.json()

    access_token = result.get("access_token")
    instance_url = result.get("instance_url")

    print("✅ JWT Login Successful")
    print("Instance URL:", instance_url)
    frontdoor_url = f"{instance_url}/secur/frontdoor.jsp?sid={access_token}"
    return access_token, instance_url, frontdoor_url


if __name__ == "__main__":
    token, url, frontdoor_url = get_access_token()

    print("\n================ FINAL RESULT ================\n")
    print("Access Token:", token)
    print("Instance URL:", url)
    print("Frontdoor URL:", frontdoor_url)