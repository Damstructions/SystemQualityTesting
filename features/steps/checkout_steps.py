from behave import then, when


@when("I click Place Order")
def step_place_order(context):
    # Remember the total shown in the cart so later steps can compare to it
    context.cart_total = context.cart.total()
    context.cart.place_order()


@when("I fill in valid details on the order form")
def step_valid(context):
    context.checkout.fill_valid_details()


@when("I fill in only the name on the order form")
def step_only_name(context):
    context.checkout.fill(name="Test Shopper")


@when("I fill in only the card number on the order form")
def step_only_card(context):
    context.checkout.fill(card="4111111111111111")


@when("I submit the order form")
def step_submit(context):
    context.checkout.submit()


@when("I accept the purchase confirmation")
def step_accept(context):
    context.checkout.confirm_ok()


@then("the order form total should equal the cart total")
def step_modal_total(context):
    actual = context.checkout.modal_total()
    assert actual == context.cart_total, f"Cart total {context.cart_total}, order form shows {actual}"


@then("I should see a purchase confirmation")
def step_confirmation(context):
    assert context.checkout.confirmation_shown(), "No 'Thank you for your purchase' confirmation"


@then("the confirmation amount should equal the cart total")
def step_amount(context):
    actual = context.checkout.confirmation_amount()
    assert actual == context.cart_total, f"Cart total {context.cart_total}, confirmation says {actual}"
