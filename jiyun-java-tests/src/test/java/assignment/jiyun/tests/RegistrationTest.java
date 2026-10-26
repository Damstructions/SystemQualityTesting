package assignment.jiyun.tests;

import assignment.jiyun.support.BrowserTest;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

import java.util.regex.Pattern;

import static com.microsoft.playwright.assertions.PlaywrightAssertions.assertThat;

@Tag("registration")
@DisplayName("TC-JT-REG User registration")
class RegistrationTest extends BrowserTest {
    @Test
    @DisplayName("REG-01 Valid details create an authenticated account")
    void registerWithValidDetails() {
        // Catches successful-looking submissions that do not create a usable account.
        account.register(uniqueEmail(), PASSWORD, PASSWORD);
        assertThat(page).hasURL(Pattern.compile(".*route=account/success.*"));
        assertThat(page.locator("#content")).containsText("Your new account has been successfully created");
        checkpoint("account-created");
        account.openAccount();
        account.assertSignedIn();
    }

    @Test
    @DisplayName("REG-02 Mismatched password confirmation is rejected")
    void rejectMismatchedPasswords() {
        // All other required inputs are valid, isolating password confirmation validation.
        account.register(uniqueEmail(), PASSWORD, "DifferentDemoPassword92!");
        assertThat(page.locator("#input-confirm").locator("..").locator(".text-danger"))
                .containsText("Password confirmation does not match password");
        assertThat(page).hasURL(Pattern.compile(".*route=account/register.*"));
        checkpoint("confirmation-rejected");
        account.openAccount();
        account.assertSignedOut();
    }

    @Test
    @DisplayName("REG-03 An existing email cannot create a second account")
    void rejectDuplicateEmail() {
        // Create this scenario's fixture; it does not depend on REG-01 running first.
        String email = uniqueEmail();
        account.createAccount(email, PASSWORD);
        account.logout();
        account.register(email, PASSWORD, PASSWORD);
        assertThat(page.locator("#account-register .alert-danger"))
                .containsText("E-Mail Address is already registered");
        assertThat(page).hasURL(Pattern.compile(".*route=account/register.*"));
        checkpoint("duplicate-email-rejected");
        account.openAccount();
        account.assertSignedOut();
    }
}
