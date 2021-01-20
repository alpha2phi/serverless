import pdfHandler from "./libs/pdf-handler-lib";
import pngHandler from "./libs/png-handler-lib";
import chromium from "chrome-aws-lambda";

export const pdfScraper = pdfHandler(async (event, context) => {
  let browser = null;
  try {
    if (
      !event.queryStringParameters ||
      !event.queryStringParameters.url ||
      event.queryStringParameters.url.length === 0
    ) {
      throw new Error("Please supply a valid URL");
    }
    const params = {
      url: event.queryStringParameters.url,
      width: Number.parseInt(event.queryStringParameters.width) || 1920,
      height: Number.parseInt(event.queryStringParameters.height) || 1080,
    };

    if (!params.url.startsWith("http")) {
      params.url = "https://" + params.url;
    }

    browser = await chromium.puppeteer.launch({
      headless: chromium.headless,
      args: chromium.args,
      ignoreHTTPSErrors: true,
      defaultViewport: chromium.defaultViewport,
      executablePath: await chromium.executablePath,
    });

    const webpage = await browser.newPage();
    if (params.width > 0 && params.height > 0) {
      await webpage.setViewport({ width: params.width, height: params.height });
    }
    await webpage.goto(params.url, { waitUntil: "networkidle0" });
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
    return pdf;
  } catch (error) {
    throw new Error(error.message);
  } finally {
    if (browser !== null) {
      await browser.close();
    }
  }
});

export const pngScraper = pngHandler(async (event, context) => {
  let browser = null;
  try {
    if (
      !event.queryStringParameters ||
      !event.queryStringParameters.url ||
      event.queryStringParameters.url.length === 0
    ) {
      throw new Error("Please supply a valid URL");
    }
    const params = {
      url: event.queryStringParameters.url,
      width: Number.parseInt(event.queryStringParameters.width) || 1920,
      height: Number.parseInt(event.queryStringParameters.height) || 1080,
    };

    if (!params.url.startsWith("http")) {
      params.url = "https://" + params.url;
    }

    browser = await chromium.puppeteer.launch({
      headless: chromium.headless,
      args: chromium.args,
      ignoreHTTPSErrors: true,
      defaultViewport: chromium.defaultViewport,
      executablePath: await chromium.executablePath,
    });

    const webpage = await browser.newPage();
    if (params.width > 0 && params.height > 0) {
      await webpage.setViewport({ width: params.width, height: params.height });
    }
    await webpage.goto(params.url, { waitUntil: "networkidle0" });

    console.log(params);
    const png = await webpage.screenshot({
      fullPage: true,
    });
    return png;
  } catch (error) {
    throw new Error(error.message);
  } finally {
    if (browser !== null) {
      await browser.close();
    }
  }
});
