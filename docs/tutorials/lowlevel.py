from atomic_lru import CACHE_MISS, Storage


class ExpensiveObject:
    """An expensive object that is not serializable."""

    pass


# Create a Storage object instance to store ExpensiveObject instances
# (this object is thread-safe, so you can use it from multiple threads)
storage = Storage[ExpensiveObject](max_items=100, default_ttl=3600)

# Create and store an ExpensiveObject instance
value = ExpensiveObject()
storage.set("key1", value, ttl=60)

# ...

# Let's retrieve it
obj = storage.get("key1")

if obj is not CACHE_MISS:
    # cache hit
    assert isinstance(obj, ExpensiveObject)
    assert id(obj) == id(value)  # this is the same object instance
