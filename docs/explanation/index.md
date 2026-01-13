# How atomic-lru works internally

This document explains the internal architecture and design decisions of the `atomic-lru` library. It covers how thread-safety is achieved, how LRU eviction works, how TTL expiration is implemented, and the relationship between the high-level `Cache` and low-level `Storage` APIs.

## Architecture overview

The library is organized into two main layers:

1. **Storage layer** (`atomic_lru._storage`): The low-level, thread-safe storage mechanism that handles LRU eviction and TTL expiration. It operates on raw values (typically `bytes` or object pointers) without serialization.

2. **Cache layer** (`atomic_lru._cache`): The high-level API that extends `Storage` to provide automatic serialization and deserialization, allowing you to cache arbitrary Python objects.

This separation allows users to choose the appropriate level of abstraction for their needs: use `Cache` for convenience when serialization is acceptable, or use `Storage` directly when you need to store object references without serialization overhead.

## Thread-safety

All operations in `atomic-lru` are thread-safe through the use of a single `threading.Lock` per storage instance. Every method that accesses or modifies the internal data structures acquires this lock before performing operations.

### Lock acquisition pattern

The lock is acquired using Python's `with` statement, ensuring proper release even if an exception occurs:

```python
with self.__lock:
    # Critical section - thread-safe operations
    value_obj = self._data.get(key)
    # ...
```

This ensures that:
- Only one thread can modify the storage at a time
- Reads and writes are atomic
- The internal state remains consistent across concurrent operations

### Why a single lock?

A single lock simplifies the implementation and ensures complete consistency. While more sophisticated locking strategies (like read-write locks) could potentially improve concurrent read performance, they add complexity and the risk of subtle race conditions. For an in-memory cache where operations are typically fast, a single lock provides excellent safety with minimal overhead.

## LRU eviction mechanism

The Least Recently Used (LRU) eviction policy ensures that when storage limits are reached, the items that haven't been accessed recently are removed first.

### Data structure: OrderedDict

The library uses Python's `collections.OrderedDict` as the primary data structure. `OrderedDict` maintains insertion order, which naturally represents the access order for LRU:

- **Most recently used**: Items at the end of the dictionary
- **Least recently used**: Items at the beginning of the dictionary

### Maintaining LRU order

When an item is accessed via `get()`, it's moved to the end of the `OrderedDict` using `move_to_end()`:

```python
self._data.move_to_end(key)
```

When an item is stored via `set()`, it's added to the end (or moved to the end if it already exists):

```python
self._data[key] = value_obj  # Adds to end if new, or updates existing
```

This ensures that frequently accessed items naturally migrate toward the end, while rarely accessed items accumulate at the beginning.

### Eviction process

When limits are reached (either `max_items` or `size_limit_in_bytes`), the eviction process removes items from the beginning of the `OrderedDict` using `popitem(last=False)`:

```python
_, value_obj = self._data.popitem(last=False)  # Remove from beginning
```

The eviction continues until the storage is within limits. This happens atomically within the lock, ensuring no race conditions during eviction.

### Size tracking

For `size_limit_in_bytes`, the library maintains an approximate size counter (`_size_in_bytes`) that tracks:

- The size of stored values (for `bytes` values)
- Overhead for the `Value` wrapper object
- Overhead for the `OrderedDict` entry (`PER_ITEM_APPROXIMATE_SIZE`)

When items are added, removed, or updated, this counter is adjusted accordingly. The size calculation is approximate because:

- Python object sizes can vary based on implementation details
- The overhead estimates are conservative approximations
- For non-`bytes` values, size tracking returns 0 (size limits only work correctly with `bytes`)

## TTL expiration

Time-to-live (TTL) expiration allows cached items to automatically expire after a specified duration.

### Expiration tracking

Each stored value is wrapped in a `Value` object that includes:

- The actual value
- An optional TTL (time-to-live in seconds)
- An expiration timestamp (`_expire_at`) calculated when the value is created

The expiration timestamp is calculated using `time.perf_counter()`, which provides high-resolution, monotonic timing suitable for measuring durations:

```python
object.__setattr__(self, "_expire_at", time.perf_counter() + self.ttl)
```

### Checking expiration

The `Value.is_expired` property checks if the current time exceeds the expiration timestamp:

```python
@property
def is_expired(self) -> bool:
    return self._expire_at is not None and self._expire_at < time.perf_counter()
```

