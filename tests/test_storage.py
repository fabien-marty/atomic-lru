import random
import time

import pytest

from atomic_lru import CACHE_MISS, CacheMissSentinel, DefaultTTLSentinel, Storage
from atomic_lru._storage.storage import PER_ITEM_APPROXIMATE_SIZE
from atomic_lru._storage.value import OBJECT_SIZE_APPROXIMATE_SIZE, Value


def test_value():
    # Test basic Value creation
    value = Value(value=b"test", ttl=None)
    assert value.value == b"test"
    assert value.ttl is None
    assert value._expire_at is None
    assert not value.is_expired

    # Test Value with negative TTL
    with pytest.raises(ValueError):
        Value(value=b"test", ttl=-1)

    # Test Value with TTL
    value_with_ttl = Value(value=b"test", ttl=5)
    assert value_with_ttl.value == b"test"
    assert value_with_ttl.ttl == 5
    assert value_with_ttl._expire_at is not None
    assert value_with_ttl._expire_at > time.perf_counter()
    assert not value_with_ttl.is_expired

    # Test expired value
    expired_value = Value(value=b"test", ttl=0)
    time.sleep(0.001)  # Small delay to ensure expiration
    assert expired_value.is_expired

    # Test size calculation
    small_value = Value(value=b"a")
    large_value = Value(value=b"a" * 100)
    assert large_value.size_in_bytes > small_value.size_in_bytes
    assert small_value.size_in_bytes == OBJECT_SIZE_APPROXIMATE_SIZE + 1
    assert large_value.size_in_bytes == OBJECT_SIZE_APPROXIMATE_SIZE + 100


def test_storage_basic():
    storage = Storage[bytes](
        size_limit_in_bytes=4096,
        max_items=100,
        default_ttl=1,
        expiration_thread_delay=0.1,
        expiration_thread_max_checks_per_iteration=1_000_000,
    )
    assert storage.size_in_bytes > 0
    initial_size = storage.size_in_bytes
    assert storage.number_of_items == 0

    storage.set("key1", b"v1")
    assert (
        storage.size_in_bytes
        == initial_size
        + OBJECT_SIZE_APPROXIMATE_SIZE
        + len(b"v1")
        + PER_ITEM_APPROXIMATE_SIZE
    )
    assert storage.number_of_items == 1

    storage.set("key2", b"value2")
    assert (
        storage.size_in_bytes
        == initial_size
        + OBJECT_SIZE_APPROXIMATE_SIZE
        + len(b"v1")
        + OBJECT_SIZE_APPROXIMATE_SIZE
        + len(b"value2")
        + 2 * PER_ITEM_APPROXIMATE_SIZE
    )
    assert storage.number_of_items == 2

    storage.delete("key2")
    assert (
        storage.size_in_bytes
        == initial_size
        + OBJECT_SIZE_APPROXIMATE_SIZE
        + len(b"v1")
        + PER_ITEM_APPROXIMATE_SIZE
    )
    assert storage.number_of_items == 1

    assert storage.get("key2") is CACHE_MISS
    assert storage.get("key1") == b"v1"

    checked, deleted = storage._clean_expired()
    assert checked == 1
    assert deleted == 0
    assert storage.get("key1") == b"v1"

    storage.set("key1", b"v1")
    assert storage.get("key1") == b"v1"

    storage.set("key1", b"v1.updated")
    assert storage.get("key1") == b"v1.updated"

    before = time.perf_counter()
    storage.close(wait=True)
    assert time.perf_counter() - before < 0.5

    before = time.perf_counter()
    storage.close(wait=True)  # should do nothing
    assert time.perf_counter() - before < 0.1

    # we can still get the value
    assert storage.get("key1") == b"v1.updated"

    # but we can't set new values
    with pytest.raises(RuntimeError):
        storage.set("key2", b"v2")


