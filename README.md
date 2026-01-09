## How to Run the Script

1. Install dependencies.
2. Setup .env variables(get it from browser)
3. Run the script using:

```sh
python twitter_scanario.py
```

## Dependencies

- Python 3.8+
- `pip install -r requirements.txt`

## Description

This project automates tweet retrieval from Twitter without using browser automation.  
It sends HTTP requests, processes the response data, and writes each tweet to a new line in an output file.

## Known Limitations

- The script may not bypass CAPTCHAs or advanced anti-bot mechanisms.
- Excessive requests may trigger rate limits or temporary blocking by the target server.
