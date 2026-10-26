# Jiyun Java tests

Java + Playwright + JUnit tests for [OpenCart Abstracta](https://opencart.abstracta.us/).

- Registration: valid details, mismatched passwords and duplicate email.
- Product comparison: add one product, compare two products and remove one.
- Wish list: add a product, remove a product and require login for anonymous access.

Each test case contains three scenarios (nine scenarios in total).

## Run

Requires JDK 17+ and Maven 3.9+. From the repository root:

```sh
cd jiyun-java-tests
mvn test-compile
mvn exec:java -Dexec.mainClass=com.microsoft.playwright.CLI -Dexec.classpathScope=test -Dexec.args="install chromium"
mvn test
```

The Chromium installation command is only needed on first setup. Use `mvn -Dheaded=true test` to run with a visible browser.
