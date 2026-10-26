package assignment.jiyun.pages;

import com.microsoft.playwright.Page;
import java.util.regex.Pattern;
import static com.microsoft.playwright.assertions.PlaywrightAssertions.assertThat;

/** Registration and account setup for isolated scenarios; no dependency on teammates' tests. */
public final class AccountPage {
    private final Page page;
    private final String baseUrl;

    public AccountPage(Page page, String baseUrl) {
        this.page = page;
        this.baseUrl = baseUrl;
    }

    public void register(String email, String password, String confirmation) {
        page.navigate(baseUrl + "index.php?route=account/register");
        page.locator("#input-firstname").fill("Test");
        page.locator("#input-lastname").fill("Shopper");
        page.locator("#input-email").fill(email);
        page.locator("#input-telephone").fill("0400000000");
        page.locator("#input-password").fill(password);
        page.locator("#input-confirm").fill(confirmation);
        page.locator("input[name='newsletter'][value='0']").check();
        page.locator("input[name='agree']").check();
        page.locator("#content input[type='submit']").click();
    }

    public void createAccount(String email, String password) {
        register(email, password, password);
        assertThat(page).hasURL(Pattern.compile(".*route=account/success.*"));
        openAccount();
        assertSignedIn();
    }

    public void openAccount() {
        page.navigate(baseUrl + "index.php?route=account/account");
    }

    public void logout() {
        page.navigate(baseUrl + "index.php?route=account/logout");
        assertThat(page).hasURL(Pattern.compile(".*route=account/logout.*"));
        assertThat(page.locator("#content")).containsText("You have been logged off your account");
    }

    public void assertSignedIn() {
        assertThat(page).hasURL(Pattern.compile(".*route=account/account.*"));
        assertThat(page.locator("#content h2").first()).hasText("My Account");
        assertThat(page.locator("#column-right a[href*='route=account/logout']")).isVisible();
    }

    public void assertSignedOut() {
        assertThat(page).hasURL(Pattern.compile(".*route=account/login.*"));
        assertThat(page.locator("#content input[type='submit']")).hasValue("Login");
    }
}
