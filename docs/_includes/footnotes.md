[^1]: When using the low level `Storage` API, values must be of type `bytes` for size tracking to work. The high level `Cache` API handles this automatically.
[^2]: By default, `pickle` is used for serialization/deserialization but you can provide your own serializer/deserializer if you want to use a different format.
