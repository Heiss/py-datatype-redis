[![Maintainability](https://api.codeclimate.com/v1/badges/9945440b076661b87ccb/maintainability)](https://codeclimate.com/github/Heiss/py-datatype-redis/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/9945440b076661b87ccb/test_coverage)](https://codeclimate.com/github/Heiss/py-datatype-redis/test_coverage)
[![PyPI version](https://badge.fury.io/py/datatype-redis.svg)](https://badge.fury.io/py/datatype-redis)

# Redis for builtin-datatypes

This library implements all builtin datatypes from python3 with a redis backend.

## Status

Work in progress, not usable

## Usage

```python
from datatype_redis import String
foo = String("bar")
```

## Introduction

After a lot of research to backup all my dict and lists to redis to use them in my microservice ecosystem, i was very disappointed about the current situation in the library environment for this purpose. There are a lot of libraries, which handle it, but no one includes everything i need. So i had to implement this by myself. You see here the results.

## Inspiration

This library is heavily inspired by [hot-redis](https://github.com/stephenmcd/hot-redis) and [py-redis-pubsub-dict](https://github.com/Richard-Mathie/py-redis-pubsub-dict).

## Options

In the following, the options of this library will be described.

### Set redis as client

As default, the library use Redis from [redis-py](https://pypi.org/project/redis/) as implementation. If you want to use another implementation, you have to inherit from this class.

If you do not set the client-argument as follows, the library assumes to use a local installation on port 6379.

```python
from datatype_redis import String
foo = String("bar", client={"host":"myremotehost", "port":6379})
```

You can initialize the redis client by yourself, too.

```python
from datatype_redis import String
from redis import Redis
r = Redis(host='myremotehost', port=6379, db=0)
foo = String("bar", client=r)
```

**Beware**: If the client is not compatible with this library, it will raise an `ValueError`.

If you want to use a redisCluster, you can do this with the client-parameter, too.

```python
from rediscluster import RedisCluster
from datatype_redis import String
# Requires at least one node for cluster discovery. Multiple nodes is recommended.
startup_nodes = [{"host": "myremotehost", "port": "7000"}]
foo = String("bar", client=RedisCluster, startup_nodes=startup_nodes)
```

You can overwrite the default behaviour with the following `configure` function.

```python
from datatype_redis import configure
configure(host='myremotehost', port=6380, db=0)
```

Of course, you can use it to set your initialized client as default.

```python
from datatype_redis import configure
from rediscluster import RedisCluster
# Requires at least one node for cluster discovery. Multiple nodes is recommended.
configure(client=RedisCluster, startup_nodes=startup_nodes)
```

**Beware**: If you set host and port and client at the same time, the library will take your client as default and ignore host and port.

You can use any implementation as client you want and set all parameters to configure. The library initialize your implementation with the given parameters for you threadsafe, so you will get a client for each thread you initialize. This behaviour helps to get a better performance in webservers etc.

### Redis key

Redis is a key-value-store, so it needs a key to store the values. To reduce the typing, you can use the default behaviour of this library, which uses unique identifier as keys. You can get the key with the `get_redis_key`-method to any datatype.

But if you want to use this library in a microservice, which should be duplicated over your cluster, this behaviour would be toxic to your implementation, so you can use the `key`-parameter to set an identifier.

```python
from datatype_redis import String
foo_uuid = String("bar")
foo_key = String("bar", key="foo")

print(foo_uuid) # expect: "bar"
print(foo_uuid.get_redis_key()) # expect: similar to "12345678-1234-5678-1234-567812345678"

print(foo_key) # expect: "bar"
print(foo_key.get_redis_key()) # expect: "foo"
```

If you query the uuid as key in your redis installation, you will not get the serialization of your data as you would expected, because this library uses a prefix per default to work with a big redis installation and to not interfere with any other implementations. You can get the key with prefix with `get_redis_key_full`-method and set this prefix in `configure`. The default value for prefix is `datatype-redis`.

```python
from datatype_redis import configure
foo_uuid = String("bar", key="fooKey")
print(foo_uuid.get_redis_key_full()) # expect: "datatype-redis/fooKey"
print(foo_uuid) # expect: "bar"
configure(prefix="fooPrefix")
print(foo_uuid.get_redis_key_full()) # expect: "fooPrefix/fooKey"
print(foo_uuid) # expect: "bar"
```

**Beware**: If you change your prefix, while you initialized a datatype, the library will rename all keys automatically with a matching filter. This will take some time on larger redis installations.

If you want to get the current prefix as string, you can call the `get_prefix`-method.

```python
from datatype_redis import get_prefix
print(get_prefix()) # expect default: "datatype-redis"
```

### Rename key

If you want to store your value in another key, you can do that with the `rename`-method.

```python
from datatype_redis import configure
foo_uuid = String("bar", key="fooKey")
print(foo_uuid.get_redis_key_full()) # expect: "datatype-redis/fooKey"
foo_uuid.rename("barKey")
print(foo_uuid.get_redis_key_full()) # expect: "datatype-redis/barKey"
```

### Msgpack as serializer

If you want to store complex datatypes (like dict or list) in redis, you need to use a serializer. This library use [msgpack](https://pypi.org/project/msgpack/) for this purpose. If you want to use another implementation, your implementation needs a `dumps` and `loads` method.

The constructor of any datatype take your implementation with `serializer`-key.

Example (use json as serializer):

```python
from datatype_redis import String
import json

foo = String("foo", serializer=json)
```

**Beware**: If you want to use nested datatypes with redis backend from this library, you should use uuid-keys. Otherwise you could overwrite existing keys and your implementation does not work as you would expect.

### PubSub Backend

If you need to get your results ASAP, but you change them rarely, you should take a look at the pubsub-cache implementation. This will reduce the latency for get-requests drastically, but you will get every problem with caches.

If you want to set a cache to an atomic datatype like String or Int, you can use the `PubSubCacheAtomic` class. You have to initialize a cache to store the values. Also, you have to use a specialized implementation of the corresponding datatype, called `PubSub*`. See the following example.

```python
from datatype_redis import PubSubCacheAtomic, PubSubString
from pylru import lrucache

cache = lrucache(1)
store = PubSubString("foo")
redcache = PubSubCacheAtomic(store, cache)
```

The following table shows the PubSub classes of each atomic datatype.

| atomic | PubSub       |
| ------ | ------------ |
| Bool   | PubSubBool   |
| String | PubSubString |
| Int    | PubSubInt    |
| Float  | PubSubFloat  |
 
For complex datatypes (called datastructure) like Dict or List, you have to use the correspondig `PubSubCache*` classes (Do not use the `PubSubCacheAtomic` class for datastructures).

| datastructure | PubSubCache*    |
| ------------- | --------------- |
| Dict          | PubSubCacheDict |
| List          | PubSubCacheList |

You use them as follows.

```python
from datatype_redis import PubSubCacheDict, PubSubDict
from pylru import lrucache

cache = lrucache(10)
store = PubSubDict()
redcache = PubSubCacheDict(store, cache)
```

## Examples and Demonstrations

### Text Type
#### Strings

```python
from datatype_redis import String

foo = String("bar")
print(foo) # expect: "bar"
foo += "foo"
print(foo) # expect: "barfoo"
```

### Numeric Types
#### Integer

```python
from datatype_redis import Int

foo = Int(3)
print(foo) # expect: "3"
foo += 7
print(foo) # expect: "10"
foo -= 11
print(foo) # expect: "-1"
```

#### Float

```python
from datatype_redis import Float

foo = Float(3.4)
print(foo) # expect: "3.4"
foo += 7
print(foo) # expect: "10.4"
foo -= 11
print(foo) # expect: "-0.6"
```

#### Complex

### Sequence Types
#### List

```python
from datatype_redis import List

foo = List()
print(foo) # expect: []
foo.append("foo")
print(foo) # expect: ["foo"]
("foo" in foo) # expect: True
foo = List(["bar"])
print(foo) # expect: ["bar"]
("foo" in foo) # expect: False
```

#### Tuple

#### Range

### Mapping Type
#### Dict

```python
from datatype_redis import Dict

foo = Dict()
print(foo) # expect: {}
foo["foo"] = "bar
print(foo["foo"]) # expect: "bar"
print(foo["bar"]) # expect: raise KeyError
print(foo) # expect: {"foo":"bar"}
print(foo.items()) # expect: [("foo", "bar")]
print(foo.values()) # expect: [("bar")]
print(foo.keys()) # expect: [("foo")]
foo["bar"] = [1,2,3]
print(foo["bar"]) # expect: [1,2,3]
print(foo) # expect: {"foo":"bar", "bar":[1,2,3]}
```

### Set Types
#### Set
#### Frozen Set

### Boolean Type
#### bool

### Binary Types
#### Bytes
#### Bytearray
#### MemoryView

## Microservices

The main purpose of this library is to use in a microservice ecosystem like a container in kubernetes. You have to run a redis instance in your cloud, configure your client with `configure()` for this library, so your microservice use redis as backend for your datatypes. This will make your values available on all your microservice implementations with same keys.

For redis in kubernetes, you should use a helm chart e.g. [redis-ha](https://github.com/DandyDeveloper/charts/tree/master/charts/redis-ha).
