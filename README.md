## Description

This project automates tweet retrieval from Twitter without using browser automation.  
It sends HTTP requests, processes the response data, and writes each tweet to a new line in an output file.

## Dependencies

- Python 3.8+
- `pip install -r requirements.txt`

## Parameters
The script exposes configurable parameters via method arguments.

```username```
- Type: str
- Default: elonmusk

```count```
- Type: int
- Default: 10

## Usage

#### Example #1 (using defalut params)
```python
scraper = TwitterScraper()
user_data = scraper.get_user_by_screen_name()
user_id = user_data["data"]["user"]["result"]["rest_id"]
tweets_data = scraper.get_user_tweets(user_id)
```

#### Example #2 (specify own params)
```python
scraper = TwitterScraper()
user_data = scraper.get_user_by_screen_name(username="cow")
user_id = user_data["data"]["user"]["result"]["rest_id"]
tweets_data = scraper.get_user_tweets(user_id, count=20)
```

## Known Limitations

- The script may not bypass CAPTCHAs or advanced anti-bot mechanisms.
- Excessive requests may trigger rate limits or temporary blocking by the target server.
