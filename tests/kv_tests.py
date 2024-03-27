import os, sys

#sys.path.append(os.path.join(os.getcwd(), "..", "azf_wrappers"))
from azf_wrappers.cache import KVDBCache

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
    cache.remove("Hello")
    print(f"WITH VALUES 5: {cache.get('Hello')}")
    del cache
    print("DELETED")
    cache = KVDBCache()
    print(f"WITH VALUES 6: {cache['Hello']}")
    cache["Hello"] = "World!!!!!!"
    print(f"WITH VALUES 7: {cache['Hello']}")
    cache["Hello"] = [1, "world"]
    print(f"WITH VALUES 8: {cache['Hello']}")
    cache["Hello"] = [2, "world 2"]
    print(f"WITH VALUES 9: {cache['Hello']}")
    cache["Hello"] = [9, {"world": "hello"}]
    print(f"WITH VALUES 10: {cache['Hello']}")
    cache.clear()
    cache["Hello"] = (1, "world")
    del cache
