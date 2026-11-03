# Zhihui Yuan —  DemoBlaze tests

Python + Playwright + pytest tests for [DemoBlaze](https://www.demoblaze.com/).

These cases cover functions DemoBlaze log out, sign-up validation, and catalogue Next/Previous paging. They do not repeat category browsing, add to cart, checkout submit, contact, carousel, About us, product-detail, store-logo navigation, or Place Order cancel.

| Test case ID | Function | Three scenarios |
|---|---|---|
| T014 | F16 Log Out | Guest navigation after logout, logout survives refresh, Home stays logged out |
| T015 | F17 Sign-up dialog | Empty fields rejected, existing username rejected, Close does not create a session |
| T016 | F18 Catalogue pagination | Next shows a new list, Previous leaves page 2, Next after Previous does not restore page 1 |

## Setup and execution

Requires Python 3.8 or newer. From this folder:

```bash
cd zhihui-yuan-additional-tests
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
pytest
```

On Windows, activate the virtual environment with `.venv\Scripts\activate`.

Screenshots from each scenario are written to `screenshots/`.
