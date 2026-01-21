# AI Notes

AI tooling was used as an implementation accelerator, not as a substitute for design or reasoning.

## How AI was used
- To generate initial file scaffolding and function stubs.
- To draft GraphQL queries and boilerplate client code.
- To iterate quickly on repetitive or mechanical transformations.

## How AI was controlled
- All core decisions (architecture, filtering rules, payload shape, trade-offs) were made manually.
- AI-generated code was reviewed, corrected, and refined before being accepted.
- Schema alignment and edge-case handling (partial fulfillment, tag priority, defensive filtering) were implemented deliberately rather than inferred.

## Key human decisions
- Keeping the connector as a dry-run only, as requested.
- Defensive filtering of orders with inconsistent Shopify states.
- Best-effort mapping to the everstox payload schema with explicit placeholders.
- Choosing synchronous HTTP for clarity and reliability under time constraints.

## What I would improve with more time
- Add unit tests around tag parsing and filtering.
- Introduce schema validation for the outgoing payload.
- Make date range and pagination parameters configurable.
- Separate payload mapping behind a versioned interface to handle schema changes.
