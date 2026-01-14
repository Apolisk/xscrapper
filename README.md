## Description

This project automates tweet retrieval from Twitter without using browser automation.  
It sends HTTP requests, processes the response data, and writes each tweet to a new line in an output file.

## Dependencies

- Python 3.8+
- `pip install -r requirements.txt`

## Parameters
The script accepts the following parameters via the command line:

```username```
- Type: str
- Default: elonmusk

```count```
- Type: int
- Default: 10

```proxy```
- Type: str
- Default: None 
- Format: ```http://<ip>:<port>```

## Usage

#### Example #1 (using defalut params)
```python
python3 twitter_scanario.py 
```

#### Example #2 (specify own params)
```python
python3 twitter_scanario.py --username BRICSinfo --count 20 --proxy http://127.0.0.1:8080
```

## Known Limitations

- The script may not bypass CAPTCHAs or advanced anti-bot mechanisms.
- Excessive requests may trigger rate limits or temporary blocking by the target server.
