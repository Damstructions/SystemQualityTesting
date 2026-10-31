package tests;

import support.BrowserTest;
import com.microsoft.playwright.Dialog;
import com.microsoft.playwright.Locator;
import com.microsoft.playwright.options.AriaRole;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import java.util.ArrayList;
import java.util.List;
import java.util.function.Consumer;
import static com.microsoft.playwright.assertions.PlaywrightAssertions.assertThat;
import static org.junit.jupiter.api.Assertions.*;

@Tag("contact")
@DisplayName("TC-JT-CONTACT Contact form")
class ContactTest extends BrowserTest {
    @Test
    @DisplayName("CONTACT-01 A completed form shows confirmation and resets the fields")
    void submitEnglishMessage() {
        submitAndCheck("qa.jiyun@example.com", "Test Shopper", "Please confirm the store opening hours.");
    }

    @Test
    @DisplayName("CONTACT-02 A multiline English message shows confirmation and resets the fields")
    void submitMultilineEnglishMessage() {
        submitAndCheck("qa.jiyun+enquiry@example.com", "Demo Customer",
                "Hello,\nI have a question about delivery.\nThank you.");
    }

    private void submitAndCheck(String email, String name, String message) {
        home.openContact();
        home.fillContact(email, name, message);
        assertThat(home.contactModal().locator("#message-text")).hasValue(message);
        checkpoint("completed-form");
        List<String> alerts = new ArrayList<>();
        Consumer<Dialog> listener = dialog -> { alerts.add(dialog.message()); dialog.accept(); };
        page.onDialog(listener);
        try {
            // The demo only shows an alert and reloads; this does not prove email delivery.
            page.waitForNavigation(() -> home.contactModal().getByRole(AriaRole.BUTTON,
                    new Locator.GetByRoleOptions().setName("Send message").setExact(true)).click());
            assertEquals(List.of("Thanks for the message!!"), alerts);
            assertThat(home.contactModal()).isHidden();
            home.openContact();
            assertThat(home.contactModal().locator("#recipient-email")).isEmpty();
            assertThat(home.contactModal().locator("#recipient-name")).isEmpty();
            assertThat(home.contactModal().locator("#message-text")).isEmpty();
        } finally {
            page.offDialog(listener);
        }
    }

    @Test
    @DisplayName("CONTACT-03 Closing a draft does not submit it and preserves the current page")
    void cancelDraft() {
        home.openContact();
        home.fillContact("qa.jiyun@example.com", "Test Shopper", "Unsent English draft.");
        List<String> alerts = new ArrayList<>();
        Consumer<Dialog> listener = dialog -> { alerts.add(dialog.message()); dialog.accept(); };
        page.onDialog(listener);
        String originalUrl = page.url();
        String marker = "draft-" + uniqueUsername();
        page.evaluate("marker => window.contactDraftMarker = marker", marker);
        try {
            home.contactModal().locator(".modal-footer").getByRole(AriaRole.BUTTON,
                    new Locator.GetByRoleOptions().setName("Close").setExact(true)).click();
            assertThat(home.contactModal()).isHidden();
            home.openContact();
            // The demo retains a cancelled draft until the page is reloaded.
            assertThat(home.contactModal().locator("#message-text")).hasValue("Unsent English draft.");
            assertEquals(marker, page.evaluate("() => window.contactDraftMarker"), "Cancel must not reload the page");
            assertThat(page).hasURL(originalUrl);
            assertTrue(alerts.isEmpty(), "Cancel must not display a submission confirmation");
        } finally {
            page.offDialog(listener);
        }
    }
}
