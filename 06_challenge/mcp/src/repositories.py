"""Repositories for fetching mock posts from various sources.

Returns:
    list[dict]: List of post/article dictionaries for each source.
"""

import os
from datetime import datetime
from typing import Any, Dict, List

import praw
import tweepy
from dotenv import find_dotenv, load_dotenv
from tavily import TavilyClient

load_dotenv(find_dotenv())

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "brand-monitor-agent")


def get_twitter_posts(company_name: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """
    Fetch recent tweets mentioning the given company via Tweepy (Twitter API v2).

    Args:
        company_name (str): The company name to search tweets for.
        max_results (int): Number of tweets to fetch (up to 100).

    Returns:
        List[Dict[str, Any]]: Tweets with keys 'id', 'text', 'author', 'timestamp', 'source', and 'company_query'.
    """
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    if not bearer_token:
        raise RuntimeError("Set TWITTER_BEARER_TOKEN in your env")

    client = tweepy.Client(bearer_token=bearer_token)

    # search_recent_tweets returns a Response with .data (list of Tweet objects)
    resp = client.search_recent_tweets(
        query=company_name,
        tweet_fields=["created_at","author_id"],
        expansions=["author_id"],
        user_fields=["username"],
        max_results=max_results
    )

    tweets = resp.data or []
    users = {u.id: u.username for u in resp.includes.get("users", [])}

    return [
        {
            "id":            t.id,
            "text":          t.text,
            "author":        users.get(t.author_id, ""),
            "timestamp":     t.created_at.isoformat(),
            "source":        "twitter",
            "company_query": company_name,
        }
        for t in tweets
    ]



def get_reddit_posts(company_name: str) -> List[Dict[str, Any]]:
    """Fetch real Reddit posts for a company using PRAW.

    Args:
        company_name (str): The company name to search Reddit posts for.

    Returns:
        List[Dict[str, Any]]: List of Reddit post dictionaries.
    """
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )
    posts = []
    for submission in reddit.subreddit('all').search(company_name, sort='new', limit=10):
        posts.append({
            "id": submission.id,
            "text": submission.title,
            "author": str(submission.author) if submission.author else None,
            "timestamp": datetime.utcfromtimestamp(submission.created_utc).isoformat(),
            "source": "reddit",
            "company_query": company_name,
        })
    return posts


def get_news_articles(company_name: str) -> List[Dict[str, Any]]:
    """Fetch mock news articles for a company.

    Args:
        company_name (str): The company name to search news articles for.

    Returns:
        List[Dict[str, Any]]: List of mock news article dictionaries.
    """

    client = TavilyClient(os.getenv("TAVILY_API_KEY"))
    response = client.search(
        query="company_name",
        topic="news"
    )
    results = response.get("results", [])
    parsed = []
    for article in results:
        title = article.get("title", "").strip()
        content = article.get("content", "").strip()
        parsed.append({
            "title": title,
            "content": content
        })

    return parsed
