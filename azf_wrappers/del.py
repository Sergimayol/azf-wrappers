from cache import KVDBCache

if __name__ == "__main__":
    cache = KVDBCache()
    print(f"NOTHING: {cache.get('Hello')}")
    cache.set("Hello", "World!!!!!!")
    print(f"WITH VALUES 1: {cache.get('Hello')}")
    cache.set("Hello", [1, "world"])
    print(f"WITH VALUES 2: {cache.get('Hello')}")
    cache.set("Hello", [2, "world 2"])
    print(f"WITH VALUES 3: {cache.get('Hello')}")
    cache.set("Hello", [9, {"world": "hello"}])
    print(f"WITH VALUES 4: {cache.get('Hello')}")
    cache.clear()
    cache.set("Hello", (1, "world"))
    del cache
