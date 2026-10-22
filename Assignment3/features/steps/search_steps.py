from behave import given, when, then
from pages.home_page import HomePage

@given("I am on the store home page")
def step_home(context):
    context.home = HomePage(context.page, context.base_url)
    context.home.open()

@when('I search for "{term}"')
def step_search(context, term):
    context.home.search(term)

@then("I should see search results")
def step_results(context):
    assert context.home.result_titles(), "No results found"

@then('the results should include "{text}"')
def step_include(context, text):
    titles = " ".join(context.home.result_titles()).lower()
    assert text.lower() in titles

@then('I should see a "no product" message')
def step_none(context):
    assert context.home.no_results_message_visible(), \
        "Expected a 'no product' message but none appeared"