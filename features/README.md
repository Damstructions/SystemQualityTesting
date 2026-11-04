# features

Behavioral tests for SystemQualityTesting. This directory contains two Behave suites driven by the Playwright sync API. Scenarios are written in Gherkin. Page objects hold selectors and page actions. Step definitions call those actions and check the results.

The DemoBlaze suite lives at the root of this directory and targets `https://www.demoblaze.com/`. The OpenCart T010 logout suite lives in `dev-features/` and targets `https://opencart.abstracta.us/`.

The root `behave.ini` sets `show_skipped` to false and limits `paths` to:

- `features/auth.feature`
- `features/cart.feature`
- `features/catalogue.feature`
- `features/checkout.feature`
- `features/dev-features/logout.feature`
- `features/dev-features/delete-cookie.feature`

A `behave` run from the repository root uses `features/` as its base directory, so it loads `features/environment.py` and `features/steps/`. `features/steps/opencart_steps.py` registers the OpenCart steps, and `features/environment.py` builds `context.account` for those scenarios. That root run includes `dev-features`.

## Set up the virtualenv

Run the commands below from the repository root. They are the same in Command Prompt and PowerShell.

`behave` is not on PATH. In PowerShell, `behave features/dev-features` raises `CommandNotFoundException`. In Command Prompt, the same text reports that `behave` is not recognized. `python` on PATH is 3.14, and that interpreter does not have the behave package. `python features/dev-features` fails as well: the directory has no `__main__.py`, so Python reports `can't find '__main__' module`.

Create the virtualenv with Python 3.13. Install the requirements with that environment's interpreter so pip does not target Python 3.14:

```text
py -3.13 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

`requirements.txt` installs Behave and the Playwright Python package for every suite in this directory. `.venv/` is listed in `.gitignore`. Each checkout creates its own virtualenv.

DemoBlaze launches the Chromium build bundled with Playwright. Install that browser once, still through the virtualenv interpreter:

```text
.venv\Scripts\python.exe -m playwright install chromium
```

The OpenCart scenarios launch the installed Google Chrome with `channel="chrome"`. The Chromium download does not provide that browser.

## Run with the virtualenv's Behave

Start Behave as a module of `.venv\Scripts\python.exe`. The command works in Command Prompt and PowerShell. It does not need `behave` on PATH, and it does not need the virtualenv to be activated.

Every feature named in `behave.ini`, DemoBlaze and OpenCart:

```text
.venv\Scripts\python.exe -m behave
```

DemoBlaze scenarios tagged `@smoke`:

```text
.venv\Scripts\python.exe -m behave --tags=@smoke
```

The OpenCart suite under `dev-features`:

```text
.venv\Scripts\python.exe -m behave features/dev-features
```

`features/dev-features/run.cmd` is that OpenCart command for either terminal. From the repository root it changes to the root, sets `HEADLESS` to `1` when the variable is unset, and runs `.venv\Scripts\python.exe -m behave features/dev-features`:

```text
features\dev-features\run.cmd
```

Activating the virtualenv puts `.venv\Scripts` first on PATH. `behave` then means the virtualenv's Behave, and the short commands work for the rest of that terminal session.

Command Prompt:

```text
.venv\Scripts\activate.bat
behave
behave features/dev-features
```

PowerShell:

```text
.\.venv\Scripts\Activate.ps1
behave
behave features/dev-features
```

An activated root `behave` reads `behave.ini` and runs the DemoBlaze features together with the two OpenCart features. `behave features/dev-features` still runs only the OpenCart suite, using `dev-features/environment.py`.

Both hooks read `HEADLESS`, `SLOW_MO`, and `BASE_URL`. `HEADLESS` defaults to `0` in the hook files, which opens a browser window. `run.cmd` sets `HEADLESS` to `1` when it is unset. Set `HEADLESS=0` before `run.cmd` to show the window. `SLOW_MO` is a delay in milliseconds and defaults to `0`. `BASE_URL` overrides the default site URL of the hook loaded for that run.

PowerShell:

```powershell
$env:HEADLESS = "1"
.venv\Scripts\python.exe -m behave features/dev-features
```

Command Prompt:

```text
set HEADLESS=1
.venv\Scripts\python.exe -m behave features/dev-features
```

## Layout

```text
features/
  environment.py                 DemoBlaze hook
  auth.feature
  cart.feature
  catalogue.feature
  checkout.feature
  pages/                         DemoBlaze page objects
  steps/                         DemoBlaze steps, plus opencart_steps.py
  dev-features/
    environment.py               Shim that loads environment2
    environment2.py              OpenCart hook
    cert_date.py                 Date-only certificate exception
    run.cmd                      Launcher for Command Prompt and PowerShell
    logout.feature
    delete-cookie.feature
    pages/account_page.py
    steps/account_steps.py
