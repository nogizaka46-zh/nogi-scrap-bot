from typing import List, Optional
import asyncio
import aiohttp
import time
import os
import json
from dotenv import load_dotenv
from dataclasses import dataclass, field
from datetime import datetime
import uuid
from config.logger import Logger

load_dotenv()
logger = Logger()


@dataclass
class BlogMeta():
    guid: str
    author: str
    title: str
    link: str
    permalink: str
    date: str


@dataclass
class Cloudflare():
    account_id: str = os.getenv("CLOUDFLARE_ACCOUNT_ID")
    namespace: str = os.getenv("CLOUDFLARE_NAMESPACE_ID")
    email: str = os.getenv("CLOUDFLARE_ACCOUNT_EMAIL")
    token: str = os.getenv("CLOUDFLARE_API_TOKEN")
    headers: dict = field(init=False)
    base_url: str = field(init=False)
    query_limit: Optional[str] = 10
    data: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/storage/kv/namespaces/{self.namespace}"
        self.headers = {
            "X-Auth-Email": os.getenv("CLOUDFLARE_ACCOUNT_EMAIL"),
            "X-Auth-Key": os.getenv("CLOUDFLARE_API_TOKEN"),
            "Content-Type": "application/json"
        }

    def form_payload(self, data) -> None:
        self.data = data

    async def exec_api(self):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            tasks = []
            id = "59d1c9bcb71140039f5dc37d4315d4ab"
            metadata = {
                'created_at': datetime.now(),
                'guid': self.data['guid']
            }
            payload = [{
                'key': str(uuid.uuid4().hex),
                'value': json.dumps(self.data),
                'metadata': json.dumps(metadata, default=str)
            }]
            tasks.append(asyncio.create_task(self.list_kv(session)))
            # tasks.append(asyncio.create_task(self.read_key(session, id)))
            # tasks.append(asyncio.create_task(self.write_key(session, payload)))

            responses = await asyncio.gather(*tasks)
            logger.info(responses)

    async def list_kv(self, session) -> List[dict]:
        url = f"{self.base_url}/keys?limit={self.query_limit}"
        async with session.get(url) as res:
            json_body = await res.json(content_type=None)
            if res.status == 200:
                return json_body

    async def write_key(self, session, payload) -> List[dict]:
        url = f"{self.base_url}/bulk"
        async with session.put(url, json=payload) as res:
            json_body = await res.json(content_type=None)
            if res.status == 200:
                return json_body

    async def read_key(self, session, id) -> List[dict]:
        url = f"{self.base_url}/values/{id}"
        async with session.get(url) as res:
            json_body = await res.json(content_type=None)
            if res.status == 200:
                return json_body


if __name__ == '__main__':
    start = time.perf_counter()
    # dummy data
    data = BlogMeta(
        guid=100794,
        author='5期生リレー',
        title='君を好きになった！！ 一ノ瀬美空',
        link='https://www.nogizaka46.com/s/n46/diary/detail/100683?ima=0211',
        permalink='https://www.nogizaka46.com/s/n46/diary/detail/100683',
        date='Fri, 09 Sep 2022 07:09:09 GMT'
    )
    cf = Cloudflare()
    cf.form_payload(data.__dict__)
    asyncio.run(cf.exec_api())
    logger.info(f"Duration - {round(time.perf_counter() - start, 2)} seconds.")
