package tests;

import support.BrowserTest;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

@Tag("carousel")
@DisplayName("TC-JT-CAROUSEL Homepage promotional carousel")
class CarouselTest extends BrowserTest {
    @Test
    @DisplayName("CAROUSEL-01 Next displays each banner and wraps from the last to the first")
    void nextWrapsToFirstSlide() {
        home.prepareCarousel();
        for (int expected : new int[] {1, 2, 0}) {
            home.nextSlide();
            home.assertSlide(expected);
        }
    }

    @Test
    @DisplayName("CAROUSEL-02 Previous wraps from the first banner to the last and moves backwards")
    void previousWrapsToLastSlide() {
        home.prepareCarousel();
        for (int expected : new int[] {2, 1, 0}) {
            home.previousSlide();
            home.assertSlide(expected);
        }
    }

    @Test
    @DisplayName("CAROUSEL-03 Indicators select their corresponding banner out of sequence")
    void indicatorsSelectCorrectSlide() {
        home.prepareCarousel();
        // Check the image AND indicator, not just whether any banner remains visible.
        for (int expected : new int[] {2, 0, 1}) {
            home.selectSlide(expected);
            home.assertSlide(expected);
        }
    }
}
