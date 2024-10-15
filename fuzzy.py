import redis

# Initialize Redis client
redis_client = redis.Redis(host='localhost', port=6379, db=0)

SORTED_SET_NAME = 'fuzzy_autocomplete'
HASH_NAME = 'fuzzy_autocomplete_hash'


def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def add_entry(redis_client, new_entry):
    """
    Add a word to the fuzzy autocomplete system.
    """

    for i in range(1, len(new_entry) + 1):
        prefix = new_entry[:i]
        redis_client.zadd(SORTED_SET_NAME, {prefix: 0})
    redis_client.hset(HASH_NAME, new_entry, new_entry)


def get_fuzzy_suggestions(redis_client, input_word, count=5):
    """
    Get fuzzy autocomplete suggestions for a given input.
    """
    # Fetch all entries, since we don't have direct fuzzy support
    all_suggestions = []
    for word in redis_client.zrange(SORTED_SET_NAME, 0, -1):
        fetched_word = redis_client.hget(HASH_NAME, word)
        if fetched_word is not None:
            all_suggestions.append(fetched_word.decode())

    # Rank words based on their Levenshtein distance to the input
    suggestions_with_distance = [(word, levenshtein_distance(
        input_word, word)) for word in all_suggestions]
    suggestions_with_distance.sort(key=lambda x: x[1])

    return [word for word, _ in suggestions_with_distance[:count]]


def test_fuzzy_suggestions(word):
    # Get fuzzy autocomplete suggestions
    suggestions = get_fuzzy_suggestions(
        redis_client, word)  # Intentional typo
    print(f'{word}: {suggestions}')


# Usage Example
if __name__ == "__main__":
    # Add some example entries
    add_entry(redis_client, "hello")
    add_entry(redis_client, "helium")
    add_entry(redis_client, "hero")
    add_entry(redis_client, "helicopter")
    add_entry(redis_client, "hebra")
    add_entry(redis_client, "happle")
    add_entry(redis_client, "hanana nam")
    add_entry(redis_client, "horange")

    # Call the test function
    test_fuzzy_suggestions('happle')
