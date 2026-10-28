from behave import given, step, then


def add_product(context, name):
    """Open the product through the UI, remember its price, add it to the cart."""
    context.home.open()
    context.home.open_product(name)
    context.prices[name] = context.product.price()
    context.product.add_to_cart()


@given("I am on the store home page")
def step_home(context):
    context.home.open()


@step('I add "{product}" to the cart')
def step_add(context, product):
    add_product(context, product)


@step('I add "{product}" to the cart {times:d} times')
def step_add_times(context, product, times):
    for _ in range(times):
        add_product(context, product)


@then('I should see the alert "{text}"')
def step_alert(context, text):
    assert context.alerts.wait_for(text), (
        f"Expected an alert containing {text!r}. Alerts seen: {context.alerts.messages}"
    )
