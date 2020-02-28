from urllib.parse import urlencode, quote
from time import sleep
from dotenv import load_dotenv
import json, os, requests

load_dotenv()

def detect_language(text):
    if len(text) > 999: # if text is over 1,000 char limit, truncate!
        text = ' '.join(long[:999].split(' ')[:-1])
    base_api = 'http://api.languagelayer.com/detect?'
    payload = urlencode({
        'access_key': os.getenv("LL_KEY"),
        'query': text
    }, quote_via=quote)
    res = requests.get(base_api + payload)
    res.raise_for_status()
    api_res = json.loads(res.text)
    sleep(3.2) # sleep to avoid hitting api rate-limit
    if api_res['success']:
        return [v[1] for v in api_res['results'][0].items()]
    else:
        return ['', 'API_ERROR_' + str(api_res['error']['code']), 0, 0, False]