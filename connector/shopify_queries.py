"""
GraphQL queries for Shopify.
"""

ORDERS_QUERY = """
query Orders($first: Int!, $after: String, $query: String!) {
  orders(
    first: $first,
    after: $after,
    query: $query,
    sortKey: CREATED_AT,
    reverse: false
  ) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      id
      name
      createdAt
      displayFinancialStatus
      displayFulfillmentStatus
      tags

      shippingAddress {
        firstName
        lastName
        company
        address1
        address2
        city
        zip
        countryCodeV2
        phone
      }

      billingAddress {
        firstName
        lastName
        company
        address1
        address2
        city
        zip
        countryCodeV2
        phone
      }

      totalPriceSet {
        shopMoney {
          amount
          currencyCode
        }
      }

      totalTaxSet {
        shopMoney {
          amount
          currencyCode
        }
      }

      totalShippingPriceSet {
        shopMoney {
          amount
          currencyCode
        }
      }

      lineItems(first: 100) {
        nodes {
          title
          quantity
          sku
          variant {
            sku
          }
          fulfillmentStatus
        }
      }
    }
  }
}
""".strip()
