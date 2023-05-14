import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

time1 = time.time()

async def crawl_website(url, session):
    visited_urls = set()
    urls_to_visit = [url]

    while urls_to_visit:
        current_url = urls_to_visit.pop(0)
        visited_urls.add(current_url)

        try:
            async with session.get(current_url) as response:
                if response.status == 200:
                    soup = BeautifulSoup(await response.text(), 'html.parser')

                    # Find all links on the current page
                    links = soup.find_all('a')
                    for link in links:
                        href = link.get('href')
                        absolute_url = urljoin(current_url, href)

                        if absolute_url.startswith(url) and absolute_url not in visited_urls:
                            urls_to_visit.append(absolute_url)
                        #     print(absolute_url)

        except aiohttp.ClientError:
            print(f"Error accessing URL: {current_url}")

        # Introduce a delay between requests
        await asyncio.sleep(.9)
        # save the urls visted in the set to a file
        with open('./sources_table/url_sources.txt', 'a') as f:
                
                for url in visited_urls:
                        print(url)
                        f.write(url + '\n')


async def start_crawling(url):
    async with aiohttp.ClientSession() as session:
        await crawl_website(url, session)

# Run the crawler asynchronously
loop = asyncio.get_event_loop()
loop.run_until_complete(start_crawling('https://linux.die.net/man/'))
loop.close()
print(time.time() - time1)
