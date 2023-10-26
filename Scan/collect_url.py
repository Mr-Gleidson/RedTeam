# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import time

requests.packages.urllib3.disable_warnings()

def get_http_banner(url):
    try:
        user_agent_list = [
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
        ]
        
        session = requests.Session()
        session.keep_alive = False  # Close idle connections

        # Try HTTP first
        response = session.get('http://' + url,
            headers={'User-Agent': random.choice(user_agent_list), 'Accept-Language': 'zh-CN,zh;q=0.9'},
            timeout=1, verify=False, allow_redirects=True)

        if response.status_code == 400:
            # If you cannot get an HTTP response, try HTTPS
            response = session.get('https://' + url,
                headers={'User-Agent': random.choice(user_agent_list), 'Accept-Language': 'zh-CN,zh;q=0.9'},
                timeout=1, verify=False, allow_redirects=True)

        encoding = response.encoding
        soup = BeautifulSoup(response.text.encode(encoding).decode('utf-8'), 'html.parser')

        title = "Title could not be found!"
        if soup.title is not None:
            title = soup.title.text.strip('\n').strip()

        return [url, title, response.status_code]

    except Exception as ex:
        return [url, str(ex), -1]  # Exception handling

def out_to_csv(data):
    with open('out.csv', 'a', encoding='utf-8-sig') as f:
        f.write('"' + '","'.join(map(str, data)) + '"\n')

def main():
    with open('url.txt', 'r') as f:
        out_to_csv(["URL", "Title", "Status Code"])

        with ThreadPoolExecutor(max_workers=100) as executor:
            future_to_url = {executor.submit(get_http_banner, url.strip()): url.strip() for url in f}

            for future in as_completed(future_to_url):
                data = future.result()
                out_to_csv(data)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print('[INFO] Tempo decorrido: %s segundos' % (time.time() - start_time))