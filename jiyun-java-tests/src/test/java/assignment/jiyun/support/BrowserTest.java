package assignment.jiyun.support;

import assignment.jiyun.pages.AccountPage;
import assignment.jiyun.pages.CatalogPage;
import com.microsoft.playwright.*;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.TestInfo;
import org.junit.jupiter.api.extension.ExtensionContext;
import org.junit.jupiter.api.extension.RegisterExtension;
import org.junit.jupiter.api.extension.TestWatcher;

import java.io.IOException;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.ZonedDateTime;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.util.Properties;
import java.util.UUID;

/** Browser lifecycle and evidence only; all business assertions live in scenario tests. */
public abstract class BrowserTest {
    // Fictional demo-only credentials. Never use a personal password on the public demo.
    protected static final String PASSWORD = "DemoTesting42!";
    private static final String RUN_ID = System.getProperty("run.id",
            ZonedDateTime.now(ZoneId.of("Australia/Sydney")).format(
                    DateTimeFormatter.ofPattern("yyyyMMdd-HHmmss")) + "-" + UUID.randomUUID().toString().substring(0, 8));
    protected Page page;
    protected AccountPage account;
    protected CatalogPage catalog;
    private Playwright playwright;
    private Browser browser;
    private BrowserContext context;
    private Path evidence;
    private long started;
    private final Properties details = new Properties();

    @RegisterExtension
    final TestWatcher results = new TestWatcher() {
        @Override public void testSuccessful(ExtensionContext ctx) { recordResult("PASS", null); }
        @Override public void testFailed(ExtensionContext ctx, Throwable cause) {
            recordResult(cause instanceof AssertionError ? "FAIL" : "ERROR", cause);
        }
        @Override public void testAborted(ExtensionContext ctx, Throwable cause) { recordResult("ABORTED", cause); }
    };

    @BeforeEach
    void startBrowser(TestInfo info) throws IOException {
        started = System.nanoTime();
        if (!RUN_ID.matches("[A-Za-z0-9_-]+")) {
            throw new IllegalArgumentException("run.id must contain only letters, numbers, underscores or hyphens");
        }
        evidence = Path.of("target", "evidence", RUN_ID,
                getClass().getSimpleName() + "-" + info.getTestMethod().orElseThrow().getName());
        Files.createDirectories(evidence);
        String baseUrl = System.getProperty("base.url", "https://opencart.abstracta.us/");
        // Site-specific selectors and fixtures: do not accidentally create accounts elsewhere.
        if (!baseUrl.matches("https://opencart\\.abstracta\\.us/?")) {
            throw new IllegalArgumentException("These tests target https://opencart.abstracta.us/ only");
        }
        baseUrl = baseUrl.endsWith("/") ? baseUrl : baseUrl + "/";
        details.setProperty("scenario", info.getDisplayName());
        details.setProperty("started.sydney", ZonedDateTime.now(ZoneId.of("Australia/Sydney")).toString());
        details.setProperty("base.url", baseUrl);
        details.setProperty("java.version", System.getProperty("java.version"));
        details.setProperty("os", System.getProperty("os.name") + " " + System.getProperty("os.version"));
        details.setProperty("architecture", System.getProperty("os.arch"));
        details.setProperty("playwright.version", "1.56.0");
        playwright = Playwright.create();
        BrowserType.LaunchOptions options = new BrowserType.LaunchOptions()
                .setHeadless(!Boolean.getBoolean("headed"));
        String channel = System.getProperty("browser.channel", "");
        if (!channel.isBlank()) options.setChannel(channel);
        browser = playwright.chromium().launch(options);
        details.setProperty("browser.version", browser.version());
        details.setProperty("browser.channel", channel.isBlank() ? "bundled-chromium" : channel);
        context = browser.newContext(new Browser.NewContextOptions()
                .setViewportSize(1440, 1000).setLocale("en-US"));
        page = context.newPage();
        page.setDefaultTimeout(15000);
        page.setDefaultNavigationTimeout(45000);
        account = new AccountPage(page, baseUrl);
        catalog = new CatalogPage(page, baseUrl);
    }

    protected String uniqueEmail() {
        return "qa.jiyun." + UUID.randomUUID().toString().replace("-", "") + "@example.com";
    }

    /** Capture important intermediate outcomes before navigating away from them. */
    protected void checkpoint(String name) {
        page.screenshot(new Page.ScreenshotOptions().setPath(evidence.resolve(name + ".png")).setFullPage(true));
    }

    @AfterEach
    void finishBrowser() throws Exception {
        // Attempt every cleanup even if capturing evidence fails; surface any failures to JUnit.
        Exception failure = null;
        try {
            if (page != null && !page.isClosed()) {
                details.setProperty("final.url", page.url());
                checkpoint("final");
                Files.writeString(evidence.resolve("final.html"), page.content());
            }
        } catch (Exception ex) { failure = ex; }
        for (AutoCloseable resource : new AutoCloseable[] {context, browser, playwright}) {
            if (resource != null) {
                try { resource.close(); }
                catch (Exception ex) {
                    if (failure == null) failure = ex;
                    else failure.addSuppressed(ex);
                }
            }
        }
        if (failure != null) throw failure;
    }

    private void recordResult(String status, Throwable error) {
        if (evidence == null) return; // JUnit XML still reports setup failures before directory creation.
        details.setProperty("status", status);
        details.setProperty("duration.seconds", String.format(java.util.Locale.ROOT,
                "%.3f", (System.nanoTime() - started) / 1_000_000_000.0));
        try {
            if (error != null) {
                StringWriter trace = new StringWriter();
                error.printStackTrace(new PrintWriter(trace));
                Files.writeString(evidence.resolve("failure.txt"), trace.toString());
            }
            try (var writer = Files.newBufferedWriter(evidence.resolve("result.properties"))) {
                details.store(writer, "Actual live-site execution; JUnit XML is the authoritative result");
            }
        } catch (IOException ex) {
            // JUnit TestWatcher exceptions are not test failures: report explicitly, never hide this.
            System.err.println("EVIDENCE WRITE ERROR: " + evidence + ": " + ex);
        }
    }
}
