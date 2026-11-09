#!/usr/bin/env python3
"""Schema Markup Generator.

A simple Python CLI that builds copy-paste ready JSON-LD schema markup
for common page types: LocalBusiness, FAQPage, Product, BreadcrumbList
and Article (Article, BlogPosting, NewsArticle).

Only the Python standard library is used, so no dependencies are needed.
"""

import argparse
import json
import sys

SCRIPT_TEMPLATE = '<script type="application/ld+json">\n{body}\n</script>'


def output_json_ld(data, wrap_script=False):
    """Print the schema as pretty JSON-LD, optionally wrapped in a script tag."""
    body = json.dumps(data, indent=2, ensure_ascii=False)
    if wrap_script:
        print(SCRIPT_TEMPLATE.format(body=body))
    else:
        print(body)


def build_localbusiness(args):
    """Build LocalBusiness JSON-LD."""
    address = {
        "@type": "PostalAddress",
        "streetAddress": args.street,
        "addressLocality": args.city,
        "addressRegion": args.region,
        "postalCode": args.postal_code,
        "addressCountry": args.country,
    }
    # Drop empty address fields so output stays clean.
    address = {k: v for k, v in address.items() if v}

    business = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": args.name,
        "url": args.url,
        "telephone": args.phone,
        "address": address,
    }
    business = {k: v for k, v in business.items() if v}

    if args.hours:
        # Accept one or more values like "Mo-Fr 09:00-18:00".
        business["openingHours"] = args.hours
    if args.image:
        business["image"] = args.image
    if args.price_range:
        business["priceRange"] = args.price_range
    return business


def build_faqpage(args):
    """Build FAQPage JSON-LD from Q/A pairs."""
    questions = []
    for pair in args.qa:
        if "?" not in pair:
            sys.exit("Error: each --qa pair must use the format 'Question?Answer'")
        question, answer = pair.split("?", 1)
        question = question.strip()
        answer = answer.strip()
        if not question or not answer:
            sys.exit("Error: each --qa pair needs a non-empty question and answer.")
        questions.append(
            {
                "@type": "Question",
                "name": question,
                "acceptedAnswer": {"@type": "Answer", "text": answer},
            }
        )
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": questions,
    }


def build_product(args):
    """Build Product JSON-LD with an offer."""
    offer = {
        "@type": "Offer",
        "price": args.price,
        "priceCurrency": args.currency,
        "availability": "https://schema.org/" + args.availability,
        "url": args.url,
    }
    product = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": args.name,
        "description": args.description,
        "image": args.image,
        "offers": offer,
    }
    return {k: v for k, v in product.items() if v}


def build_article(args):
    """Build Article/BlogPosting/NewsArticle JSON-LD."""
    article = {
        "@context": "https://schema.org",
        "@type": args.article_type,
        "headline": args.headline,
        "description": args.description,
        "author": {"@type": "Person", "name": args.author} if args.author else None,
        "datePublished": args.date_published,
        "dateModified": args.date_modified,
        "image": args.image,
        "url": args.url,
        "publisher": (
            {"@type": "Organization", "name": args.publisher} if args.publisher else None
        ),
    }
    return {k: v for k, v in article.items() if v}


def build_breadcrumbs(args):
    """Build BreadcrumbList JSON-LD from 'Name|URL' crumbs."""
    items = []
    for position, crumb in enumerate(args.crumb, start=1):
        if "|" not in crumb:
            sys.exit("Error: each --crumb must use the format 'Name|URL'")
        name, url = crumb.split("|", 1)
        name = name.strip()
        url = url.strip()
        if not name or not url:
            sys.exit("Error: each --crumb needs a non-empty name and URL.")
        items.append(
            {
                "@type": "ListItem",
                "position": position,
                "name": name,
                "item": url,
            }
        )
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items,
    }


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description=(
            "Generate copy-paste ready JSON-LD schema markup "
            "(LocalBusiness, FAQPage, Product, BreadcrumbList)."
        )
    )
    parser.add_argument(
        "--script",
        action="store_true",
        help="Wrap the output in a <script type=\"application/ld+json\"> tag.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    script_parent = argparse.ArgumentParser(add_help=False)
    script_parent.add_argument(
        "--script",
        action="store_true",
        help="Wrap the output in a <script type=\"application/ld+json\"> tag.",
    )

    lb = sub.add_parser(
        "localbusiness", parents=[script_parent], help="Generate LocalBusiness schema."
    )
    lb.add_argument("--name", required=True, help="Business name.")
    lb.add_argument("--url", help="Business website URL.")
    lb.add_argument("--phone", help="Business phone number.")
    lb.add_argument("--street", help="Street address.")
    lb.add_argument("--city", help="City.")
    lb.add_argument("--region", help="State or region.")
    lb.add_argument("--postal-code", help="Postal code.")
    lb.add_argument("--country", help="Country (e.g. US, UK, PK).")
    lb.add_argument(
        "--hours",
        action="append",
        metavar='"Mo-Fr 09:00-18:00"',
        help="Opening hours; repeatable, e.g. --hours \"Mo-Fr 09:00-18:00\".",
    )
    lb.add_argument("--image", help="Business logo or photo URL.")
    lb.add_argument("--price-range", help="Price range, e.g. '$$'.")

    faq = sub.add_parser("faqpage", parents=[script_parent], help="Generate FAQPage schema.")
    faq.add_argument(
        "--qa",
        required=True,
        action="append",
        metavar='"Question?Answer"',
        help="One question/answer pair; repeatable.",
    )

    prod = sub.add_parser("product", parents=[script_parent], help="Generate Product schema.")
    prod.add_argument("--name", required=True, help="Product name.")
    prod.add_argument("--description", help="Product description.")
    prod.add_argument("--price", required=True, help="Product price, e.g. 49.99.")
    prod.add_argument("--currency", default="USD", help="Currency code (default USD).")
    prod.add_argument(
        "--availability",
        default="InStock",
        choices=["InStock", "OutOfStock", "PreOrder", "Discontinued"],
        help="Availability status (default InStock).",
    )
    prod.add_argument("--url", help="Product page URL.")
    prod.add_argument("--image", help="Product image URL.")

    crumbs = sub.add_parser("breadcrumbs", parents=[script_parent], help="Generate BreadcrumbList schema.")
    crumbs.add_argument(
        "--crumb",
        required=True,
        action="append",
        metavar='"Name|URL"',
        help="One breadcrumb; repeatable, in page order.",
    )

    art = sub.add_parser("article", parents=[script_parent], help="Generate Article schema.")
    art.add_argument(
        "--type",
        dest="article_type",
        default="Article",
        choices=["Article", "BlogPosting", "NewsArticle"],
        help="Schema type (default Article).",
    )
    art.add_argument("--headline", required=True, help="Article headline.")
    art.add_argument("--description", help="Short article description.")
    art.add_argument("--author", help="Author name.")
    art.add_argument("--date-published", help="Publish date, e.g. 2026-11-09.")
    art.add_argument("--date-modified", help="Last modified date, e.g. 2026-11-09.")
    art.add_argument("--image", help="Featured image URL.")
    art.add_argument("--url", help="Article page URL.")
    art.add_argument("--publisher", help="Publisher organization name.")

    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    builders = {
        "localbusiness": build_localbusiness,
        "faqpage": build_faqpage,
        "product": build_product,
        "breadcrumbs": build_breadcrumbs,
        "article": build_article,
    }
    schema = builders[args.command](args)
    output_json_ld(schema, wrap_script=args.script)


if __name__ == "__main__":
    main()
