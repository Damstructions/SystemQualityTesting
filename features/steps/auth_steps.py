import time

from behave import then, when

PASSWORD = "Passw0rd!QA"


@when("I sign up with a new username")
def step_signup(context):
    # Unique per run: the demo site keeps every account in one shared database
    context.username = f"qa_user_{int(time.time() * 1000)}"
    context.auth.sign_up(context.username, PASSWORD)


@when("I log in with that username and password")
def step_login(context):
    # Make sure the sign-up alert has arrived before moving on
    assert context.alerts.wait_for("Sign up successful"), "Sign up did not succeed"
    context.auth.log_in(context.username, PASSWORD)


@when("I log in with that username and the wrong password")
def step_login_wrong(context):
    assert context.alerts.wait_for("Sign up successful"), "Sign up did not succeed"
    context.auth.log_in(context.username, PASSWORD + "-wrong")


@when('I log in as the unknown user "{username}"')
def step_login_unknown(context, username):
    context.auth.log_in(username, PASSWORD)


@then("I should see the welcome message for that user")
def step_welcome(context):
    text = context.auth.welcome_text()
    assert context.username in text, f"Welcome text was {text!r}"
