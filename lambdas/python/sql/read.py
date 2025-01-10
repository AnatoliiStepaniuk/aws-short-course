import pymysql
import os
import json
from datetime import date

# RDS configurations
rds_host = os.environ['RDS_HOST']
rds_user = os.environ['RDS_USER']
rds_password = os.environ['RDS_PASSWORD']
rds_db = os.environ['RDS_DB']

# MySQL connection setup
def connect_to_db():
    try:
        conn = pymysql.connect(
            host=rds_host,
            user=rds_user,
            password=rds_password,
            db=rds_db,
            connect_timeout=5
        )
        return conn
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL: {e}")
        return None


# Read data from database with custom SQL query
def read_from_db(conn, query):
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return result
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
        return None


# Custom JSON serializer for handling date objects
def custom_json_serializer(obj):
    if isinstance(obj, (date,)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def close(conn):
    conn.commit()
    conn.close()


# Lambda handler function
def handler(event, context):
    conn = connect_to_db()

    if conn is None:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error connecting to the database.'})
        }

    query = "SELECT * FROM aws_course_students LIMIT 100;"
    result = read_from_db(conn, query)
    close(conn)

    if result is None:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error executing query.'})
        }

    result_json = json.dumps(result, default=custom_json_serializer, indent=4, ensure_ascii=False)

    print(result_json)

    return {
        'statusCode': 200,
        'body': result_json
    }

#handler(None, None)