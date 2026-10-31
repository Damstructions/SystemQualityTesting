package support;

import com.microsoft.playwright.*;
import com.microsoft.playwright.options.AriaRole;
import java.util.ArrayList;
import java.util.List;
import java.util.function.Consumer;
import static com.microsoft.playwright.assertions.PlaywrightAssertions.assertThat;
import static org.junit.jupiter.api.Assertions.*;

/** Independent account fixtures for logout tests; signup/login are prerequisites only. */
public final class AccountPage {
    private final Page page;

    public AccountPage(Page page) { this.page = page; }

    public void createSignedInAccount(String username, String password) {
        page.locator("#signin2").click();
        page.locator("#sign-username").fill(username);
        page.locator("#sign-password").fill(password);
        List<String> alerts = new ArrayList<>();
        Consumer<Dialog> listener = dialog -> { alerts.add(dialog.message()); dialog.accept(); };
        page.onDialog(listener);
        try {
            page.locator("#signInModal").getByRole(AriaRole.BUTTON,
                    new Locator.GetByRoleOptions().setName("Sign up").setExact(true)).click();
            page.waitForCondition(() -> !alerts.isEmpty());
            assertEquals(List.of("Sign up successful."), alerts, "Account fixture must be created successfully");
            assertThat(page.locator("#signInModal")).isHidden();
        } finally {
            page.offDialog(listener);
        }
        page.locator("#login2").click();
        page.locator("#loginusername").fill(username);
        page.locator("#loginpassword").fill(password);
        page.locator("#logInModal").getByRole(AriaRole.BUTTON,
                new Locator.GetByRoleOptions().setName("Log in").setExact(true)).click();
        assertThat(page.locator("#nameofuser")).hasText("Welcome " + username);
        assertThat(page.locator("#logout2")).isVisible();
        assertTrue(hasAuthCookie(page), "Logout requires a real authenticated session");
    }

    public void logout() {
        page.locator("#logout2").click();
        assertSignedOut(page);
    }

    public static boolean hasAuthCookie(Page target) {
        return target.context().cookies(target.url()).stream()
                .anyMatch(cookie -> cookie.name.equals("tokenp_") && !cookie.value.isBlank());
    }

    public static void assertSignedOut(Page target) {
        assertThat(target.locator("#login2")).isVisible();
        assertThat(target.locator("#signin2")).isVisible();
        assertThat(target.locator("#logout2")).isHidden();
        assertThat(target.locator("#nameofuser")).isHidden();
        assertFalse(hasAuthCookie(target), "Logout must remove the browser authentication cookie");
    }
}
