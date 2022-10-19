import asyncio
import aiohttp
import time
# from typing import List
from lxml import etree as et
from io import StringIO

from config.logger import Logger
from config.data import DataLoader


logger = Logger()
config = DataLoader().load_data()

"""test block starts"""
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Dnt": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
}


async def scrape_data(session, url: str) -> None:
    result = []
    async with session.request('GET', url) as response:
        text = await response.text()
        if response.status == 200:
            root = et.XML(bytes(text, encoding='utf8'))
            tree = et.ElementTree(root)
            author = tree.xpath('//author/text()')
            print("author", author)
            # [result.append(html.tostring(title)) for title in blog_titles]
    print(result)


def create_task_queue(session):
    tasks = []
    for url in config["urls"]:
        tasks.append(asyncio.create_task(scrape_data(session, url)))
    return tasks


async def exec():
    async with aiohttp.ClientSession() as session:
        tasks = create_task_queue(session)
        responses = await asyncio.gather(*tasks)
        [logger.info(item) for item in responses]


if __name__ == '__main__':
    start = time.perf_counter()
    asyncio.run(exec())
    logger.info(f"Duration - {round(time.perf_counter() - start, 2)} seconds.")
