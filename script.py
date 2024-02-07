from datetime import datetime, timedelta, UTC
from typing import NamedTuple

import feedparser
from dateutil.parser import parse
from decouple import config
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = config("SENDGRID_API_KEY")
FROM_EMAIL = config("FROM_EMAIL")
TO_EMAIL = config("TO_EMAIL")
PLANET_PYTHON_FEED = "https://planetpython.org/rss20.xml"
ONE_DAY = 1


class Article(NamedTuple):
    title: str
    link: str
    publish_date: str


def fetch_articles() -> list[Article]:
    feed = feedparser.parse(PLANET_PYTHON_FEED)
    return [
        Article(entry.title, entry.link, entry.published)
        for entry in feed.entries
    ]


def filter_recent_articles(
    articles: list[Article], days: int = ONE_DAY
) -> list[Article]:
    recent_articles = []
    now = datetime.now(UTC)
    for article in articles:
        publish_date = parse(article.publish_date)
        if now - publish_date <= timedelta(days):
            recent_articles.append(article)
    return recent_articles


def send_email(
    from_email: str, to_email: str, subject: str, content: str
) -> None:
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=content,
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email sent with status code: {response.status_code}")
    except Exception as e:
        print(e)


def main() -> None:
    articles = fetch_articles()
    recent_articles = filter_recent_articles(articles)
    if len(recent_articles) == 0:
        print("No new articles found")
        return
    subject = "New Planet Python articles"

    def _create_link(article: Article) -> str:
        return f"<a href='{article.link}'>{article.title}</a>"

    body = "<br>".join(
        [_create_link(article) for article in recent_articles]
    )
    send_email(FROM_EMAIL, TO_EMAIL, subject, body)


if __name__ == "__main__":
    main()
