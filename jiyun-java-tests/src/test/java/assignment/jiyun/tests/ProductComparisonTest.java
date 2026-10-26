package assignment.jiyun.tests;

import assignment.jiyun.pages.CatalogPage;
import assignment.jiyun.support.BrowserTest;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

import static com.microsoft.playwright.assertions.PlaywrightAssertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertEquals;

@Tag("comparison")
@DisplayName("TC-JT-COMP Product comparison")
class ProductComparisonTest extends BrowserTest {
    @Test
    @DisplayName("COMP-01 One product is shown with the correct model")
    void compareSingleProduct() {
        catalog.addToComparison(CatalogPage.IPHONE);
        catalog.openComparison();
        assertEquals(1, catalog.comparisonProductNames().size());
        assertEquals("iPhone", catalog.comparisonProductNames().get(0));
        assertEquals("product 11", catalog.comparisonValue("Model", "iPhone"));
    }

    @Test
    @DisplayName("COMP-02 Two products retain their own details and prices")
    void compareTwoProducts() {
        // Read current catalogue prices because this is a mutable shared demo store.
        String iphonePrice = catalog.addToComparison(CatalogPage.IPHONE);
        String macbookPrice = catalog.addToComparison(CatalogPage.MACBOOK);
        catalog.openComparison();
        assertEquals(java.util.List.of("iPhone", "MacBook"), catalog.comparisonProductNames());
        assertEquals("product 11", catalog.comparisonValue("Model", "iPhone"));
        assertEquals("Product 16", catalog.comparisonValue("Model", "MacBook"));
        assertEquals(iphonePrice, catalog.comparisonValue("Price", "iPhone"));
        assertEquals(macbookPrice, catalog.comparisonValue("Price", "MacBook"));
    }

    @Test
    @DisplayName("COMP-03 Removing one product preserves the other")
    void removeComparedProduct() {
        catalog.addToComparison(CatalogPage.IPHONE);
        catalog.addToComparison(CatalogPage.MACBOOK);
        catalog.openComparison();
        assertEquals(2, catalog.comparisonProductNames().size());
        catalog.removeComparedProduct("iPhone");
        assertThat(page.locator("#content")).containsText("Product Comparison");
        assertEquals(java.util.List.of("MacBook"), catalog.comparisonProductNames());
        assertEquals("Product 16", catalog.comparisonValue("Model", "MacBook"));
    }
}
