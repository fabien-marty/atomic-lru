# Quickstart

## Installation

`pip install atomic-lru` (or equivalent for your package manager)

## High level API *(with automatic serialization/deserialization)*

The main use-case is to use it as a **cache** for your data. You store any kind of data type which will be **automatically serialized** to bytes. [^2]

```python
{% include 'tutorials/highlevel.py' %}
```

## Low level API *(without serialization/deserialization)*

But you can use it at a lower level to store any kind of data type **without serialization**. In that case, you will loose the `max-size-in-bytes` feature but you still get the `max-items` feature.

```python
{% include 'tutorials/lowlevel.py' %}
```
