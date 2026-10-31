# Jiyun Java tests

Java + Playwright + JUnit tests for [Demoblaze](https://www.demoblaze.com/).

- Logout: restore guest state, stay logged out after reload, and stay logged out in a new tab.
- Contact form: an English message, a multiline English message, and cancelling a draft. Checks the demo's confirmation and form behaviour, not actual email delivery.
- Homepage carousel: next/previous navigation with wraparound, and selecting banners by indicator.

Each test case contains three scenarios (nine scenarios in total). Signup/login only prepare independent accounts for logout tests. Automatic carousel rotation is paused to check manual controls reliably.

The three test files are in `src/tests/`; shared browser and page helpers are in `src/support/`.

## Run

Requires JDK 17+ and Maven 3.9+. From the repository root:

```sh
cd jiyun-java-tests
mvn test-compile
mvn exec:java -Dexec.mainClass=com.microsoft.playwright.CLI -Dexec.classpathScope=test -Dexec.args="install chromium"
mvn test
```

The Chromium installation command is only needed on first setup. Use `mvn -Dheaded=true test` for a visible browser, or `mvn -Dbrowser.channel=chrome test` for installed Chrome. Reports and screenshots are generated under the ignored `target/` directory.
