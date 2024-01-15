from typing import Optional, Any, Dict, Tuple, Callable, get_origin
from datetime import datetime, timedelta
from sqlite3 import connect


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
    _TABLE = "CREATE TABLE IF NOT EXISTS cache(key TEXT PRIMARY KEY, data TEXT, dtype TEXT NOT NULL, exp_t DATETIME);"
    def __init__(self): 
        self.cache = connect(":memory:")
        self.cache.execute(self._TABLE)

    def _get_dtype_func(self, dtype: str) -> Callable:
        type_mapping: Dict[str, Callable[..., Any]] = {
            "dict": dict,
            "str": str,
            "list": list,
            "tuple": tuple,
            "set": set,
            "int": int,
            "float": float,
            "bool": bool,
            "bytes": bytes,
            "bytearray": bytearray,
            "NoneType": type(None)
        }
        func = type_mapping.get(dtype)
        if func is None: raise ValueError(f"Data type is not supported yet: {dtype}")
        return func

    def _get_dtype(self, data: Any) -> str:
        dtype = get_origin(data)
        return dtype.__name__ if dtype else str(dtype)

    def get(self, key) -> Optional[Any]:
        cached_data: Optional[Tuple[str, str, str, datetime]] = self.cache.execute("SELECT * FROM cache WHERE key = ?", [key]).fetchone()
        if cached_data is None: return None
        dtype = self._get_dtype_func(cached_data[2])
        return dtype(cached_data[1]) if cached_data and self.is_valid(cached_data[3]) else None 

    def set(self, key: str, data: Any, expiration_seconds=5) -> None:
        expiration_time = datetime.utcnow() + timedelta(seconds=expiration_seconds)
        self.cache.execute("INSERT INTO cache values (?, ?, ?, ?)", [key, data, data.__name__, expiration_time])

    def is_valid(self, expiration_time: datetime) -> None: return expiration_time and expiration_time > datetime.utcnow()

    def clear(self) -> None: self.cache.executemany(f"DROP TABLE IF EXISTS cache; {self._TABLE}")
