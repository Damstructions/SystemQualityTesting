package tests;
import support.AccountPage;
import support.BrowserTest;
import com.microsoft.playwright.Page;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
@Tag("logout")
@DisplayName("TC-JT-LOGOUT User logout")
class LogoutTest extends BrowserTest {
    @Test
    @DisplayName("LOGOUT-01 Logout restores guest controls and removes the authentication cookie")
    void logoutRestoresGuestState() {
        // A unique real account avoids dependence on teammates' tests or shared credentials.
        account.createSignedInAccount(uniqueUsername(), PASSWORD);
        checkpoint("signed-in");
        account.logout();
    }
    @Test
    @DisplayName("LOGOUT-02 Reloading after logout does not restore the session")
    void logoutSurvivesReload() {
        account.createSignedInAccount(uniqueUsername(), PASSWORD);
        account.logout();
        page.reload();
        AccountPage.assertSignedOut(page);
    }
    @Test
    @DisplayName("LOGOUT-03 A new tab in the same browser remains signed out after logout")
    void logoutAppliesToNewTab() {
        account.createSignedInAccount(uniqueUsername(), PASSWORD);
        account.logout();
        // Reuse the SAME context: an unrelated fresh context would make this check trivial.
        Page original = page;
        page = original.context().newPage();
        page.navigate(original.url());
        AccountPage.assertSignedOut(page);
    }
}
