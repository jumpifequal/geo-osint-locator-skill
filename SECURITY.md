# Security and Data Handling

Geo OSINT Locator is an analysis skill. It may invoke web, map or geocoding tools only when the active runtime permits them.

## Operational rules

- Do not claim a tool, map, reverse-image, street-level or network action was executed unless it actually ran.
- Keep user-provided images and derived crops scoped to the active task.
- Do not encode conversation-history geography as evidence for a new image.
- Treat external search and map results as evidence to corroborate, not as truth.
- Avoid bulk scraping.
- Preserve `NOT_EXECUTED` when a required runtime action is unavailable.

## Reporting security issues

When publishing this repository, configure a private security-reporting channel appropriate for the hosting organization.
