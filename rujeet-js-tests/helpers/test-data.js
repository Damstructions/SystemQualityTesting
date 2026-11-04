const PASSWORD = "DemoTesting42!";

function uniqueEmail() {
  const timestamp = Date.now();
  const randomValue = Math.random().toString(16).slice(2);

  return `qa.rujeet.${timestamp}.${randomValue}@example.com`;
}

module.exports = {
  PASSWORD,
  uniqueEmail,
};
