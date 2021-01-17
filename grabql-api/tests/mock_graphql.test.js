import * as hello from '../hello';

test('mock_graphql', async () => {
  const database = require('../mocks/database');
  console.log("database is ", database);
  const order = await database.orders.get("778899");
  console.log("order is ", order);
});
