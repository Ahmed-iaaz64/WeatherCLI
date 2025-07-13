# ☁️ WeatherCLI

**WeatherCLI** is a Python script that fetches weather data from the Visual Crossing API. It supports dynamic and custom date ranges, and uses Redis to cache results for 5 minutes.

---

## Features

- ✅ Search by location and date
- ✅ Supports single dates and ranges (`2025/07/01 to 2025/07/07`)
- ✅ Accepts dynamic dates like `today`, `yesterday`, `next7days`
- ✅ Uses Redis caching to avoid duplicate API calls
- ✅ Saves results to `weather.json`
- ✅ Can be reused by importing `get_weather_data(...)`

---

## Setup

1. Install packages:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file:

```
WEATHER_API_KEY=your_visual_crossing_key
```

3. Run Redis locally (default port 6379).

---

## Usage

```bash
python weathercli.py
```

Example:

```
Location: london
Date: today
```

---

## Example (as a function)

```python
from weathercli import get_weather_data

data = get_weather_data("tokyo", "today")
print(data["days"][0]["tempmax"])
```

---

## Author

Made by [Your Name]
