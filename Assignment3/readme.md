Run the following

python -m venv .venv

pip install behave playwright
playwright install chromium
pip freeze > requirements.txt

When ready, run the following:

behave                          # all features
behave features/search.feature  # one feature
behave --tags=@smoke            # by tag
behave -f pretty --junit        # JUnit XML for CI