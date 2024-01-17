from typing import Optional, Any, Dict, Tuple, Callable
from datetime import datetime, timedelta
from sqlite3 import connect, Binary
from pickle import dumps, loads


class KVMapCache:
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

class KVDBCache:
    _TABLE = "CREATE TABLE IF NOT EXISTS cache(key TEXT PRIMARY KEY, data BLOB, dtype TEXT NOT NULL, exp_t DATETIME);"
    def __init__(self): 
        self.cache = connect(":memory:")
        self.cache.execute(self._TABLE)

    def _get_dtype(self, data: Any) -> str: return type(data).__name__

    def get(self, key) -> Optional[Any]:
        cached_data: Optional[Tuple[str, str, str, datetime]] = self.cache.execute("SELECT * FROM cache WHERE key = ?", [key]).fetchone()
        if cached_data is None: return None
        return loads(cached_data[1]) if cached_data and self.is_valid(datetime.strptime(cached_data[3], "%Y-%m-%d %H:%M:%S.%f")) else None 

    def set(self, key: str, data: Any, expiration_seconds=5) -> None:
        expiration_time = datetime.utcnow() + timedelta(seconds=expiration_seconds)
        self.cache.execute("INSERT OR REPLACE INTO cache values (?, ?, ?, ?)", [key, Binary(dumps(data)), self._get_dtype(data), expiration_time])

    def is_valid(self, expiration_time: datetime) -> None: return expiration_time and expiration_time > datetime.utcnow()

    def clear(self) -> None: self.cache.executescript(f"DROP TABLE IF EXISTS cache; {self._TABLE}")

    def __del__(self) -> None: self.cache.close()
