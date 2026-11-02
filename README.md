# Schema Markup Generator

A simple Python CLI that generates copy-paste ready **JSON-LD** schema markup
for four common page types:

- **LocalBusiness** (name, address, phone, hours, URL)
- **FAQPage** (question/answer pairs)
- **Product** (name, price, currency, availability)
- **BreadcrumbList** (page trail)

Uses only the Python standard library. No dependencies, no API keys, no build step.

## Usage

```bash
python generate_schema.py localbusiness --name "Demo Plumbing Co" \
  --city "Austin" --region "TX" --country "US" \
  --phone "+1-555-0100" --url "https://demo.example.com" \
  --hours "Mo-Fr 09:00-18:00"

python generate_schema.py faqpage \
  --qa "What are your hours?We are open Monday to Friday 9am to 6pm." \
  --qa "Do you offer free quotes?Yes, every quote is free."

python generate_schema.py product --name "Ergonomic Office Chair" \
  --price "249.99" --currency "USD" --url "https://demo.example.com/chair"

python generate_schema.py breadcrumbs \
  --crumb "Home|https://demo.example.com/" \
  --crumb "Services|https://demo.example.com/services"
```

Add `--script` to any command to wrap the output in a ready-to-paste
`<script type="application/ld+json">` tag.

Repeatable flags (`--hours`, `--qa`, `--crumb`) accept multiple values; just
pass the flag again for each entry.

## Validation

Before putting markup on a live page, validate it with Google's
[Rich Results Test](https://search.google.com/test/rich-results) or
[schema.org](https://validator.schema.org/). This tool generates the markup,
but only Google's tools confirm whether a page qualifies for rich results.

## Honest notes

- This generates syntactically valid JSON-LD, but structured data is a hint to
  search engines, not a guarantee of rich results or ranking changes.
- Output is generated locally; no data leaves your machine.
- The examples above use fictional demo businesses. Replace them with your
  real business details.
