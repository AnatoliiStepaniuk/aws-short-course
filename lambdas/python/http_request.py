import urllib.request
import json
import urllib.error


def make_http_request(api_url, data=None, method='GET'):
    try:
        if data is not None:
            # Convert data to JSON string and then to bytes
            data = json.dumps(data).encode('utf-8')
        else:
            data = None

        # Define headers inside the function
        headers = {
            'Content-Type': 'application/json'
        }

        req = urllib.request.Request(api_url, data=data, headers=headers, method=method)

        with urllib.request.urlopen(req) as response:
            status_code = response.getcode()
            response_body = response.read()
            response_data = json.loads(response_body)
            return response_data, status_code

    except urllib.error.HTTPError as e:
        return {"error": e.reason}, e.code
    except urllib.error.URLError as e:
        return {"error": str(e)}, 500


def lambda_handler(event, context):
    api_url = "https://api.monobank.ua/bank/currency"

    json_data, status_code = make_http_request(api_url)

    return {
        "statusCode": status_code,
        "body": json_data
    }