def test_storage_expiration_manual():
    storage = Storage[bytes](
        size_limit_in_bytes=None,
        max_items=100,
        default_ttl=0.1,
        expiration_thread_delay=0.01,
        expiration_thread_max_checks_per_iteration=0,  # no expiration thread
    )

    for i in range(100):
        storage.set(f"key{i}", b"v")

    assert storage.number_of_items == 100

    time.sleep(0.2)

    checked, deleted = storage._clean_expired(start=0, stop=10)
    assert checked == 10
    assert deleted == 10
    assert storage.number_of_items == 90

    checked, deleted = storage._clean_expired(start=0, stop=10)
    assert checked == 10
    assert deleted == 10
    assert storage.number_of_items == 80

    storage.set("new", b"new")

    checked, deleted = storage._clean_expired()
    assert checked == 81
    assert deleted == 80
    storage.close()


def test_storage_expiration_thread():
    storage = Storage[bytes](
        size_limit_in_bytes=None,
        max_items=1000,
        default_ttl=60.0,  # note: won't be used because we set a lower TTL at item level
        expiration_thread_delay=0.01,
        expiration_thread_max_checks_per_iteration=10,
        expiration_thread_log=True,
    )

    for i in range(100):
        storage.set(f"key{i}", b"v", ttl=0.1)

    assert storage.number_of_items == 100

    storage.set("new", b"new", ttl=60)  # should not be expired

    time.sleep(0.5)  # enough time for the expiration thread to run

    assert storage.number_of_items == 1
    assert storage.get("new") == b"new"

    storage.close()


def test_storage_too_many_items():
    storage = Storage[bytes](size_limit_in_bytes=None, max_items=11, default_ttl=None)

    for i in range(100):
        storage.set(f"key{i}", f"v{i}".encode())
        for j in range(i):
            if j % 10 == 0:
                # Let's make some traffic on these keys (%10==0)
                # to test the LRU behavior
                assert storage.get(f"key{j}") == f"v{j}".encode()

    assert storage.number_of_items == 11

    for i in range(100):
        if i % 10 == 0:
            # These keys should be still in the storage (thanks to the LRU behavior)
            assert storage.get(f"key{i}") == f"v{i}".encode()
    storage.close()


def test_storage_various():
    x = DefaultTTLSentinel()
    assert str(x) == "<DefaultTTL>"
    y = CacheMissSentinel()
    assert str(y) == "<CacheMiss>"

    storage = Storage[bytes](expiration_thread_max_checks_per_iteration=0)
    assert (
        storage.delete("key1") is False
    )  # delete a non-existing key should do nothing

    storage.set("key1", b"v1", ttl=0.01)

    time.sleep(0.1)

    # Get an expired key should return CACHE_MISS
    assert storage.get("key1") is CACHE_MISS
    storage.close()


def test_storage_delete_return_value():
    storage = Storage[bytes](expiration_thread_max_checks_per_iteration=0)
    storage.set("key1", b"v1")
    assert storage.delete("key1") is True
    assert storage.delete("key1") is False
    storage.close()


def test_non_bytes_storage():
    storage = Storage[int](
        size_limit_in_bytes=None,
    )
    storage.set("key1", 1)
    assert storage.get("key1") == 1
    storage.close()


def test_no_expiration_storage():
    storage = Storage[int](
        size_limit_in_bytes=None,
        expiration_disabled=True,
    )
    storage.set("key1", 1)
    assert storage.get("key1") == 1
    assert storage._clean_expired() == (0, 0)
    storage.close()


def test_max_size_limit():
    storage = Storage[bytes](size_limit_in_bytes=4096, max_items=100)
    storage.set("key", b"v" * 3000)

    # as the value is bigger than size_limit_in_bytes/2
    assert storage.get("key") is CACHE_MISS

    for i in range(10_000):
        size = random.randint(1, 100)  # noqa: S311
        storage.set(f"key{i}", b"v" * size)

    assert storage.number_of_items > 10
    assert storage.size_in_bytes > 3500
    assert storage.size_in_bytes < 4096
    storage.close()


