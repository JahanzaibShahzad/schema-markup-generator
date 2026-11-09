"""Tests for generate_schema.py (stdlib only, run with: python -m unittest test_generate_schema -v)."""

import unittest

from generate_schema import build_article, build_breadcrumbs, build_faqpage, build_localbusiness, parse_args


class TestArticle(unittest.TestCase):
    def test_blogposting_with_all_fields(self):
        args = parse_args(
            [
                "article",
                "--type",
                "BlogPosting",
                "--headline",
                "Local SEO Checklist for 2026",
                "--description",
                "A practical checklist.",
                "--author",
                "Jane Smith",
                "--date-published",
                "2026-11-09",
                "--date-modified",
                "2026-11-09",
                "--image",
                "https://demo.example.com/cover.jpg",
                "--url",
                "https://demo.example.com/blog/local-seo-checklist",
                "--publisher",
                "Demo Agency",
            ]
        )
        schema = build_article(args)
        self.assertEqual(schema["@type"], "BlogPosting")
        self.assertEqual(schema["headline"], "Local SEO Checklist for 2026")
        self.assertEqual(schema["author"], {"@type": "Person", "name": "Jane Smith"})
        self.assertEqual(schema["datePublished"], "2026-11-09")
        self.assertEqual(schema["publisher"], {"@type": "Organization", "name": "Demo Agency"})

    def test_article_defaults_and_empty_fields_dropped(self):
        args = parse_args(["article", "--headline", "Just a headline"])
        schema = build_article(args)
        self.assertEqual(schema["@type"], "Article")
        self.assertEqual(schema["headline"], "Just a headline")
        self.assertNotIn("author", schema)
        self.assertNotIn("description", schema)
        self.assertNotIn("datePublished", schema)
        self.assertNotIn("publisher", schema)

    def test_newsarticle_type(self):
        args = parse_args(
            ["article", "--type", "NewsArticle", "--headline", "Breaking news"]
        )
        self.assertEqual(build_article(args)["@type"], "NewsArticle")


class TestExistingBuilders(unittest.TestCase):
    def test_localbusiness_drops_empty_fields(self):
        args = parse_args(["localbusiness", "--name", "Demo Plumbing Co", "--city", "Austin"])
        schema = build_localbusiness(args)
        self.assertEqual(schema["name"], "Demo Plumbing Co")
        self.assertEqual(schema["address"]["addressLocality"], "Austin")
        self.assertNotIn("telephone", schema)
        self.assertNotIn("streetAddress", schema["address"])

    def test_faqpage_builds_questions(self):
        args = parse_args(
            ["faqpage", "--qa", "What are your hours?We open at 9am.", "--qa", "Free quotes?Yes."]
        )
        schema = build_faqpage(args)
        self.assertEqual(schema["@type"], "FAQPage")
        self.assertEqual(len(schema["mainEntity"]), 2)
        self.assertEqual(schema["mainEntity"][0]["name"], "What are your hours")

    def test_breadcrumbs_positions(self):
        args = parse_args(
            [
                "breadcrumbs",
                "--crumb",
                "Home|https://demo.example.com/",
                "--crumb",
                "Services|https://demo.example.com/services",
            ]
        )
        schema = build_breadcrumbs(args)
        self.assertEqual(schema["itemListElement"][0]["position"], 1)
        self.assertEqual(schema["itemListElement"][1]["position"], 2)


if __name__ == "__main__":
    unittest.main()
