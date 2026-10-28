from behave import step, then, when


@step("I open the cart page")
def step_open_cart(context):
    context.cart.open()


@when("I reload the cart page")
def step_reload(context):
    context.cart.reload()


@when('I delete "{product}" from the cart')
def step_delete(context, product):
    context.cart.delete(product)


@then("the cart should be empty")
def step_empty(context):
    assert context.cart.is_empty(), f"Cart still has {context.cart.count()} line(s)"


@then('the cart should contain "{product}"')
def step_contains(context, product):
    titles = [i["title"] for i in context.cart.items()]
    assert product in titles, f"'{product}' not in cart {titles}"


@then('the cart should not contain "{product}"')
def step_not_contains(context, product):
    titles = [i["title"] for i in context.cart.items()]
    assert product not in titles, f"'{product}' is still in the cart {titles}"


@then("the number of cart lines should be {n:d}")
def step_line_count(context, n):
    actual = len(context.cart.items())
    assert actual == n, f"Expected {n} cart line(s), found {actual}"


@then("the cart total should equal the sum of the item prices")
def step_total_sum(context):
    expected = sum(i["price"] for i in context.cart.items())
    actual = context.cart.total()
    assert actual == expected, f"Item prices add to {expected}, cart total shows {actual}"


@then('the cart total should be twice the price of "{product}"')
def step_total_twice(context, product):
    expected = context.prices[product] * 2
    actual = context.cart.total()
    assert actual == expected, f"Expected 2 x {context.prices[product]} = {expected}, got {actual}"


@then('the cart price for "{product}" should match its product page price')
def step_price_match(context, product):
    in_cart = {i["title"]: i["price"] for i in context.cart.items()}
    assert product in in_cart, f"'{product}' not in cart {list(in_cart)}"
    assert in_cart[product] == context.prices[product], (
        f"Product page showed {context.prices[product]}, cart shows {in_cart[product]}"
    )
