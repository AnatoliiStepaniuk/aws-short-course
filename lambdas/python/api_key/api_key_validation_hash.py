import json
import os
import hashlib

def is_api_key_correct(request_api_key):
    # Return False if the API key is not provided
    if not request_api_key:
        return False

    API_KEY_HASH = os.getenv("API_KEY_HASH")

    hashed_api_key = hashlib.sha256(request_api_key.encode()).hexdigest()

    return hashed_api_key == API_KEY_HASH

def lambda_handler(event, context):

    hashlib.sha256('some-password'.encode()).hexdigest()

    hash = hashlib.sha256('my-secret-api-key-from-env-vars'.encode()).hexdigest()
    print(hash)
    hash = hashlib.sha256('my-secret-api-key-from-env-vars'.encode()).hexdigest()
    print(hash)
    hash = hashlib.sha256('my-secret-api-key-from-env-vars'.encode()).hexdigest()
    print(hash)
    hash = hashlib.sha256('my-secret-api-key-from-env-vars1'.encode()).hexdigest()
    print(hash)
    hash = hashlib.sha256('my-secret-api-key-from-env-vars1'.encode()).hexdigest()
    print(hash)
    hash = hashlib.sha256('my-secret-api-key-from-env-vars1'.encode()).hexdigest()
    print(hash)

    # Retrieve API Key from Authorization header
    headers = event.get("headers", {})
    api_key = headers.get("authorization")

    # If the API key is not correct, return 403
    if not is_api_key_correct(api_key):
        return {
            "statusCode": 403,
            "body": json.dumps({"message": "Unauthorized"})
        }

    # Proceed with the rest of the logic if the API key is correct
    # Example logic: Replace with your actual implementation
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "API key is valid, proceeding with the logic"})
    }


#lambda_handler(None, None)