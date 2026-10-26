package assignment.jiyun.pages;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import java.util.List;
import static com.microsoft.playwright.assertions.PlaywrightAssertions.assertThat;

/** Public product pages, comparison table and account wish list. */
public final class CatalogPage {
    public record Product(int id, String name) {}
    public static final Product IPHONE = new Product(40, "iPhone");
    public static final Product MACBOOK = new Product(43, "MacBook");
    private final Page page;
    private final String baseUrl;

    public CatalogPage(Page page, String baseUrl) {
        this.page = page;
        this.baseUrl = baseUrl;
    }

    private void openProduct(Product product) {
        page.navigate(baseUrl + "index.php?route=product/product&product_id=" + product.id());
        assertThat(page.locator("#content h1")).hasText(product.name());
    }

    public String addToComparison(Product product) {
        openProduct(product);
        String price = page.locator("#content h1").locator("..").locator("ul h2").innerText().trim();
        // Scope by the product ID to avoid clicking a related product's identical button.
        page.locator("button[onclick=\"compare.add('" + product.id() + "');\"]").click();
        assertThat(page.locator(".alert-success")).containsText(product.name());
        assertThat(page.locator(".alert-success")).containsText("product comparison");
        return price;
    }

    public void openComparison() {
        page.navigate(baseUrl + "index.php?route=product/compare");
        assertThat(page.locator("#content h1")).hasText("Product Comparison");
    }

    private Locator comparisonNameRow() {
        return page.locator("#content table tbody tr").filter(
                new Locator.FilterOptions().setHas(page.locator("td").getByText("Product", new Locator.GetByTextOptions().setExact(true))));
    }

    public List<String> comparisonProductNames() {
        Locator names = comparisonNameRow().locator("td a strong");
        assertThat(names.first()).isVisible();
        return names.allTextContents().stream().map(String::trim).toList();
    }

    public String comparisonValue(String label, String productName) {
        int column = comparisonProductNames().indexOf(productName) + 1;
        if (column == 0) throw new AssertionError("Missing comparison product: " + productName);
        // The first cell labels each row; subsequent cells follow the product header order.
        Locator row = page.locator("#content table tbody tr").filter(new Locator.FilterOptions()
                .setHas(page.locator("td").getByText(label, new Locator.GetByTextOptions().setExact(true))));
        return row.locator("td").nth(column).innerText().trim();
    }

    public void removeComparedProduct(String productName) {
        int id = productName.equals(IPHONE.name()) ? IPHONE.id() : MACBOOK.id();
        page.locator("#content a[href*='remove=" + id + "']").click();
    }

    public void addToWishlist(Product product) {
        openProduct(product);
        page.locator("button[onclick=\"wishlist.add('" + product.id() + "');\"]").click();
        assertThat(page.locator(".alert-success")).containsText(product.name());
        // A guest can also see a success-styled message. Only tests of saved rows prove persistence.
    }

    public void openWishlist() {
        page.navigate(baseUrl + "index.php?route=account/wishlist");
    }

    public Locator wishlistRows() {
        return page.locator("#content table tbody tr");
    }

    public Locator wishlistRow(String productName) {
        return wishlistRows().filter(new Locator.FilterOptions().setHas(
                page.getByRole(com.microsoft.playwright.options.AriaRole.LINK,
                        new Page.GetByRoleOptions().setName(productName).setExact(true))));
    }

    public void removeWishlistProduct(String productName) {
        wishlistRow(productName).locator("a[href*='remove=']").click();
    }
}
