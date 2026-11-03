class TestCataloguePagination:
    """T016 / F18 DemoBlaze catalogue Next and Previous"""

    def test_next_shows_a_different_product_list(self, store):
        store.wait_for_catalogue()
        first_page = store.product_titles()
        assert "Samsung galaxy s6" in first_page

        second_page = store.go_to_next_page()
        assert second_page
        assert second_page != first_page
        assert "Samsung galaxy s6" not in second_page
        assert store.page.locator("#prev2").is_visible()

    def test_previous_leaves_the_second_page(self, store):
        store.wait_for_catalogue()
        first_page = store.product_titles()
        second_page = store.go_to_next_page()
        restored = store.go_to_previous_page()

        assert restored != second_page
        assert "Nokia lumia 1520" in restored
        # DEF-ZY-03: Previous after Next skips the original first card.
        assert restored[0] != first_page[0]
        assert "Samsung galaxy s6" not in restored

    def test_next_after_previous_does_not_restore_page_one(self, store):
        store.wait_for_catalogue()
        first_page = store.product_titles()
        store.go_to_next_page()
        store.go_to_previous_page()
        again = store.go_to_next_page()

        assert again
        assert again != first_page
        assert "Samsung galaxy s6" not in again
