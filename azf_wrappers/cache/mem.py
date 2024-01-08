from typing import Optional, Any, Dict
from datetime import datetime, timedelta


class LocalCache:
    def __init__(self): self.cache = {}

    def get(self, key) -> Optional[Any]:
        cached_data = self.cache.get(key, None)
        return cached_data["data"] if cached_data and self.is_valid(cached_data) else None

    def set(self, key, data, expiration_seconds=5) -> None:
        expiration_time = datetime.utcnow() + timedelta(seconds=expiration_seconds)
        self.cache[key] = {"data": data, "expiration_time": expiration_time}

    def is_valid(self, cached_data: Dict) -> None:
        expiration_time = cached_data.get("expiration_time")
        return expiration_time and expiration_time > datetime.utcnow()

    def clear(self) -> None: self.cache = {}
