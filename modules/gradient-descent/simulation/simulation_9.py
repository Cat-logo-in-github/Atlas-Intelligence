from pathlib import Path
import re
import requests
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt


WARS_URL = "https://en.wikipedia.org/wiki/List_of_wars_in_the_Indian_subcontinent"
USER_AGENT = "AtlasSimulation/1.0"


def _extract_year(text):
    years = [int(y) for y in re.findall(r"\b(1[5-7]\d{2}|1800)\b", str(text))]
    return min(years) if years else None


def _extract_article_title(href):
    if not href or "/wiki/" not in href:
        return None
    title = href.split("/wiki/")[-1]
    title = title.split("#")[0]
    return title


def _fetch_coordinates(article_title):
    url = (
        "https://en.wikipedia.org/w/api.php"
        "?action=query"
        "&prop=coordinates"
        "&colimit=1"
        "&titles={}"
        "&format=json"
    ).format(article_title)

    r = requests.get(
        url,
        headers={"User-Agent": USER_AGENT},
        timeout=20,
    )
    r.raise_for_status()
    pages = r.json()["query"]["pages"]

    for page in pages.values():
        coords = page.get("coordinates")
        if coords:
            return coords[0]["lat"], coords[0]["lon"]

    return None


def build(simulation):
    world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    india = world[world["name"] == "India"]

    tables = pd.read_html(WARS_URL)

    response = requests.get(
        WARS_URL,
        headers={"User-Agent": USER_AGENT},
        timeout=30,
    )
    response.raise_for_status()

    html_tables = pd.read_html(response.text, extract_links="all")

    battles = []

    for table in html_tables:
        cols = [str(c).lower() for c in table.columns]

        if not any("battle" in c or "name" in c for c in cols):
            continue

        battle_col = None
        date_col = None
        conflict_col = None

        for c in table.columns:
            lc = str(c).lower()
            if battle_col is None and ("battle" in lc or "name" in lc):
                battle_col = c
            if date_col is None and ("date" in lc or "year" in lc):
                date_col = c
            if conflict_col is None and ("war" in lc or "conflict" in lc):
                conflict_col = c

        if battle_col is None or date_col is None:
            continue

        for _, row in table.iterrows():
            battle_cell = row[battle_col]
            if isinstance(battle_cell, tuple):
                battle_name, href = battle_cell
            else:
                battle_name = str(battle_cell)
                href = None

            year = _extract_year(row[date_col])
            if year is None or year < 1500 or year > 1800:
                continue

            article = _extract_article_title(href)
            if article is None:
                continue

            try:
                coord = _fetch_coordinates(article)
            except Exception:
                coord = None

            if coord is None:
                continue

            lat, lon = coord

            if not (6 <= lat <= 38 and 68 <= lon <= 98):
                continue

            battles.append(
                {
                    "battle": battle_name,
                    "year": year,
                    "latitude": lat,
                    "longitude": lon,
                    "conflict": (
                        row[conflict_col][0]
                        if conflict_col is not None
                        and isinstance(row[conflict_col], tuple)
                        else str(row[conflict_col])
                        if conflict_col is not None
                        else ""
                    ),
                }
            )

    df = (
        pd.DataFrame(battles)
        .drop_duplicates(subset=["battle", "year"])
        .sort_values("year")
        .reset_index(drop=True)
    )

    fig, ax = plt.subplots(figsize=(8, 10))

    india.plot(
        ax=ax,
        color="#f5f5f5",
        edgecolor="black",
        linewidth=0.8,
    )

    if not df.empty:
        ax.scatter(
            df["longitude"],
            df["latitude"],
            s=28,
            color="crimson",
            edgecolor="black",
            linewidth=0.3,
            zorder=5,
        )

    ax.set_title("Major Battles in India (1500–1800)")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_aspect("equal")

    simulation.figure(fig, "india_major_battles_1500_1800")
    simulation.data(df, "india_major_battles_1500_1800_data")