def test_overwrite_existing_key_size_tracking():
    """Test that overwriting an existing key correctly updates size tracking."""
    storage = Storage[bytes](
        size_limit_in_bytes=4096,
        max_items=100,
        expiration_thread_max_checks_per_iteration=0,
    )
    initial_size = storage.size_in_bytes

    # Set a key with a small value
    small_value = b"small"
    storage.set("key1", small_value)
    size_after_small = storage.size_in_bytes
    expected_size_after_small = (
        initial_size
        + OBJECT_SIZE_APPROXIMATE_SIZE
        + len(small_value)
        + PER_ITEM_APPROXIMATE_SIZE
    )
    assert size_after_small == expected_size_after_small

    # Overwrite the same key with a larger value
    large_value = b"x" * 100
    storage.set("key1", large_value)
    size_after_large = storage.size_in_bytes
    # When overwriting, old size is subtracted, then new size is added
    # Net change: (new_value_size - old_value_size)
    expected_size_after_large = (
        initial_size
        + OBJECT_SIZE_APPROXIMATE_SIZE
        + len(large_value)
        + PER_ITEM_APPROXIMATE_SIZE
    )
    assert size_after_large == expected_size_after_large
    assert storage.number_of_items == 1  # Still only one item

    # Overwrite again with a smaller value
    medium_value = b"medium"
    storage.set("key1", medium_value)
    size_after_medium = storage.size_in_bytes
    expected_size_after_medium = (
        initial_size
        + OBJECT_SIZE_APPROXIMATE_SIZE
        + len(medium_value)
        + PER_ITEM_APPROXIMATE_SIZE
    )
    assert size_after_medium == expected_size_after_medium
    assert storage.number_of_items == 1

    # Verify the value is correct
    assert storage.get("key1") == medium_value

    storage.close()


def test_clear():
    """Test that clear() removes all items and resets size tracking."""
    storage = Storage[bytes](
        size_limit_in_bytes=4096,
        max_items=100,
        expiration_thread_max_checks_per_iteration=0,
    )
    initial_size = storage.size_in_bytes
    assert storage.number_of_items == 0

    # Clear empty cache should work
    storage.clear()
    assert storage.number_of_items == 0
    assert storage.size_in_bytes == initial_size

    # Add some items
    storage.set("key1", b"value1")
    storage.set("key2", b"value2")
    storage.set("key3", b"value3")
    assert storage.number_of_items == 3
    assert storage.size_in_bytes > initial_size

    # Verify items exist
    assert storage.get("key1") == b"value1"
    assert storage.get("key2") == b"value2"
    assert storage.get("key3") == b"value3"

    # Clear the cache
    storage.clear()
    assert storage.number_of_items == 0
    assert storage.size_in_bytes == initial_size

    # Verify items are gone
    assert storage.get("key1") is CACHE_MISS
    assert storage.get("key2") is CACHE_MISS
    assert storage.get("key3") is CACHE_MISS

    # Can add items after clearing
    storage.set("key4", b"value4")
    assert storage.number_of_items == 1
    assert storage.get("key4") == b"value4"

    storage.close()


def test_clear_closed_storage():
    """Test that clear() raises RuntimeError when storage is closed."""
    storage = Storage[bytes](
        size_limit_in_bytes=4096,
        max_items=100,
        expiration_thread_max_checks_per_iteration=0,
    )
    storage.set("key1", b"value1")
    storage.close()

    with pytest.raises(RuntimeError, match="Storage is closed"):
        storage.clear()


def test_overwrite_existing_key_updates_lru_position():
    """Overwriting a key via set() should move it to the most recently used position."""
    storage = Storage[bytes](size_limit_in_bytes=None, max_items=3)

    storage.set("a", b"a")
    storage.set("b", b"b")
    storage.set("c", b"c")

    # Overwrite "a" — it should now be the most recently used
    storage.set("a", b"a2")

    # Adding "d" must evict "b" (oldest), not "a"
    storage.set("d", b"d")

    assert storage.get("a") == b"a2"  # should still be present
    assert storage.get("b") is CACHE_MISS  # evicted (LRU)
    assert storage.get("c") == b"c"
    assert storage.get("d") == b"d"

    storage.close()


