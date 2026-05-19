import pandas as pd


def build_score_bucket(score: int) -> str:
    if pd.isna(score):
        return "unknown"

    if score >= 90:
        return "masterpiece"

    if score >= 80:
        return "excellent"

    if score >= 70:
        return "good"

    if score >= 60:
        return "average"

    return "poor"

def build_price_bucket(price: float) -> str:

    if pd.isna(price):
        return "unknown"

    if price == 0:
        return "free"

    if price < 10:
        return "<10"

    if price < 20:
        return "10-20"

    if price < 40:
        return "20-40"

    if price < 60:
        return "40-60"

    return "60+"