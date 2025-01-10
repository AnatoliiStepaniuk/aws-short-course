import boto3
from botocore.exceptions import ClientError
from template_builder import render_email

def send_email(sender, recipients, aws_region, stock_symbol, stock_price, rule_id, template_dir='.', template_file='email_template.html'):
    print(f"send_email params - sender: {sender}, recipients: {recipients}, aws_region: {aws_region}, stock_symbol: {stock_symbol}, stock_price: {stock_price}, template_dir: {template_dir}, template_file: {template_file}")

    subject, body_html, body_text = render_email(stock_symbol, stock_price, rule_id, template_dir, template_file)

    ses_client = boto3.client('ses', region_name=aws_region)

    try:
        response = ses_client.send_email(
            Source=sender,
            Destination={
                'ToAddresses': recipients,
            },
            Message={
                'Subject': {
                    'Data': subject,
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Html': {
                        'Data': body_html,
                        'Charset': 'UTF-8'
                    },
                    'Text': {
                        'Data': body_text,
                        'Charset': 'UTF-8'
                    }
                }
            }
        )
    except ClientError as e:
        print(f"Error sending email: {e.response['Error']['Message']}")
        raise e
    else:
        print(f"Email sent! Message ID: {response['MessageId']}")
        return response
