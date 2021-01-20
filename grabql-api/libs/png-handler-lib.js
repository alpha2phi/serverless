import * as debug from "./debug-lib";

export default function handler(lambda) {
  return async function (event, context) {
    let body, statusCode;

    // Start debugger
    debug.init(event, context);

    try {
      // Run the Lambda
      body = await lambda(event, context);
      statusCode = 200;
    } catch (e) {
      // Print debug messages
      debug.flush(e);
      body = { error: e.message };
      statusCode = 500;

      return {
        statusCode,
        body: JSON.stringify(body),
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Credentials": true,
        },
      };
    }

    // Return HTTP response
    return {
      statusCode,
      body: body.toString("base64"),
      isBase64Encoded: true,
      headers: {
        "Content-Type": "image/png",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": true,
      },
    };
  };
}
