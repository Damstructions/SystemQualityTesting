import { ClientFunction, Selector } from 'testcafe';

const STORE_URL = 'https://opencart.abstracta.us/';
const EMAIL = 'Ag007@temp-mail.io';
const PASSWORD = 'greedisgood10000';
const SHORT_WORD = 'awesome';
const LOGGED_OFF = 'Logged Off';
const PSALM_23 = `The LORD is my shepherd; I shall not want.
He maketh me to lie down in green pastures: he leadeth me beside the still waters.
He restoreth my soul: he leadeth me in the paths of righteousness for his name's sake.
Yea, though I walk through the valley of the shadow of death, I will fear no evil: for thou art with me; thy rod and thy staff they comfort me.
Thou preparest a table before me in the presence of mine enemies: thou anointest my head with oil; my cup runneth over.
Surely goodness and mercy shall follow me all the days of my life: and I will dwell in the house of the LORD for ever.`;
const SONNET_LENGTH = 1000;
const SONNET_18 = `Shall I compare thee to a summer's day?
Thou art more lovely and more temperate:
Rough winds do shake the darling buds of May,
And summer's lease hath all too short a date:
Sometime too hot the eye of heaven shines,
And often is his gold complexion dimm'd;
And every fair from fair sometime declines,
By chance or nature's changing course untrimm'd;
But thy eternal summer shall not fade
Nor lose possession of that fair thou owest;
Nor shall Death brag thou wander'st in his shade,
When in eternal lines to time thou growest:
So long as men can breathe or eyes can see,
So long lives this, and this gives life to thee.`;

const pageUrl = ClientFunction(() => document.location.href);
const hideHostingBadge = ClientFunction(() => {
    document.querySelectorAll('#bitnami-banner, [id*="bitnami"], [class*="bitnami"]').forEach(element => {
        element.remove();
    });
});
const enquiryValue = ClientFunction(() => document.querySelector('#input-enquiry').value);
const revealEnquiry = ClientFunction(() => {
    const field = document.querySelector('#input-enquiry');
    field.style.height = `${field.scrollHeight}px`;
});

function asciiSonnet(length) {
    const poem = SONNET_18.replace(/\r\n/g, '\n');
    let text = '';

    while (text.length < length)
        text += text ? `\n\n${poem}` : poem;

    return text.slice(0, length);
}

function cyclingAlphabet(length) {
    const alphabet = 'abcdefghijklmnopqrstuvwxyz';
    let text = '';

    while (text.length < length)
        text += alphabet;

    return text.slice(0, length);
}

function isStandardAscii(text) {
    return [...text].every(character => character.charCodeAt(0) <= 127);
}

async function openContactForm(t) {
    const contactForm = Selector('legend').withText('Contact Us');

    await t
        .click(Selector('i.fa-phone').parent('a'))
        .expect(contactForm.visible).ok();
}

fixture('Contact us after logon')
    .page('https://opencart.abstracta.us/index.php?route=account/login')
    .beforeEach(async t => {
        const myAccount = Selector('#content h2').withText('My Account');

        await t
            .typeText('#input-email', EMAIL)
            .typeText('#input-password', PASSWORD)
            .click(Selector('#content input[type="submit"]').withAttribute('value', 'Login'))
            .expect(myAccount.visible).ok()
            .expect(pageUrl()).contains('route=account/account');
    });

test('Submit an ASCII word of at most 10 characters', async t => {
    const enquiryError = Selector('.text-danger').withText('Enquiry must be between 10 and 3000 characters!');

    await t
        .expect(SHORT_WORD.length).lte(10)
        .expect(/^[!-~]+$/.test(SHORT_WORD)).ok()
        .expect(isStandardAscii(SHORT_WORD)).ok();

    await openContactForm(t);
    await t
        .typeText('#input-name', 'Ag Seven', { replace: true })
        .typeText('#input-email', EMAIL, { replace: true })
        .typeText('#input-enquiry', SHORT_WORD, { replace: true, paste: true })
        .expect(enquiryValue()).eql(SHORT_WORD);

    await hideHostingBadge();
    await t
        .resizeWindow(1280, 900)
        .takeScreenshot({ path: 'contact-short-word-before-submit.png', fullPage: true })
        .click(Selector('#content input[type="submit"]').withAttribute('value', 'Submit'))
        .expect(pageUrl()).contains('route=information/contact')
        .expect(pageUrl()).notContains('route=information/contact/success')
        .expect(enquiryValue()).eql(SHORT_WORD)
        .expect(enquiryError.visible).ok();

    await hideHostingBadge();
    await t.takeScreenshot({ path: 'contact-short-word-after-submit.png', fullPage: true });
});

