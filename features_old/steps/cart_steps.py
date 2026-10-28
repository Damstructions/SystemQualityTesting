from behave import given, when, then
from pages.cart_page import CartPage


def cart(context):
    if not hasattr(context, "cart"):
        context.cart = CartPage(context.page, context.base_url)
    return context.cart


# ---- Given ------------------------------------------------------------------
@given("I have an empty cart")
def step_empty_cart(context):
    # environment.py gives every scenario a fresh browser page, so the cart
    # starts empty. This step verifies that precondition instead of assuming it.
    cart(context).open()
    assert cart(context).is_empty_message_visible(), "Cart was not empty at the start"


# ---- When -------------------------------------------------------------------
@when('I add "{product}" to the cart')
def step_add(context, product):
    cart(context).add_product(product)


@when('I add "{product}" to the cart with quantity {qty:d}')
def step_add_qty(context, product, qty):
    cart(context).add_product(product, qty)


@when("I open the cart page")
def step_open_cart(context):
    cart(context).open()


@when("I reload the cart page")
def step_reload_cart(context):
    cart(context).reload()


@when('I update the quantity of "{product}" to {qty:d}')
def step_update_qty(context, product, qty):
    cart(context).update_quantity(product, qty)


@when('I remove "{product}" from the cart')
def step_remove(context, product):
    cart(context).remove(product)


# ---- Then -------------------------------------------------------------------
@then("I should see the empty cart message")
def step_see_empty(context):
    assert cart(context).is_empty_message_visible(), "Empty cart message not shown"


@then('the cart should contain "{product}" with quantity {qty:d}')
def step_cart_contains(context, product, qty):
    assert cart(context).contains(product), f"'{product}' is not in the cart"
    actual = cart(context).quantity_of(product)
    assert actual == qty, f"Expected quantity {qty} for '{product}', found {actual}"


@then("the cart should contain {n:d} line items")
def step_line_items(context, n):
    actual = cart(context).line_item_count()
    assert actual == n, f"Expected {n} line items, found {actual}"


@then('the line total for "{product}" should be {qty:d} times the unit price')
def step_line_total(context, product, qty):
    unit = cart(context).unit_price(product)
    total = cart(context).line_total(product)
    assert total == unit * qty, f"Expected {unit} x {qty} = {unit * qty}, page shows {total}"


@then("the cart sub-total should equal the sum of the line totals")
def step_subtotal(context):
    expected = sum(cart(context).all_line_totals())
    actual = cart(context).sub_total()
    assert actual == expected, f"Line totals add to {expected}, sub-total shows {actual}"
