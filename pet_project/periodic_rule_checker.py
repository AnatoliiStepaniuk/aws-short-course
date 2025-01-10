import os
import json
import pymysql
import ssl
import requests

from email_sender import send_email

def lambda_handler(event, context):
    connection = get_secure_connection()
    try:
        rules = fetch_all_rules(connection)
        print(f"received rules from DB: {rules}")

        for rule in rules:
            company_symbol    = rule["company_symbol"]
            threshold         = rule["threshold"]
            comparison_op     = rule["comparison_operator"]
            event_active      = rule["event_active"]
            rule_id           = rule["id"]

            current_price = get_current_price(company_symbol)

            # Перевіряємо, чи виконується умова (>= або <)
            if check_condition(current_price, threshold, comparison_op):
                print(f"current price of {company_symbol} is: {current_price} which triggers the rule: {comparison_op}{threshold}")
                # Якщо вперше
                if not event_active:
                    # 1. Відправка нотифікації через метод send_email
                    send_email(
                        sender        = os.environ["EMAIL_SENDER"],
                        recipients    = [rule["user_email"]],
                        aws_region    = os.environ.get("AWS_REGION", "us-east-1"),
                        stock_symbol  = company_symbol,
                        stock_price   = str(current_price),
                        rule_id = rule_id,
                        template_dir  = '.',
                        template_file ='email_template.html'
                    )

                    # 2. Запис в таблицю notifications (історія відправлень)
                    insert_notification(connection, rule_id)

                    # 3. Оновити поле event_active -> TRUE
                    update_event_active(connection, rule_id, True)
                else:
                    print(f"current price of {company_symbol} has an ongoing event, ignoring it")
            else:
                # Якщо ціна більше не відповідає умові, скидаємо event_active
                if event_active:
                    update_event_active(connection, rule_id, False)

        return {
            "statusCode": 200,
            "body": json.dumps("Check complete")
        }
    finally:
        connection.close()


def check_condition(current_price, threshold, comparison_op):
    if comparison_op == '>=':
        return current_price >= threshold
    elif comparison_op == '<':
        return current_price < threshold
    else:
        raise ValueError(f"Unsupported comparison operator: {comparison_op}")


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


def fetch_all_rules(connection):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM notification_rules WHERE enabled = TRUE"
        cursor.execute(sql)
        return cursor.fetchall()


def insert_notification(connection, rule_id):
    with connection.cursor() as cursor:
        sql = """
            INSERT INTO notifications (rule_id, sent_at)
            VALUES (%s, NOW())
        """
        cursor.execute(sql, (rule_id,))
    connection.commit()


def update_event_active(connection, rule_id, is_active):
    with connection.cursor() as cursor:
        sql = """
            UPDATE notification_rules
            SET event_active = %s
            WHERE id = %s
        """
        cursor.execute(sql, (1 if is_active else 0, rule_id))
    connection.commit()


def get_current_price(symbol):
    api_token = os.environ["FINNHUB_API_TOKEN"]
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_token}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        return data.get("c")  # Return the "c" field (current price)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None