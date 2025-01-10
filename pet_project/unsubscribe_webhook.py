import os
import pymysql
import json
import ssl


# https://LAMBDA_PUBLIC_URL/?apiKey=SOME_API_KEY&ruleId=2

def lambda_handler(event, context):
    # Parse query parameters
    query_params = event.get('queryStringParameters', {})
    api_key = query_params.get('apiKey')
    rule_id = query_params.get('ruleId')

    # Validate API key
    if api_key != os.environ['API_KEY']:
        return {
            "statusCode": 403,
            "body": json.dumps({"message": "Invalid API key."})
        }

    # Validate rule ID
    if not rule_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Missing rule ID."})
        }

    try:
        # Attempt to delete the rule
        rows_deleted = disable_rule(rule_id)

        # Return response based on deletion result
        if rows_deleted > 0:
            return {
                "statusCode": 200,
                "body": json.dumps({"message": f"Rule with ID {rule_id} has been removed."})
            }
        else:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": f"No rule found with ID {rule_id}."})
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "An error occurred.", "error": str(e)})
        }


def get_secure_connection():
    ssl_context = ssl.create_default_context()
    return pymysql.connect(
        host      = os.environ["DB_HOST"],
        user      = os.environ["DB_USER"],
        password  = os.environ["DB_PASSWORD"],
        database  = os.environ["DB_NAME"],
        cursorclass=pymysql.cursors.DictCursor,
        ssl={'ssl': ssl_context}  # Enforce SSL
    )

def disable_rule(rule_id):
    connection = get_secure_connection()
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE notification_rules SET enabled = FALSE WHERE id = %s"
            rows_updated = cursor.execute(sql, (rule_id,))
            connection.commit()
        return rows_updated
    finally:
        connection.close()
