import handler from "./libs/pdf-handler-lib";
import chromium from "chrome-aws-lambda";

export const main = handler(async (event, context) => {
  const executablePath = process.env.DEBUG
    ? null
    : await chromium.executablePath;

  console.log("executable is ", executablePath);
  const browser = await chromium.puppeteer.launch({
    headless: true,
    args: chromium.args,
    defaultViewport: chromium.defaultViewport,
    executablePath,
  });

  const webpage = await browser.newPage();

  // await webpage.setViewport({ width: 1200, height:800 });

  const url = "https://www.google.com";

  await webpage.goto(url, { waitUntil: "networkidle0" });

  const pdf = await webpage.pdf({
    printBackground: true,
    format: "Letter",
    margin: {
      top: "20px",
      bottom: "20px",
      left: "20px",
      right: "20px",
    },
  });

  await browser.close();

  return pdf;
});