```

## DemoBlaze

Run this suite from the repository root with the virtualenv interpreter: `.venv\Scripts\python.exe -m behave`. Install its browser first with `.venv\Scripts\python.exe -m playwright install chromium`.

Each feature starts on the store home page. Every scenario gets a new browser context, so cookies and site storage start empty and the cart and login state do not carry over. On failure, a screenshot is written to `screenshots/` in the working directory.

`auth.feature` is tagged `@auth`. It registers a new account, logs in with that account, logs in with the wrong password, and logs in as the unknown user `no_such_user_qa_12345`. `steps/auth_steps.py` builds a new username from the current time, because the demo site stores every account in one shared database. The password is a constant in that file. Sign-up success, a wrong password, and an unknown user are all reported through the site's `alert()`. After a successful login, the welcome text must contain that username. `Log in after registering` is also tagged `@smoke`.

`catalogue.feature` is tagged `@catalogue`. The home page must list products. The category examples are Phones / Samsung galaxy s6, Laptops / MacBook air, and Monitors / Apple monitor 24. Opening Samsung galaxy s6 must show that name and a price. The next page must list a different set of products. `The home page lists products` is also tagged `@smoke`. Category and paging waits poll `#tbodyid` until AJAX replaces the titles.

`cart.feature` is tagged `@cart`. A new visitor has an empty cart. After a product is added, the scenario checks the name, the number of lines, and that the total equals the sum of the line prices. The cart price for Samsung galaxy s6, Nokia lumia 1520, and Sony vaio i5 must match the product page. Two different products produce two lines. Adding Nexus 6 twice also produces two lines, and the total is twice the unit price. One of two products can be removed, and so can the only product. Sony vaio i5 is still in the cart after the cart page is reloaded. `Add a product to the cart` is also tagged `@smoke`. The add-to-cart step records the price seen on the product page in `context.prices`.

`checkout.feature` is tagged `@checkout`. Every scenario adds Samsung galaxy s6 to the cart and opens the cart. The order form total must equal the cart total. An empty form, a name with no card number, and a card number with no name each raise the alert `Please fill out Name and Creditcard.` Two scenarios tagged `@order` submit a valid order. The confirmation amount must equal the cart total, and accepting the confirmation leaves the cart empty. `I wait a bit` waits 2 seconds after submit.

`@smoke` currently marks the post-registration login, the home-page product list, and adding one product. `@order` marks only the two checkout scenarios that place an order.

Page objects live in `features/pages/`:

| File | Responsibility |
| --- | --- |
| `alerts.py` | `Alerts` records and accepts DemoBlaze `alert()` dialogs. Waiting uses `page.wait_for_timeout` so Playwright can deliver dialog events. |
| `home_page.py` | Home-page titles, categories, and the next page. |
| `product_page.py` | Product name, price, and add to cart. |
| `cart_page.py` | Cart contents, line count, delete, and total. |
| `checkout_page.py` | Order form and confirmation amount. |
| `auth_page.py` | Sign-up, login, and welcome text. |
| `util.py` | `money` parses a price string into a `Decimal`. `exact` builds a whole-string regular expression. |

Step definitions live in `features/steps/`. `common_steps.py` covers the home page, adding a product, and alerts. `auth_steps.py`, `catalogue_steps.py`, `cart_steps.py`, and `checkout_steps.py` are split by area. Their sentences use the shopper voice, `I ...`.

This suite launches the Chromium build bundled with Playwright and does not set `channel`. The default page timeout is 10 seconds.

## OpenCart (`dev-features`)

Run this suite from the repository root with `.venv\Scripts\python.exe -m behave features/dev-features`, or with `features\dev-features\run.cmd`. Both use the virtualenv's Behave. The launcher sets `HEADLESS=1` when that variable is unset. The browser is the installed Google Chrome.

These scenarios implement T010, User Logout. Both features are tagged `@t010` and `@logout`. They log in as the existing customer named in the test case. The account is stored in `dev-features/steps/account_steps.py`, and the email is `Ag007@temp-mail.io`.

`logout.feature` starts logged out, submits the logon form, and checks My Account. The URL contains `route=account/account`, the first `h2` in `#content` is `My Account`, and the header contains Logout. It then clicks the Logout link in the right-hand My Account column (`route=account/logout` inside `#column-right`). The logout page URL contains `route=account/logout`, the text `You have been logged off your account` is visible, and the header shows Login. This scenario checks server-side logout: OpenCart removes the customer from the session. The browser may still hold `OCSESSID`, so the scenario does not require the cookies to be cleared.

