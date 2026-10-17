# Context

## What this app is
Greeter: a single-page web app that welcomes visitors. Standard library only, no dependencies.

## Architecture
app.py holds the HTTP handler and `home_page(query)`, which returns the page HTML. Tests in tests/ call functions directly.

## Constraints
No third-party packages. Anything echoed from a request must be HTML-escaped.
