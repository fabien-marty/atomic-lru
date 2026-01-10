## What is this?

This is a **thread-safe** and **dependency-free** **in-memory** **LRU storage** Python 3.12+ library with optional Time To Live (TTL).

You can define:

- **limits** (`max-items` or `max-size-in-bytes`)
- **TTL expiration** (globally or per item)

to prevent the storage from growing too big.

You will get an automatic **LRU eviction** of the least recently used items when the limits are reached.
