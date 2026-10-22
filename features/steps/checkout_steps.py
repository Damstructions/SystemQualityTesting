from behave import when, then
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


def checkout(context):
    if not hasattr(context, "checkout"):
        context.checkout = CheckoutPage(context.page, context.base_url)
    return context.checkout


def cart(context):
    if not hasattr(context, "cart"):
        context.cart = CartPage(context.page, context.base_url)
    return context.cart


# ---- When -------------------------------------------------------------------
@when("I go directly to the checkout page")
def step_direct_checkout(context):
    checkout(context).open()


@when("I proceed to checkout from the cart")
def step_proceed(context):
    cart(context).proceed_to_checkout()


@when("I choose guest checkout")
def step_guest(context):
    checkout(context).choose_guest()


@when("I continue without entering any details")
def step_continue_empty(context):
    checkout(context).click_continue()


@when("I enter valid guest billing details")
def step_billing(context):
    checkout(context).fill_billing_details()


@when("I accept the terms and continue to confirmation")
def step_terms(context):
    checkout(context).accept_terms_and_continue()


@when("I confirm the order")
def step_confirm(context):
    checkout(context).confirm_order()


# ---- Then -------------------------------------------------------------------
@then("I should be redirected to the cart page")
def step_redirected(context):
    context.page.wait_for_url("**checkout/cart**", timeout=10000)
    assert "checkout/cart" in context.page.url


@then("I should be on the checkout page")
def step_on_checkout(context):
    context.page.wait_for_url("**checkout/checkout**", timeout=10000)
    assert "checkout/checkout" in context.page.url


@then("I should see validation errors")
def step_errors(context):
    assert checkout(context).validation_errors_visible(), "No validation error was shown"


@then("the order should be placed")
def step_placed(context):
    assert checkout(context).order_placed(), "Order confirmation message not shown"
