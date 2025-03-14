import requests
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Set Chess.com username
username = "alexulanch"

# Start and end dates
start_date = datetime(2025, 3, 1)  # March 2025
end_date = datetime(2021, 7, 1)    # July 2021

# Output PGN file
output_file = "all_chess_games.pgn"

# Open file for writing merged PGNs
with open(output_file, "w", encoding="utf-8") as outfile:
    current_date = start_date

    while current_date >= end_date:
        year = current_date.year
        month = current_date.month
        formatted_month = f"{month:02d}"  # Ensure 2-digit format

        # Construct API URL
        url = f"https://api.chess.com/pub/player/{username}/games/{year}/{formatted_month}/pgn"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        print(f"Fetching: {url}")

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raises error for 403, 404, etc.

            if response.text.strip():
                outfile.write(f"\n\n; Games from {year}-{formatted_month}\n")
                outfile.write(response.text)
                print(f"✅ Added games from {year}-{formatted_month}")
            else:
                print(f"⚠️ No games found for {year}-{formatted_month}")

        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching {year}-{formatted_month}: {e}")

        # ✅ Correct way to decrement a month, even handling year changes
        current_date -= relativedelta(months=1)

        # Avoid API rate limits
        time.sleep(1)

print("\n🎉 Done! All games are saved in 'all_chess_games.pgn'.")