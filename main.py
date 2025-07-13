import urllib.request
import sys
import os
import redis
import json
from dotenv import load_dotenv

# Load and get .env vars
load_dotenv()

api_key = os.environ.get("WEATHER_API_KEY", "default")

# Set up Redis client
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# Check connection
try:
    redis_client.ping()
    print("Connected to Redis!")
except redis.ConnectionError:
    print("Unable to connect to Redis.")
    sys.exit()

# Returns url for single date or a range of 2 dates
def get_url(location, start_date, end_date):

    if end_date:
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{start_date}/{end_date}?unitGroup=metric&key={api_key}&contentType=json"
    else:
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{start_date}?unitGroup=metric&key={api_key}&contentType=json"
    print(url)
    return url


# Fetch weather from API
def fetch_weather(location, start_date, end_date):

    try:
        url = get_url(location, start_date, end_date)
        with urllib.request.urlopen(url) as response:
            data = json.load(response)
            return data
        
    except urllib.error.HTTPError as e:
        print("HTTPError:", e.code, e.read().decode())
        sys.exit()

    except urllib.error.URLError as e:
        print("URLError:", e.reason)
        sys.exit()

# Check Redis cache or fetch new
def get_weather(location, start_date, end_date):

    # Normalize redis key
    redis_key = f"weather:{location.lower()}:{start_date}"
    if end_date:
        key += f":{end_date}"
    
    cached = redis_client.get(redis_key)
    if cached:
        print("Cache hit")
        return json.loads(cached)
    else:
        print("Cache miss - fetching from API")
        data = fetch_weather(location, start_date, end_date)
        redis_client.set(redis_key, json.dumps(data), ex=300)  # Cache for 5 mins
        return data

# Get location and dates for API call from user
def get_prompt():

    dynamic_dates = ["today", "tommorow", "yesterday", "next7days", "last7days", "next15days"]
    print(f"""Date must in format 'YYYY/MM/DD'.
Format for range of 2 dates is 'YYYY/MM/DD to YYYY/MM/DD'.
Dynamic date options include: {dynamic_dates}""")
    
    location = input("Location: ")
    if not location:
        print("Location required!")
        sys.exit()

    date = input("Date: ").strip().lower()

    # If dateformate is YYYY/MM/DD to YYYY/MM/DD
    if "to" in date and date not in dynamic_dates:
        start_date, end_date = date.split("to")
        return location, start_date, end_date
    
    # else return single date, 0 is checked for in get_url()
    return location, date, 0
    

def main():
    # get prompts for data
    location, start_date, end_date = get_prompt()

    weather_data = get_weather(location, start_date, end_date)

    # Save to local file
    with open("weather.json", "w") as f:
        json.dump(weather_data, f, indent=4)

    print("Weather saved to weather.json")


if __name__ == "__main__":
    main()