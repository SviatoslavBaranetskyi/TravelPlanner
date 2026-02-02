import os
import asyncio
from typing import List, Optional
import httpx
from functools import lru_cache

from app.core.constants import DEFAULT_TIMEOUT
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")

class ArtInstituteClient:
    def __init__(self):
        self.client = httpx.Client(timeout=DEFAULT_TIMEOUT)
        self._cache = {}

    def validate_place_exists(self, external_id: str) -> bool:
        if external_id in self._cache:
            return self._cache[external_id]

        try:
            resp = self.client.get(f"{API_URL}/{external_id}")
            exists = resp.status_code == 200
        except httpx.RequestError:
            exists = False

        self._cache[external_id] = exists
        return exists

    def get_places_by_ids(self, ids: List[str]) -> List[dict]:
        results = []

        def fetch(external_id: str):
            if external_id in self._cache and self._cache[external_id]:
                return self._cached_response(external_id)
            try:
                resp = self.client.get(f"{API_URL}/{external_id}")
                if resp.status_code == 200:
                    data = resp.json()
                    self._cache[external_id] = True
                    return data
                else:
                    self._cache[external_id] = False
            except httpx.RequestError:
                self._cache[external_id] = False

        tasks = [fetch(eid) for eid in ids]
        fetched = asyncio.gather(*tasks, return_exceptions=True)
        for item in fetched:
            if isinstance(item, dict):
                results.append(item)

        return results

    def _cached_response(self, external_id: str) -> Optional[dict]:
        resp = self.client.get(f"{API_URL}/{external_id}")
        if resp.status_code == 200:
            return resp.json()
        return None

    def close(self):
        self.client.close()


artic_client = ArtInstituteClient()
