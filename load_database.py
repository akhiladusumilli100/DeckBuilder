import sqlite3
import requests
import gzip
import json


# Connect to database
connection = sqlite3.connect("carddatabase.db")
cursor = connection.cursor()

print("Dropping existing cards table...")
cursor.execute("DROP TABLE IF EXISTS cards")
print("Creating new cards table...")

# Create cards table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS cards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scryfall_id TEXT UNIQUE,
        oracle_id TEXT,
        name TEXT NOT NULL,
        mana_cost TEXT,
        cmc INTEGER,
        type_line TEXT,
        keywords TEXT,
        oracle_text TEXT,
        power TEXT,
        toughness TEXT,
        colors TEXT,
        color_identity TEXT
    )
""")


# Get Scryfall bulk-data information
print("Getting Scryfall bulk data information...")

response = requests.get(
    "https://api.scryfall.com/bulk-data",
    headers={
        "User-Agent": "MTG-DeckBuilder/1.0",
        "Accept": "application/json"
    }
)

response.raise_for_status()

bulk_info = response.json()


# Find Oracle Cards dataset
oracle_data = None

for bulk_file in bulk_info["data"]:
    if bulk_file["type"] == "oracle_cards":
        oracle_data = bulk_file
        break


if oracle_data is None:
    raise Exception("Could not find Oracle Cards bulk data")

download_url = oracle_data["jsonl_download_uri"]

print("Downloading Scryfall card data...")

cards_response = requests.get(
    download_url,
    headers={
        "User-Agent": "MTG-DeckBuilder/1.0",
        "Accept": "application/json"
    }
)

cards_response.raise_for_status()

print("Download complete. Reading cards...")

# Decompress the gzip file
decompressed_data = gzip.decompress(cards_response.content)

# JSONL = one JSON object per line
cards = [
    json.loads(line)
    for line in decompressed_data.decode("utf-8").splitlines()
]

print(f"Downloaded {len(cards)} cards.")


# Insert cards into SQLite
print("Adding cards to database...")

for card in cards:

    # Only add cards that are legal in Commander
    if card.get("legalities", {}).get("commander") != "legal":
        continue

    cursor.execute("""
        INSERT OR REPLACE INTO cards (
            scryfall_id,
            oracle_id,
            name,
            mana_cost,
            cmc,
            type_line,
            keywords,
            oracle_text,
            power,
            toughness,
            colors,
            color_identity
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        card["id"],
        card.get("oracle_id"),
        card["name"],
        card.get("mana_cost"),
        card.get("cmc"),
        card.get("type_line"),
        ",".join(card.get("keywords", [])),
        card.get("oracle_text"),
        card.get("power"),
        card.get("toughness"),
        ",".join(card.get("colors", [])),
        ",".join(card.get("color_identity", []))
    ))


# Save changes
connection.commit()
connection.close()

print("Cards successfully imported!")