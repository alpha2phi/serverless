import * as mock_graphql from "../mock_graphql";

test("mock_graphql", async () => {
  const event = {
    body: '{order(id:"778899") {customerName}}',
  };

  const response = await mock_graphql.main(event);
  expect(response.statusCode).toEqual(200);
  expect(typeof response.body).toBe("string");
  console.log(response.body);
});
