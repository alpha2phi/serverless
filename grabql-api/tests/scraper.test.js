import * as scraper from "../scraper";
// import fs from "fs";

test("scraper", async () => {
  const event = {
    body: null,
    pathParameters: null,
    queryStringParameters: {
      url: "https://www.google.com",
      width: "800",
      height: "600",
    },
  };

  const context = "context";
  const response = await scraper.pdfScraper(event, context);
  expect(response.statusCode).toEqual(200);

  // fs.writeFile("generated/output.pdf", response.body, (err) => {
  //   if (err) throw err;
  // });
});
