import os

from newsapi import NewsApiClient


def get_articles(company_name: str):
    news = NewsApiClient(api_key=os.environ.get("NEWS_API"))
    news_data = news.get_everything(qintitle=company_name, sort_by="publishedAt", page_size=3, language="en")
    articles = news_data["articles"]
    articles_to_send = [
        [f"{company_name}: \nHeadline: {article["title"]}\nBriefing: {article["description"]}\nFull Report At: {article["url"]}", article["url"]]
        for article in articles]
    return articles_to_send

