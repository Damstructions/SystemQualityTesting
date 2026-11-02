package tests;

import support.BrowserTest;
import com.microsoft.playwright.Locator;
import com.microsoft.playwright.options.AriaRole;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

import static com.microsoft.playwright.assertions.PlaywrightAssertions.assertThat;

@Tag("about-us")
@DisplayName("TC-JT-ABOUT About Us dialog")
class AboutUsTest extends BrowserTest {
    private Locator dialog() { return page.locator("#videoModal"); }

    private void openAboutUs() {
        page.locator("a[data-target='#videoModal']").click();
        assertThat(dialog()).isVisible();
        assertThat(dialog().locator(".modal-title")).hasText("About us");
    }

    private void assertClosed() {
        assertThat(dialog()).isHidden();
        // Closing must also remove the overlay that would block homepage interaction.
        assertThat(page.locator(".modal-backdrop")).hasCount(0);
    }

    @Test
    @DisplayName("ABOUT-01 About us opens the dialog with its title, video area and close controls")
    void openAboutUsDialog() {
        assertThat(dialog()).isHidden();
        openAboutUs();
        // This checks that the video area is displayed, not that streaming playback works.
        assertThat(dialog().locator("video")).isVisible();
        assertThat(dialog().locator(".modal-footer").getByRole(AriaRole.BUTTON,
                new Locator.GetByRoleOptions().setName("Close").setExact(true))).isVisible();
        assertThat(dialog().locator(".modal-header button.close")).isVisible();
    }

    @Test
    @DisplayName("ABOUT-02 The Close button dismisses the dialog and homepage navigation remains usable")
    void closeUsingFooterButton() {
        openAboutUs();
        checkpoint("dialog-open");
        dialog().locator(".modal-footer").getByRole(AriaRole.BUTTON,
                new Locator.GetByRoleOptions().setName("Close").setExact(true)).click();
        assertClosed();
        checkpoint("dialog-closed");
        // A real click verifies that the dismissed dialog no longer blocks the page.
        page.locator("#nava").click();
        assertThat(page.locator("#nava")).isVisible();
        assertClosed();
    }

    @Test
    @DisplayName("ABOUT-03 The X button dismisses the dialog and it can be opened again")
    void closeUsingXAndReopen() {
        openAboutUs();
        dialog().locator(".modal-header button.close").click();
        assertClosed();
        checkpoint("closed-with-x");
        openAboutUs();
        assertThat(dialog().locator("video")).isVisible();
    }
}