def test_overwrite_existing_key_updates_lru_position_with_multiple_overwrites():
    """Multiple set() overwrites correctly track the least recently used key."""
    storage = Storage[bytes](size_limit_in_bytes=None, max_items=3)

    storage.set("a", b"a")
    storage.set("b", b"b")
    storage.set("c", b"c")

    # Overwrite "b" then "a" — "c" becomes the oldest
    storage.set("b", b"b2")
    storage.set("a", b"a2")

    # Adding "d" must evict "c" (actual LRU)
    storage.set("d", b"d")

    assert storage.get("a") == b"a2"
    assert storage.get("b") == b"b2"
    assert storage.get("c") is CACHE_MISS  # evicted (LRU)
    assert storage.get("d") == b"d"

    storage.close()


def test_storage_invalid_parameters():
    """Test that invalid constructor parameters raise ValueError with clear messages."""
    with pytest.raises(ValueError, match="max_items must be at least 1"):
        Storage[bytes](max_items=0)

    with pytest.raises(ValueError, match="max_items must be at least 1"):
        Storage[bytes](max_items=-5)

    with pytest.raises(ValueError, match="default_ttl cannot be negative"):
        Storage[bytes](default_ttl=-1.0)

    with pytest.raises(ValueError, match="expiration_thread_delay must be positive"):
        Storage[bytes](expiration_thread_delay=0)

    with pytest.raises(ValueError, match="expiration_thread_delay must be positive"):
        Storage[bytes](expiration_thread_delay=-1.0)

    with pytest.raises(
        ValueError,
        match="expiration_thread_max_checks_per_iteration cannot be negative",
    ):
        Storage[bytes](expiration_thread_max_checks_per_iteration=-1)


def test_overwrite_lru_item_size_tracking():
    """Size tracking stays correct when set() overwrites a key that gets evicted as the LRU item.

    Scenario: "A" is the LRU item. Calling set("A", larger_value) triggers eviction which
    pops "A" itself (the LRU). The subsequent size accounting must treat the store as a fresh
    insert, not an overwrite, to avoid double-subtracting the old size.
    """
    small_value = b"X" * 2000
    large_value = b"Y" * 2100

    small_value_obj = Value(value=small_value, ttl=None)
    large_value_obj = Value(value=large_value, ttl=None)
    item_total_small = small_value_obj.size_in_bytes + PER_ITEM_APPROXIMATE_SIZE
    item_total_large = large_value_obj.size_in_bytes + PER_ITEM_APPROXIMATE_SIZE

    # The storage starts with an OrderedDict overhead baked into _size_in_bytes.
    # Use a throw-away storage instance to measure the initial overhead so we can
    # set size_limit tightly enough that overwriting "A" triggers eviction of "A" itself.
    _probe = Storage[bytes](size_limit_in_bytes=4096)
    initial_overhead = _probe.size_in_bytes
    _probe.close()

    # Size limit that fits exactly the initial overhead plus two small items.
    size_limit = initial_overhead + item_total_small * 2
    assert size_limit >= 4096, "size_limit must meet the Storage minimum"
    # large_value raw length must not exceed size_limit / 2 or Storage silently drops it
    assert len(large_value) <= size_limit / 2

    storage = Storage[bytes](size_limit_in_bytes=size_limit)

    # Insert "A" first (it becomes the LRU), then "B"
    storage.set("A", small_value)
    storage.set("B", small_value)
    assert storage.size_in_bytes == size_limit

    # Overwrite "A" with a larger value — eviction will pop "A" (the LRU) to make room,
    # then re-insert it as a fresh entry with the new value
    storage.set("A", large_value)

    # "A" must be retrievable with the new value
    assert storage.get("A") == large_value

    # "B" should still be present (it was not the LRU)
    assert storage.get("B") == small_value

    # Size must reflect the initial overhead plus one small item ("B") and one large item ("A")
    expected_size = initial_overhead + item_total_small + item_total_large
    assert storage.size_in_bytes == expected_size

    storage.close()
