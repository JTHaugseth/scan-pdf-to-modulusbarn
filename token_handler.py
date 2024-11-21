import requests
import jwt
import time
from datetime import datetime, timezone
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# Configuration
CLIENT_ID = 'PASTE_CLIENT_ID_HERE' # Maskinporten Client ID for authentication
TOKEN_ENDPOINT = 'PASTE_TOKEN_ENDPOINT_HERE' # Maskinporten Token endpoint URL
KEY_ID = 'PASTE_KEY_ID_HERE' # Key ID associated with the private key
SCOPE = 'PASTE_SCOPE_HERE' # Modulus Barn API scope
PRIVATE_KEY_PATH = 'PATH_TO_PRIVATEKEY_._PEM' # Path to the private key file. Has to be .pem made from Enterprise Certificate (Virksomhetssertifikat)

# Load the private key from a PEM file
def load_private_key(path):
    with open(path, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key

# Generate a JWT for authentication
def generate_jwt(client_id, scope, private_key, kid, token_endpoint):
    current_time = int(time.time())
    payload = {
        'iss': client_id,
        'sub': client_id,
        'aud': token_endpoint,
        'scope': scope,
        'exp': current_time + 60,
        'iat': current_time,
    }
    headers = {
        'kid': kid,
        'alg': 'RS256',
        'typ': 'JWT'
    }
    encoded_jwt = jwt.encode(
        payload,
        private_key,
        algorithm='RS256',
        headers=headers
    )
    return encoded_jwt

# Request an access token
def get_access_token():
    private_key = load_private_key(PRIVATE_KEY_PATH)
    jwt_token = generate_jwt(CLIENT_ID, SCOPE, private_key, KEY_ID, TOKEN_ENDPOINT)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        'assertion': jwt_token,
    }

    # Send a POST request to the token endpoint
    response = requests.post(TOKEN_ENDPOINT, headers=headers, data=data)
    if response.status_code == 200: # Token retrieved successfully
        token_response = response.json()
        return token_response.get('access_token')
    else: # Token retrieval failed
        raise Exception(f"Failed to obtain access token: {response.status_code}, {response.text}")