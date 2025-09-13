#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path
from typing import Tuple, List

import pandas as pd


TWITTER_CSV = Path("data/twitter_data.csv")
SENTIMENT_CSV = Path("data/sentiment_data.csv")
RANDOM_SEED = 1


def load_data(
    twitter_csv: Path, sentiment_csv: Path
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df_twitter = pd.read_csv(twitter_csv)
    df_sentiment = pd.read_csv(sentiment_csv)
    return df_twitter, df_sentiment


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates()


def filter_non_null_sentiment(df_sentiment: pd.DataFrame) -> Tuple[pd.DataFrame, int]:
    num_missing = df_sentiment["airline_sentiment"].isnull().sum()
    df_clean = df_sentiment.dropna(subset=["airline_sentiment"])
    return df_clean, num_missing


def inner_merge_on_unit_id(
    df_twitter: pd.DataFrame, df_sentiment_notnull: pd.DataFrame
) -> pd.DataFrame:
    return pd.merge(df_twitter, df_sentiment_notnull, on="_unit_id", how="inner")


def extract_mentions(text: str) -> List[str]:
    return re.findall(r"@\w+", text)


def add_mentions_column(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["mentions"] = df["text"].fillna("").apply(extract_mentions)
    return df


def report_merge_stats(
    df_twitter: pd.DataFrame,
    df_sentiment_notnull: pd.DataFrame,
    df_merged: pd.DataFrame,
) -> None:
    num_tweets_twitter = len(df_twitter)
    num_tweets_sentiment = len(df_sentiment_notnull)
    num_tweets_merged = len(df_merged)
    num_removed_twitter = num_tweets_twitter - num_tweets_merged
    num_removed_sentiment = num_tweets_sentiment - num_tweets_merged

    print(f"Total number of tweets in the merged dataset: {num_tweets_merged}")
    print(f"Number of removed tweets from the Twitter dataset: {num_removed_twitter}")
    print(
        f"Number of removed tweets from the sentiment dataset: {num_removed_sentiment}"
    )


def report_mentions(
    df: pd.DataFrame, sample_n: int = 15, seed: int = RANDOM_SEED
) -> None:
    total_mentions = df["mentions"].apply(len).sum()
    average_mentions = df["mentions"].apply(len).mean()
    random_sample = df["mentions"].sample(n=sample_n, random_state=seed)

    print(f"Total number of mentions: {total_mentions}")
    print(f"Average number of mentions per tweet: {average_mentions:.4f}")
    print("Random sample of 15 entries of the mentions column:")
    print(random_sample)


def main(
    twitter_csv: Path = TWITTER_CSV,
    sentiment_csv: Path = SENTIMENT_CSV,
) -> None:
    # Load
    df_twitter, df_sentiment = load_data(twitter_csv, sentiment_csv)

    # Deduplicate
    df_twitter = remove_duplicates(df_twitter)
    df_sentiment = remove_duplicates(df_sentiment)

    # Filter sentiment
    df_sentiment_notnull, num_missing = filter_non_null_sentiment(df_sentiment)
    print(f"Number of discarded lines: {num_missing}")

    # Merge
    df = inner_merge_on_unit_id(df_twitter, df_sentiment_notnull)
    report_merge_stats(df_twitter, df_sentiment_notnull, df)

    # Mentions
    df = add_mentions_column(df)
    report_mentions(df, sample_n=15, seed=RANDOM_SEED)


if __name__ == "__main__":
    main()
