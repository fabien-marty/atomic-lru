## Features

- Thread-Safe
- (optional) TTL expiration *(globally or per item)*
- (optional) Total size limit *(in bytes)* [^1]
- (optional) Max items limit
- Automatic LRU eviction *(when the limits are reached)*
- Full-typing support
- High level `Cache` API **with** automatic serialization/deserialization [^2]
- Low level `Storage` API **without** serialization/deserialization *(store only references to given objects)*
