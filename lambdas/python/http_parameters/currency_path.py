import urllib.request
import json
import urllib.error

def get_currency_code(currency: str) -> int:
    # Mapping of currency codes to ISO 4217 numeric codes
    currency_mapping = {
        "USD": 840,
        "UAH": 980,
        "EUR": 978,
        "GBP": 826,
        "JPY": 392,
        # Add more currency codes as needed
    }

    if currency in currency_mapping:
        return currency_mapping[currency]
    else:
        raise ValueError(f"Currency code '{currency}' is not supported.")


def get_currency_rate(currency_from: str, currency_to: str, rate_type: str, json_data):
    # Convert currency from and to ISO 4217 numeric codes
    currency_from_num = get_currency_code(currency_from)
    currency_to_num = get_currency_code(currency_to)
    print(f"Searching for currency rate for codes from {currency_from_num} to {currency_to_num}")

    # If json_data is not a string, convert it to a JSON string
    if isinstance(json_data, list):
        json_data = json.dumps(json_data)

    # Load JSON data
    data = json.loads(json_data)

    # Search for the specific currency pair and rate type
    for item in data:
        if item["currencyCodeA"] == currency_from_num and item["currencyCodeB"] == currency_to_num:
            if rate_type in item:
                return item[rate_type]
            else:
                raise ValueError(f"Rate type '{rate_type}' not found in the provided data.")

    # If no match found, raise an error
    raise ValueError("The requested currency pair is not available in the provided data.")


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

    # currency_from = "USD"
    # currency_to = "UAH"
    # rate_type = "rateBuy"

    path_segments = event["rawPath"].split("/")
    currency_from = path_segments[4]  # e.g. "USD"
    currency_to   = path_segments[6]  # e.g. "UAH"
    rate_type     = path_segments[8]  # e.g. "rateSell"

    print(f"Making request for {currency_from}/{currency_to} ({rate_type})")
    json_data, status_code = make_http_request(api_url)

    if status_code != 200:
        return {
            "statusCode": status_code,
            "body": json_data
        }

    rate = get_currency_rate(currency_from, currency_to, rate_type, json_data)

    return {
        "statusCode": status_code,
        "body": {
            "fromCurrency": currency_from,
            "toCurrency": currency_to,
            "rate": rate
        }
    }