test('Submit 1000 ASCII characters from a Shakespeare sonnet', async t => {
    const poem = asciiSonnet(SONNET_LENGTH);
    const successHeading = Selector('#content h1').withText('Contact Us');
    const continueButton = Selector('#content a.btn-primary').withText('Continue');

    await t
        .expect(poem.length).eql(SONNET_LENGTH)
        .expect(isStandardAscii(poem)).ok()
        .expect(poem).contains("Shall I compare thee to a summer's day?");

    await openContactForm(t);
    await t
        .typeText('#input-name', 'Ag Seven', { replace: true })
        .typeText('#input-email', EMAIL, { replace: true })
        .typeText('#input-enquiry', poem, { replace: true, paste: true })
        .expect(enquiryValue()).eql(poem);

    await hideHostingBadge();
    await revealEnquiry();
    await t
        .resizeWindow(1280, 900)
        .takeScreenshot({ path: 'contact-sonnet-before-submit.png', fullPage: true })
        .click(Selector('#content input[type="submit"]').withAttribute('value', 'Submit'))
        .expect(pageUrl()).contains('route=information/contact/success')
        .expect(successHeading.visible).ok()
        .expect(continueButton.visible).ok()
        .expect(Selector('#input-enquiry').exists).notOk();

    await hideHostingBadge();
    await t.takeScreenshot({ path: 'contact-sonnet-after-submit.png', fullPage: true });
});

fixture('Contact us after clearing every cookie')
    .page(STORE_URL);

test('Clear cookies, then submit Logged Off, a 3001-letter cycle, and Psalm 23', async t => {
    const psalm = PSALM_23.replace(/\r\n/g, '\n');
    const overLimit = cyclingAlphabet(3001);
    const successHeading = Selector('#content h1').withText('Contact Us');
    const continueButton = Selector('#content a.btn-primary').withText('Continue');
    const submit = Selector('#content input[type="submit"]').withAttribute('value', 'Submit');
    const enquiryError = Selector('.text-danger').withText('Enquiry must be between 10 and 3000 characters!');

    await t
        .expect(LOGGED_OFF.length).eql(10)
        .expect(isStandardAscii(LOGGED_OFF)).ok()
        .expect(overLimit.length).eql(3001)
        .expect(overLimit.startsWith('abcdefg')).ok()
        .expect(/^[a-z]+$/.test(overLimit)).ok()
        .expect(isStandardAscii(overLimit)).ok()
        .expect(psalm.length).gt(10)
        .expect(psalm.length).lte(3000)
        .expect(isStandardAscii(psalm)).ok()
        .expect(psalm).contains('The LORD is my shepherd');

    await t.deleteCookies();
    const cookies = await t.getCookies();
    await t.expect(cookies.length).eql(0);

    await t
        .navigateTo(`${STORE_URL}index.php?route=account/account`)
        .expect(pageUrl()).contains('route=account/login');

    await openContactForm(t);
    await t
        .typeText('#input-name', 'Ag Seven', { replace: true })
        .typeText('#input-email', EMAIL, { replace: true })
        .typeText('#input-enquiry', LOGGED_OFF, { replace: true, paste: true })
        .expect(enquiryValue()).eql(LOGGED_OFF);

    await hideHostingBadge();
    await t
        .resizeWindow(1280, 900)
        .takeScreenshot({ path: 'contact-logged-off-before-submit.png', fullPage: true })
        .click(submit)
        .expect(pageUrl()).contains('route=information/contact/success')
        .expect(successHeading.visible).ok()
        .expect(continueButton.visible).ok()
        .expect(Selector('#input-enquiry').exists).notOk();

    await hideHostingBadge();
    await t.takeScreenshot({ path: 'contact-logged-off-after-submit.png', fullPage: true });

    await openContactForm(t);
    await t
        .typeText('#input-name', 'Ag Seven', { replace: true })
        .typeText('#input-email', EMAIL, { replace: true })
        .typeText('#input-enquiry', overLimit, { replace: true, paste: true })
        .expect(enquiryValue()).eql(overLimit);

    await hideHostingBadge();
    await revealEnquiry();
    await t
        .resizeWindow(1280, 900)
        .takeScreenshot({ path: 'contact-alphabet-before-submit.png', fullPage: true })
        .click(submit)
        .expect(pageUrl()).contains('route=information/contact')
        .expect(pageUrl()).notContains('route=information/contact/success')
        .expect(enquiryValue()).eql(overLimit)
        .expect(enquiryError.visible).ok();

    await hideHostingBadge();
    await t.takeScreenshot({ path: 'contact-alphabet-after-submit.png', fullPage: true });

    await openContactForm(t);
    await t
        .typeText('#input-name', 'Ag Seven', { replace: true })
        .typeText('#input-email', EMAIL, { replace: true })
        .typeText('#input-enquiry', psalm, { replace: true, paste: true })
        .expect(enquiryValue()).eql(psalm);

    await hideHostingBadge();
    await revealEnquiry();
    await t
        .resizeWindow(1280, 900)
        .takeScreenshot({ path: 'contact-psalm23-before-submit.png', fullPage: true })
        .click(submit)
        .expect(pageUrl()).contains('route=information/contact/success')
        .expect(successHeading.visible).ok()
        .expect(continueButton.visible).ok()
        .expect(Selector('#input-enquiry').exists).notOk();

    await hideHostingBadge();
    await t.takeScreenshot({ path: 'contact-psalm23-after-submit.png', fullPage: true });
});
