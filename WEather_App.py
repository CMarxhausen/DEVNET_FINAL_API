#Checks to see if GNews is installed. If not, it installs it
import subprocess
import sys

try:
    import gnews
except ImportError:
    print("Installing gnews...")
    subprocess.run([sys.executable, "-m", "pip", "install", "gnews"], check=True)
# imports the requests and json libraries to make API calls and format the response
import requests
from gnews import GNews

# valid states for the weather API
VALID_STATES = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
}

# valid news categories from GNews
NEWS_CATEGORIES = {
    "1": ("WORLD",      "World News"),
    "2": ("NATION",     "U.S. News"),
    "3": ("BUSINESS",   "Business"),
    "4": ("TECHNOLOGY", "Technology"),
    "5": ("SPORTS",     "Sports"),
    "6": ("SCIENCE",    "Science"),
    "7": ("HEALTH",     "Health"),
    "8": ("POLITICS",   "Politics"),
    "9": ("FINANCE",    "Finance"),
}

# def function for the weather API
def check_weather_alerts():
    while True:
        state = input("Enter a state abbreviation (e.g., TX, NY) or 'back' to return: ").strip().upper()
        print()

        if state == "BACK":
            break
        if state not in VALID_STATES:
            print("Invalid state abbreviation. Please try again.\n")
            continue
        try:
            response = requests.get(
                f"https://api.weather.gov/alerts/active?area={state}",
                timeout=10  # causes code to return user back to select the state again if the time reaches limit
            )
            response.raise_for_status()
            alerts = response.json().get("features", [])
        except requests.exceptions.Timeout:
            print("Request timed out. Please try again.\n")
            continue
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}\n")
            continue

        if alerts:
            print(f"Found {len(alerts)} active alert(s) for {state}:\n")  # displays number of alerts
            for alert in alerts:
                props = alert["properties"]
                print("------------------------------------------------------------------------------------------------------------------------")
                print(f"⚠️  {props.get('headline', 'No headline')}")  # breaks alert up to make it easier to read
                print(f"   Severity: {props.get('severity', 'Unknown')}")
                print(f"   Urgency:  {props.get('urgency', 'Unknown')}")
                print(f"   Ends:     {props.get('ends', 'Not specified')}")
                print()
        else:
            print(f"No active weather alerts for {state}.\n")

# function for Google News
def check_news():
    google_news = GNews(language="en", country="US", max_results=5) # basic gnews set up - Change the max_results if we want more than 5 results to show up

    while True:
        print("-----News Categories-----")
        for key, (_, label) in NEWS_CATEGORIES.items():
            print(f"{key}: {label}")
        print("S: Search by keyword") #Allows the possibility to search outside the 9 categories listed.
        print("-------------------------\n")

        choice = input("Which news category would you like to search for?\n-Enter a number to select from the list or 'S' to search by keyword\n-Enter 'back' to return\nSelection: ").strip().upper()
        print()

        if choice == "BACK":
            break

        try:
            if choice == "S": #allows the user to search by keyword and not by number
                keyword = input("Enter search keyword: ").strip()
                print()
                if not keyword:
                    print("No keyword entered. Please try again.\n")
                    continue
                articles = google_news.get_news(keyword)
                header = f'Search results for "{keyword}"'

            elif choice in NEWS_CATEGORIES:
                topic, label = NEWS_CATEGORIES[choice]
                articles = google_news.get_news_by_topic(topic.upper())
                header = label
            else:
                print("Invalid news category choice. Please try again.\n")
                continue

        except Exception as e:
            print(f"Error occurred: {e}\n")
            continue

        if not articles:
            print(f"No news articles found for {choice}\nPlease select a different news category.\n")
            continue

        #this is the output for the articles - shows title, source, date, and a url
        print(f"{header} (Top {len(articles)} )\n")
        for i, article in enumerate(articles, 1):
            print("----------------------------------------------------------------------------------------------------------------------------")
            print(f"{i}. {article.get('title', 'No title')}")
            print(f"   Source:      {article.get('publisher', {}).get('title', 'Unknown')}")
            print(f"   Published:   {article.get('published date', 'Unknown')}")
            print(f"   URL:         {article.get('url', 'No URL')}")
            print()


# Main loop —  comes after the function definitions
while True:  # displays which tools are available
    print("--------- Weather & News Alerts ---------")  # RENAME THIS TO SOMETHING ELSE ONCE WE GET THE ADDITIONAL APIS ADDED
    print("1. Check active weather alerts by state")
    print("2. Check current news")
    print("-----------------------------------------")
    # add another option if we want here (fun fact?)
    print("Type 'exit' to quit\n")
    # user enters choice
    option = input("Enter the number of your choice: ").strip().lower()
    print()
    # code calls the functions
    if option == "1":
        check_weather_alerts()
    elif option == "2":
        check_news()
    elif option == "exit":
        print("Exiting the program. Stay safe!")
        break
    else:
        print("Invalid option. Please enter 1, 2, or 'exit'.\n")
