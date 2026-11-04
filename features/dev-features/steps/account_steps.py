from behave import given, then, when

# T010 note: this test case logs on as this existing customer.
EMAIL = "Ag007@temp-mail.io"
PASSWORD = "greedisgood10000"


@given("the customer is logged out")
def step_logged_out(context):
    context.account.open_login()
    assert context.account.header_is_logged_out(), context.page.url


@when("the customer logs on by submitting the logon form")
def step_logon(context):
    context.account.login(EMAIL, PASSWORD)


@then("the logon feedback page is My Account")
def step_logon_feedback(context):
    assert context.account.logon_feedback_shown(), context.page.url


@when("the customer clicks the Logout button in My Account")
def step_click_logout(context):
    context.account.logout_from_my_account()


@then("the logout feedback page is shown")
def step_logout_feedback(context):
    assert context.account.logout_feedback_shown(), context.page.url


@when("the customer deletes cookies and site data in Chrome")
def step_delete_site_data(context):
    context.session_cookie = context.account.session_cookie(context.browser_context)
    context.account.delete_chrome_cookies_and_site_data(context.browser_context)


@then("this site has no cookies stored")
def step_cookie_jar_empty(context):
    remaining = context.browser_context.cookies()
    assert remaining == [], remaining


@when("the customer reloads the page")
def step_reload(context):
    context.account.reload()


@then("the old session cookie is gone")
def step_old_session_gone(context):
    values = [cookie["value"] for cookie in context.browser_context.cookies()]
    assert context.session_cookie not in values, values


@then("the page shows no logon sign")
def step_no_logon_sign(context):
    assert context.account.shows_no_logon_sign(), context.page.url
