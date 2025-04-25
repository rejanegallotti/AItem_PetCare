"""Pydantic schemas for Twitter, Reddit, and News API responses.

Returns:
    TwitterPostsResponse, RedditPostsResponse, NewsArticlesResponse: Response models for each endpoint.
"""

from pydantic import BaseModel
from typing import List, Optional


class TwitterPost(BaseModel):
    """Schema for a single Twitter post.

    Returns:
        TwitterPost: Twitter post object.
    """

    id: str
    text: str
    author: str
    timestamp: str
    source: str
    company_query: str


class RedditPost(BaseModel):
    """Schema for a single Reddit post.

    Returns:
        RedditPost: Reddit post object.
    """

    id: str
    text: str
    author: Optional[str]
    timestamp: str
    source: str
    company_query: str


class TwitterPostsResponse(BaseModel):
    """Response model for Twitter posts endpoint.

    Returns:
        TwitterPostsResponse: Response containing a list of Twitter posts.
    """

    twitter_posts: List[TwitterPost]


class RedditPostsResponse(BaseModel):
    """Response model for Reddit posts endpoint.

    Returns:
        RedditPostsResponse: Response containing a list of Reddit posts.
    """

    reddit_posts: List[RedditPost]


class TitleContent(BaseModel):
    title: str
    content: str


class NewsArticlesResponse(BaseModel):
    news_articles: List[TitleContent]
