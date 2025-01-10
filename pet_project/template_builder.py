import os
from jinja2 import Environment, FileSystemLoader

def render_email(stock_symbol, stock_price, rule_id, template_dir='.', template_file='email_template.html'):
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_file)

    body_html = template.render(STOCK_SYMBOL=stock_symbol, STOCK_PRICE=stock_price, UNSUBSCRIBE_URL = os.environ["UNSUBSCRIBE_URL"], UNSUBSCRIBE_API_KEY = os.environ["UNSUBSCRIBE_API_KEY"], RULE_ID = rule_id)

    subject = f"Notification: {stock_symbol} price alert"
    body_text = f"The price of {stock_symbol} is ${stock_price}."
    return (
        subject,
        body_html,
        body_text
    )






