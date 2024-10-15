from typing import List
import redis
import logging
import hashlib
from Levenshtein import distance as levenshtein_distance

SORTED_SET_NAME = 'autocomplete'
HASH_NAME = 'items'

logging.basicConfig(level=logging.DEBUG,
                    format="{asctime} - {levelname} - {message}",
                    style="{",
                    datefmt="%Y-%m-%d %H:%M",)


def add_item(redis_client: redis.Redis, item: str) -> None:
    """
    Add a word to the fuzzy autocomplete system.
    """
    # Generate a unique key for the item
    key = hashlib.sha256(item.lower().encode()).hexdigest()

    # Normalize the item by converting to lowercase and removing non-alphanumeric characters
    normalized_item = ''.join(e for e in item.lower()
                              if e.isalnum() or e.isspace())

    # Split the normalized item into words and remove stop words
    stop_words: Set[str] = {'a', 'an', 'the', 'is', 'of',
                            'in', 'on', 'to', 'and', '&', 'for', 'from', 'with'}
    words = [word for word in normalized_item.split() if word not in stop_words]

    logging.info(f'Adding item: {item} [{key}] :: {words}')

    # Add prefixes of the item to the sorted set for autocomplete
    pipeline = redis_client.pipeline()
    for i in range(1, len(item) + 1):
        prefix = item[:i]
        pipeline.zadd(SORTED_SET_NAME, {prefix: 0})

    # Store the original item in the hash
    pipeline.hset(HASH_NAME, key, item)
    pipeline.hset(HASH_NAME, item, item)
    pipeline.execute()


def get_fuzzy_suggestions(redis_client: redis.Redis, input_word: str, count: int = 5) -> List[str]:
    """
    Get fuzzy autocomplete suggestions for a given input.
    """
    # Fetch all entries in a single call
    all_words = redis_client.zrange(SORTED_SET_NAME, 0, -1)
    all_suggestions = redis_client.hmget(HASH_NAME, all_words)

    # Filter out None values and decode bytes to strings
    all_suggestions = [word.decode()
                       for word in all_suggestions if word is not None]

    # Rank words based on their Levenshtein distance to the input
    suggestions_with_distance = [(word, levenshtein_distance(
        input_word, word)) for word in all_suggestions]
    suggestions_with_distance.sort(key=lambda x: x[1])

    return [word for word, _ in suggestions_with_distance[:count]]


def test_fuzzy_suggestions(redis_client: redis.Redis, word: str) -> None:
    # Get fuzzy autocomplete suggestions
    suggestions = get_fuzzy_suggestions(redis_client, word)
    print(f'{word}: {suggestions}')


# Usage Example
if __name__ == "__main__":
    redis_client = redis.Redis(host='localhost', port=6379, db=0)

    with open('film.lst', 'r') as file:
        for line in file:
            item = line.strip()
            add_item(redis_client, item)

    fruits = ['apple',
              'banana',
              'cherry',
              'date',
              'fig',
              'grape']
    for fruit in fruits:
        add_item(redis_client, fruit)

    things = ['hello',
              'helium',
              'hero',
              'helicopter']
    for thing in things:
        add_item(redis_client, thing)

    test_fuzzy_suggestions(redis_client, 'helo')
