# Readme #

## Run Docker ##

```
docker run -d --rm --name redis-local -p 6379:6379 redis
```

if you want show the log you can use this command

```
docker logs -f redis-local
```

A different option is up docker and dont put it in background getting the log

```
docker run --rm --name redis-local -p 6379:6379 redis
```

## References ##

- **Antirez** (<http://oldblog.antirez.com/post/autocomplete-with-redis.html>)
- (<https://patshaughnessy.net/2011/11/29/two-ways-of-using-redis-to-build-a-nosql-autocomplete-search-index>)
