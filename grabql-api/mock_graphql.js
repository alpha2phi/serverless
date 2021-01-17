const {
  graphql,
  buildSchema
} = require('graphql');

const schema = buildSchema(`
  type Product {
    id: String!
    name: String!
    price: String!
  }

  type Order {
    id: String!
    customerName: String!
    deliveryAddress: String!
    product: Product!
    quantity: Int!
  }

  type Query {
    product(id: String!): Product
    order(id: String!): Order
  }
`);

const database = require('./mocks/database').default;
const resolvers = {
  order: async ({id}) => {
    const order = await database.orders.get(id);
    if (!order) return null;

    return {
      ...order,
      product: () => database.products.get(order.productId)
    };
  }
};

export const main = async (event) => {
  const result = await graphql(schema, event.body, resolvers);
  return {statusCode: 200, body: JSON.stringify(result.data, null, 2)};
};
