package support;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.options.AriaRole;
import static com.microsoft.playwright.assertions.PlaywrightAssertions.assertThat;

/** Contact modal and promotional banner, separate from the product catalogue. */
public final class HomePage {
    private final Page page;
    private final String baseUrl;

    public HomePage(Page page, String baseUrl) {
        this.page = page;
        this.baseUrl = baseUrl;
    }

    public void open() {
        page.navigate(baseUrl);
        assertThat(page.locator("#nava")).isVisible();
    }

    public Locator contactModal() { return page.locator("#exampleModal"); }

    public void openContact() {
        page.getByRole(AriaRole.LINK, new Page.GetByRoleOptions().setName("Contact").setExact(true)).click();
        assertThat(contactModal()).isVisible();
        assertThat(contactModal().locator(".modal-title")).hasText("New message");
    }

    public void fillContact(String email, String name, String message) {
        contactModal().locator("#recipient-email").fill(email);
        contactModal().locator("#recipient-name").fill(name);
        contactModal().locator("#message-text").fill(message);
    }

    public Locator carousel() { return page.locator("#carouselExampleIndicators"); }

    public void prepareCarousel() {
        // Pause only the automatic timer; all tested transitions use real UI controls.
        // Otherwise the five-second timer can race manual navigation assertions.
        page.waitForFunction("() => window.jQuery && typeof jQuery.fn.carousel === 'function'");
        carousel().evaluate("el => window.jQuery(el).carousel('pause')");
        selectSlide(0);
        assertSlide(0);
        // Selecting the already active indicator can restart Bootstrap's automatic timer.
        carousel().evaluate("el => window.jQuery(el).carousel('pause')");
    }

    public void selectSlide(int index) {
        carousel().locator(".carousel-indicators li").nth(index).click();
    }

    public void nextSlide() { carousel().locator(".carousel-control-next").click(); }
    public void previousSlide() { carousel().locator(".carousel-control-prev").click(); }

    public void assertSlide(int index) {
        String[] images = {"Samsung1.jpg", "nexus1.jpg", "iphone1.jpg"};
        String[] labels = {"First slide", "Second slide", "Third slide"};
        assertThat(carousel().locator(".carousel-item.active")).hasCount(1);
        Locator image = carousel().locator(".carousel-item.active img");
        assertThat(image).hasAttribute("src", images[index]);
        assertThat(image).hasAttribute("alt", labels[index]);
        assertThat(image).isVisible();
        assertThat(carousel().locator(".carousel-indicators li.active")).hasCount(1);
        assertThat(carousel().locator(".carousel-indicators li.active"))
                .hasAttribute("data-slide-to", Integer.toString(index));
        // A visible but broken image is not a successful banner change.
        page.waitForFunction("src => { const img = document.querySelector('#carouselExampleIndicators .carousel-item.active img');"
                + " return img && img.getAttribute('src') === src && img.complete && img.naturalWidth > 0; }", images[index]);
        assertThat(carousel().locator(".carousel-item-next, .carousel-item-prev")).hasCount(0);
    }
}
