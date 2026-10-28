from behave import then, when


@when('I select the "{category}" category')
def step_category(context, category):
    context.home.select_category(category)


@when('I open the product "{product}"')
def step_open_product(context, product):
    context.home.open_product(product)


@when("I go to the next page of products")
def step_next(context):
    context.first_page_titles = context.home.titles()
    context.home.next_page()


@then("I should see products")
def step_see_products(context):
    assert context.home.titles(), "No products are listed"


@then('the products should include "{product}"')
def step_include(context, product):
    titles = context.home.titles()
    assert product in titles, f"'{product}' not in {titles}"


@then('the product page should show the name "{name}"')
def step_product_name(context, name):
    assert context.product.name() == name, f"Page shows {context.product.name()!r}"


@then("the product page should show a price")
def step_product_price(context):
    assert context.product.price() > 0, "Product price is missing or zero"
