from bs4 import BeautifulSoup
from urllib.parse import urlparse
from time import sleep
import os, requests, hashlib, random

def proxy_dict(proxy):
    return { 'http':f'http://{proxy}', 'https':f'http://{proxy}' }

def visit_uri(uri, session, wait_element=None, return_soup=True, print_visits=True, sleep_after_visit=True):
    res = session.get(uri, timeout=5)
    res.raise_for_status()
    sleep(random.uniform(0.05, 2)) if sleep_after_visit else None
    soup = BeautifulSoup(res.content, features="lxml")
    if wait_element:
        assert len(soup.select(wait_element)) > 0, 'ElementNotFound'
    print(res.status_code, to_digest(uri), end='\r') if print_visits else None
    return soup if return_soup else res.text.strip()

def verify_session_proxy(session):
    opts = { 'return_soup':False, 'print_visits':False, 'sleep_after_visit':False }
    proxy = visit_uri('https://wtfismyip.com/text', session, **opts)
    assert proxy in session.proxies['http']
    print('Proxy IP: OK')

def to_digest(url):
    m = hashlib.md5()
    m.update(url.encode('utf-8'))
    return m.hexdigest()

def cache_location(url):
    file_name = to_digest(url) + '.html'
    cache_dir = '/'.join(['cache', urlparse(url).hostname])
    return (cache_dir, file_name)

def validate_and_cache_page(session, url, wait_element):
    cache_dir, file_name = cache_location(url)
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    cache_path = cache_dir + '/' + file_name
    if os.path.exists(cache_path):
        print('<C>', file_name, end='\r')
        with open(cache_path, 'r') as file:
            soup = BeautifulSoup(file.read(), features="lxml")
    else:
        soup = visit_uri(url, session, wait_element=wait_element)
        with open(cache_path, 'w') as file:
            file.write(soup.encode().decode('utf-8'))
    return soup