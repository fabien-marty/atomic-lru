from atomic_lru import CACHE_MISS, Cache

# Create a Cache object instance
# (this object is thread-safe, so you can use it from multiple threads)
cache = Cache(max_items=100, default_ttl=3600)

# Let's store something (a dictionnary here) in the cache with a custom TTL
cache.set("user:123", {"name": "Alice", "age": 30}, ttl=60)

# ...

# Let's retrieve it
user = cache.get("user:123")

if user is not CACHE_MISS:
    # cache hit
    print(user["name"])