`delete-cookie.feature` uses the same login, then deletes this site's cookies and site data in Chrome. Immediately after deletion, and before reload, the cookie jar must be empty. After reload, the old `OCSESSID` value must be gone, the URL must contain `route=account/login`, `#content` must not have a `My Account` heading, and the header must show Login. Reload issues a new `OCSESSID`, `language`, and `currency`, so the scenario does not require the jar to stay empty. Clearing uses the Chrome DevTools Protocol. `Storage.clearDataForOrigin` with `storageTypes` set to `all` removes the host-only `OCSESSID` and leaves the Domain cookies `language` and `currency`. `Network.deleteCookies` then removes every remaining cookie whose domain ends with `opencart.abstracta.us`. The browser is a temporary Chrome profile, so the run leaves the everyday Chrome profile untouched.

`AccountPage` is `dev-features/pages/account_page.py`. The default page timeout is 20 seconds, and the context locale is `en-AU`. The assertions still expect the store's English copy.

`environment2` asks Chrome to ignore a certificate date error only when the default trust store's remaining objection is the date (`certificate has expired` or `certificate is not yet valid`) and the leaf name matches the site host. The exception is Chrome's `--ignore-certificate-errors-spki-list` entry for that leaf key. A hostname mismatch, an untrusted issuer, or any other verification failure is left in place. `ignore_https_errors` is not used. The leaf for `opencart.abstracta.us` was expired on 2026-11-04 (`notAfter` 2026-11-03 05:37:30, Let's Encrypt YE1). Before this check, both scenarios stopped on `net::ERR_CERT_DATE_INVALID` at the login page.

## `environment` and `environment2`

Behave executes only a file named `environment.py` in the base directory. `--stage` adds a prefix to that fixed name. It does not accept an arbitrary filename. Three files are involved.

`features/environment.py` is the DemoBlaze hook, and a root `behave` run executes it. `before_all` starts the Chromium build bundled with Playwright and creates `screenshots/`. `before_scenario` opens a new context and page, sets the default timeout to 10 seconds, and attaches `alerts`, `home`, `product`, `cart`, `checkout`, `auth`, and an empty `prices` dict. The default `BASE_URL` is `https://www.demoblaze.com/`. On failure, `after_scenario` saves a screenshot and closes the context. `after_all` closes the browser and stops Playwright.

`features/dev-features/environment2.py` is the OpenCart hook. Behave does not execute it under that filename. It follows the same lifecycle. `before_all` launches the installed Chrome with `channel="chrome"`. `before_scenario` opens a context with locale `en-AU`, sets the default timeout to 20 seconds, and attaches `account` (`AccountPage`). The default `BASE_URL` is `https://opencart.abstracta.us/`. Screenshots and teardown match the DemoBlaze hook.

`features/dev-features/environment.py` is a shim. `behave features/dev-features` uses `dev-features/` as the base directory because that directory contains `steps/`. Behave executes this `environment.py` only. The shim adds `dev-features/` to the import path and imports `before_all`, `before_scenario`, `after_scenario`, and `after_all` from `environment2`. Those four names become the Behave hooks, and their implementations stay in `environment2.py`. That run does not load `features/environment.py`.

The two hooks differ in site, browser, timeout, locale, and the objects they attach to `context`. DemoBlaze steps use only their own context attributes. OpenCart steps use only `context.account`.

## Merging `dev-features` into `features`

Moving `dev-features` up into `features/` is straightforward. The Gherkin and the `AccountPage` call sites can stay as they are.

The step sentences do not overlap. DemoBlaze sentences use `I ...`, and OpenCart sentences use `the customer ...`. Both step modules can live in `features/steps/`, and Behave will match each sentence to one step.

`account_page.py` can move to `features/pages/`. Its class name and selectors do not collide with the DemoBlaze page objects. `features/environment.py` already puts `features/` on the import path, so `from pages.account_page import AccountPage` still works from the merged hook.

The hooks fold into one `features/environment.py`. A single `before_scenario` can build the DemoBlaze page objects and `AccountPage`. `AccountPage` keeps the OpenCart URL itself, and `context.base_url` can keep pointing at DemoBlaze. The OpenCart cookie clear needs the Chrome DevTools Protocol from the installed Chrome. The DemoBlaze scenarios do not depend on Playwright's bundled Chromium, so the whole suite can launch with `channel="chrome"`.

The merge deletes the `dev-features/environment.py` shim and adds `logout.feature` and `delete-cookie.feature` to `paths` in `behave.ini`. A root `behave` run then includes them. Until those two paths are added, moving the files into `features/` still leaves the default run on the original four features. Once `dev-features/steps/` is no longer its own base directory, one load picks up the OpenCart steps together with the DemoBlaze steps.

## TestCafe

This directory is also used to store future TestCafe test cases.
