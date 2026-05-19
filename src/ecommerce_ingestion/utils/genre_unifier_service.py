import pandas as pd

from ecommerce_ingestion.config.mappers import GENRE_MAPPER


def map_genre(tag: str) -> tuple[str, int]:
    normalized_tag = str(tag).strip().lower()

    return GENRE_MAPPER.get(
        normalized_tag,
        ("unknown", 999)
    )

def get_main_genres(tags: list[str]) -> tuple[str, str | None]:
    mapped_genres = []

    for tag in tags:
        genre, priority = map_genre(tag)

        if genre != "unknown":
            mapped_genres.append((genre, priority))

    if not mapped_genres:
        return "unknown", None

    unique_genres = list(set(mapped_genres))

    ordered_genres = sorted(
        unique_genres,
        key=lambda x: x[1]
    )

    primary_genre = ordered_genres[0][0]

    secondary_genre = (
        ordered_genres[1][0]
        if len(ordered_genres) > 1
        else None
    )

    return primary_genre, secondary_genre


def get_genre_unified_genre_data(primary_genre_data: pd.DataFrame) -> pd.DataFrame:

    secondary_genre_data = primary_genre_data

    primary_genre_data = primary_genre_data[
        primary_genre_data["primary_genre"] != "unknown"]
    secondary_genre_data = secondary_genre_data[
        secondary_genre_data["secondary_genre"] != "unknown"]

    primary_genre_data["unified_genre"] = primary_genre_data[
        "primary_genre"]
    secondary_genre_data["unified_genre"] = secondary_genre_data[
        "secondary_genre"]



    return pd.concat([primary_genre_data, secondary_genre_data]
)
