from datetime import datetime, timedelta
import sys

from decouple import config
import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = config("SENDGRID_API_KEY")
FROM_EMAIL = config("FROM_EMAIL")
TO_EMAIL = config("TO_EMAIL")
API_URL = "https://codechalleng.es/api/articles/"
ONE_WEEK = 7


def fetch_articles():
    response = requests.get(API_URL)
    response.raise_for_status()
    return response.json()


def filter_recent_articles(articles, days):
    recent_articles = []
    now = datetime.now()
    for article in articles:
        publish_date = datetime.strptime(
            article["publish_date"], "%Y-%m-%d %H:%M:%S+00:00"
        )
        if now - publish_date <= timedelta(days=days):
            recent_articles.append(article)
    return recent_articles


def send_email(from_email, to_email, subject, content):
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        plain_text_content=content,
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email sent with status code: {response.status_code}")
    except Exception as e:
        print(e)


def main(days=ONE_WEEK):
    articles = fetch_articles()
    recent_articles = filter_recent_articles(articles, days)
    subject = "New Pybites Articles"
    body = "\n\n".join(
        [f"{article['title']}\n{article['link']}"
         for article in recent_articles]
    )
    send_email(FROM_EMAIL, TO_EMAIL, subject, body)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        main()
    else:
        days = int(sys.argv[1])
        main(days)
