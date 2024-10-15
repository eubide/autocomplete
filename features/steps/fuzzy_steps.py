from behave import given, when, then
from fuzzy import add_item, get_fuzzy_suggestions
import redis


@given('a Redis client')
def step_given_redis_client(context):
    context.redis_client = redis.Redis(host='localhost', port=6379, db=0)


@given('an empty Redis database')
def step_given_empty_redis_db(context):
    context.redis_client.flushdb()


@when('I add the following items to the autocomplete system')
def step_when_add_items(context):
    for row in context.table:
        add_item(context.redis_client, row['item'])


@when('I get fuzzy suggestions for "{input_word}"')
def step_when_get_fuzzy_suggestions(context, input_word):
    context.suggestions = get_fuzzy_suggestions(
        context.redis_client, input_word)


@then('the suggestions should contain some of the following')
def step_then_suggestions_should_contain(context):
    expected_suggestions = [row['suggestion'] for row in context.table]
    actual_suggestions = context.suggestions
    assert all(suggestion in actual_suggestions for suggestion in expected_suggestions), \
        f"Expected suggestions {expected_suggestions} not all found in actual suggestions {actual_suggestions}"


@then('the first suggestion should be "{expected_suggestion}"')
def step_then_first_suggestion_should_be(context, expected_suggestion):
    assert context.suggestions[0] == expected_suggestion, \
        f"Expected first suggestion {expected_suggestion} not found"
