package assignment.jiyun.tests;

import assignment.jiyun.pages.CatalogPage;
import assignment.jiyun.support.BrowserTest;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

import java.util.regex.Pattern;

import static com.microsoft.playwright.assertions.PlaywrightAssertions.assertThat;

@Tag("wishlist")
@DisplayName("TC-JT-WISH Wish list")
class WishlistTest extends BrowserTest {
    @Test
    @DisplayName("WISH-01 A signed-in customer can save a product")
    void addProductToWishlist() {
        // Registration supplies a private fixture; login is not this test's subject.
        account.createAccount(uniqueEmail(), PASSWORD);
        catalog.addToWishlist(CatalogPage.IPHONE);
        catalog.openWishlist();
        assertThat(page).hasURL(Pattern.compile(".*route=account/wishlist.*"));
        assertThat(catalog.wishlistRows()).hasCount(1);
        assertThat(catalog.wishlistRow("iPhone")).isVisible();
        // Saved account data must survive reloading the page.
        page.reload();
        assertThat(catalog.wishlistRow("iPhone")).isVisible();
        assertThat(catalog.wishlistRows()).hasCount(1);
    }

    @Test
    @DisplayName("WISH-02 Removing one saved product preserves another")
    void removeProductFromWishlist() {
        account.createAccount(uniqueEmail(), PASSWORD);
        catalog.addToWishlist(CatalogPage.IPHONE);
        catalog.addToWishlist(CatalogPage.MACBOOK);
        catalog.openWishlist();
        assertThat(catalog.wishlistRows()).hasCount(2);
        catalog.removeWishlistProduct("iPhone");
        assertThat(catalog.wishlistRows()).hasCount(1);
        assertThat(catalog.wishlistRow("iPhone")).hasCount(0);
        assertThat(catalog.wishlistRow("MacBook")).isVisible();
        page.reload();
        assertThat(catalog.wishlistRows()).hasCount(1);
        assertThat(catalog.wishlistRow("MacBook")).isVisible();
    }

    @Test
    @DisplayName("WISH-03 An anonymous visitor must log in to view saved items")
    void anonymousWishlistRequiresLogin() {
        catalog.openWishlist();
        account.assertSignedOut();
        assertThat(page.locator("#content input[name='email']")).isVisible();
        assertThat(page.locator("#content input[name='password']")).isVisible();
        assertThat(catalog.wishlistRows()).hasCount(0);
    }
}
