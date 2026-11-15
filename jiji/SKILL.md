---
name: jiji
description: Search Jiji Nigeria live listings through its public API, with current filters and listing vetting.
---

Search Jiji Nigeria directly with its live public listings endpoint:

`https://jiji.ng/api_web/v1/listing?query=<URL-encoded search>`

Use URL query parameters to narrow results:

- `region_id=119` for Lagos State; obtain current region IDs from `https://jiji.ng/api_web/v1/regions.json`
- `slug=<category-slug>` for a category, such as `cameras-video-cameras-and-accessories`, `watches`, or `172-flash-drives`
- `price_min=<naira>` and `price_max=<naira>`
- `sort=newest` when recency matters
- `page=<number>`; prefer the response's `next_url` when present, since it carries the current listing session parameters
- category filters such as `filter_attr_243_condition=Used` and `filter_attr_245_type=DSLR%20Cameras`

Discover the valid category slug and current filter parameter names/values before using category filters:

`https://jiji.ng/api_web/v1/attributes/update-filters?slug=<category-slug>&region_id=<region-id>`

Use `https://jiji.ng/api_web/v1/search_suggest?term=<URL-encoded search>` for live query suggestions.

For each listing, return its title, price, location, condition, seller history/rating where available, and canonical link (`https://jiji.ng` plus the API response's `url`). Check the ad page directly before recommending it: confirm the item specs match the claimed model, the listing has seller-owned photos, seller tenure/feedback is meaningful, and the price is within the normal range for comparable local listings. Exclude anomalously cheap listings, contradictory specifications, incomplete bundles, and likely counterfeit claims from quality/price recommendations.

Do not place orders, message sellers, provide payments, or advise paying in advance. Remind buyers to inspect and test items in person; for batteries, storage, cameras, and power banks, require the exact model/specification and a functional test before payment.
