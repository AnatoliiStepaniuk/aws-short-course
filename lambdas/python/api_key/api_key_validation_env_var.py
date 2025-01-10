import json
import os

def is_api_key_correct(request_api_key):
    # Return False if the API key is not provided
    if not request_api_key:
        return False

    #CORRECT_API_KEY = "my-secret-api-key" # simple way - hardcoded, without Env Vars

    CORRECT_API_KEY = os.getenv("API_KEY")

    return request_api_key == CORRECT_API_KEY

def lambda_handler(event, context):
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