from behave import given, when, then


@given('I have an empty film list')
def step_given_empty_film_list(context):
    context.film_list = []


@when('I add "Inception" to the film list')
def step_when_add_film(context):
    context.film_list.append("Inception")


@then('the film list should contain "Inception"')
def step_then_film_list_contains_inception(context):
    assert "Inception" in context.film_list