### Lazy expiration

Expired items are removed lazily in two scenarios:

1. **On access**: When `get()` is called on an expired item, it's immediately deleted and `CACHE_MISS` is returned.

2. **Background cleanup**: A background thread periodically checks for expired items and removes them proactively.

### Background expiration thread

The `ExpirationThread` runs as a daemon thread that periodically checks for expired items. It uses a round-robin approach:

1. Checks a batch of items (up to `max_checks_per_iteration`) starting from a tracked index
2. Calls the `_clean_expired()` method to test and delete expired items
3. Updates the start index for the next iteration
4. Waits for `expiration_thread_delay` seconds before the next iteration

This approach ensures:
- The cleanup work is distributed over time (doesn't block for long periods)
- All items are eventually checked (round-robin through the entire storage)
- The thread can be gracefully stopped when the storage is closed

The thread is created automatically when a `Storage` or `Cache` instance is created (unless `expiration_disabled=True`), and is stopped when `close()` is called.

## Serialization layer

The `Cache` class extends `Storage[bytes]` to provide automatic serialization and deserialization of arbitrary Python objects.

### Serialization protocol

The library uses a protocol-based design (`Serializer` and `Deserializer`) that allows users to provide custom serialization logic. By default, Python's `pickle` module is used, which can serialize most Python objects.

### Serialization flow

When storing a value with `Cache.set()`:

1. The value is serialized to `bytes` using the configured serializer
2. The serialized bytes are stored in the underlying `Storage[bytes]`
3. Size limits are enforced on the serialized bytes

When retrieving a value with `Cache.get()`:

1. The serialized bytes are retrieved from the underlying `Storage[bytes]`
2. The bytes are deserialized back to the original Python object
3. The deserialized object is returned

### Why separate Storage and Cache?

This design provides flexibility:

- **Storage**: Use when you want to store object references directly (no serialization overhead, but no size tracking for non-bytes)
- **Cache**: Use when you need to serialize objects (enables size limits, but adds serialization overhead)

The separation also allows the low-level `Storage` to be used independently when serialization isn't needed, avoiding unnecessary overhead.

## Design decisions and trade-offs

### Why OrderedDict instead of a custom LRU implementation?

Python's `OrderedDict` provides an efficient, well-tested implementation that's optimized for the access patterns needed for LRU. While a custom doubly-linked list implementation could potentially be slightly more memory-efficient, `OrderedDict` offers:

- Proven reliability and performance
- Simple, readable code
- Built-in Python support

### Why approximate size tracking?

Accurately tracking the memory size of arbitrary Python objects is complex and would require:

- Deep introspection of object structures
- Handling of circular references
- Accounting for Python's memory management overhead
- Significant performance overhead

Instead, the library uses approximate tracking that works well for `bytes` values (the primary use case for size limits) while keeping the implementation simple and performant.

### Why a background thread for expiration?

While lazy expiration on access is sufficient for correctness, a background thread provides:

- Proactive cleanup of expired items
- Prevention of memory accumulation from expired but unaccessed items
- Better resource management

The thread is designed to be lightweight and non-blocking, checking items in batches with configurable limits to avoid impacting application performance.

### Why sentinel values instead of exceptions or None?

The library uses sentinel values (`CACHE_MISS`, `DEFAULT_TTL`) instead of exceptions or `None` because:

- **CACHE_MISS**: Allows distinguishing between "key not found" and "key found with value None"
- **DEFAULT_TTL**: Allows distinguishing between "use default TTL", "no TTL", and "use this specific TTL value"

This design provides clearer semantics and avoids ambiguity in the API.

## Memory management

The library is designed to be memory-efficient:

- `Value` objects use `@dataclass(frozen=True, slots=True)` to minimize memory overhead
- Size tracking includes approximations for object overhead
- Items larger than half the size limit are rejected to prevent a single large item from dominating the cache
- Expired items are proactively removed to prevent memory leaks

## Concurrency considerations

While the library is thread-safe, there are some considerations for concurrent usage:

- All operations acquire the same lock, so highly concurrent workloads may experience contention
- The background expiration thread shares the same lock, so expiration checks may briefly delay other operations
- The lock is held for the entire duration of operations, ensuring atomicity but potentially causing brief blocking

For most use cases, these considerations are negligible, but applications with extremely high concurrency requirements should be aware of potential lock contention.

