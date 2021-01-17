export default {
  products: {
    get: async (id) => {
      switch (id) {
        case "123":
          return {
            id,
            name: "Widget",
            price: "$10.00",
          };
        case "234":
          return {
            id,
            name: "Gadget",
            price: "$8.50"
          };
      }
    }
  },

  orders: {
    get: async (id) => {
      switch (id) {
        case "445566":
          return {
            id,
            customerName: "John Q. Public",
            deliveryAddress: "1234 Elm St.",
            quantity: 5,
            productId: "123"
          };
        case "778899":
          return {
            id,
            customerName: "Stacey L. Civic",
            deliveryAddress: "4321 Oak St.",
            quantity: 32,
            productId: "234"
          };
      }
    }
  }
};
