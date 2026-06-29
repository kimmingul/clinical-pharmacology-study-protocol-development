from html.parser import HTMLParser
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PAGE = REPO_ROOT / "docs" / "index.html"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.html_lang = None
        self.ids = set()
        self.hrefs = []
        self.meta_descriptions = []
        self.text_parts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.html_lang = attrs.get("lang")
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("href"):
            self.hrefs.append(attrs["href"])
        if tag == "meta" and attrs.get("name") == "description":
            self.meta_descriptions.append(attrs.get("content", ""))

    def handle_data(self, data):
        text = data.strip()
        if text:
            self.text_parts.append(text)


def parse_page():
    parser = PageParser()
    parser.feed(PAGE.read_text(encoding="utf-8"))
    return parser


class GitHubPagesTest(unittest.TestCase):
    def test_github_pages_entrypoint_and_nojekyll_exist(self):
        self.assertTrue(PAGE.exists())
        self.assertTrue((REPO_ROOT / "docs" / ".nojekyll").exists())

    def test_page_has_korean_metadata_and_primary_sections(self):
        parser = parse_page()
        page_text = " ".join(parser.text_parts)

        self.assertEqual(parser.html_lang, "ko")
        self.assertIn("임상약리 임상시험 계획서 개발", parser.meta_descriptions[0])
        self.assertTrue(
            {"top", "features", "workflow", "safety", "install", "release"}.issubset(
                parser.ids
            )
        )
        self.assertIn("임상약리 임상시험 계획서 개발을", page_text)
        self.assertIn("조사부터 검증까지 한 흐름으로", page_text)
        self.assertIn("AI 생성물은 전문가 검토와 IRB 승인이 필요한 초안입니다", page_text)

    def test_page_links_to_repository_release_and_installation_flow(self):
        parser = parse_page()
        page_text = " ".join(parser.text_parts)

        self.assertIn(
            "https://github.com/kimmingul/clinical-pharmacology-study-protocol-development",
            parser.hrefs,
        )
        self.assertIn(
            "https://github.com/kimmingul/clinical-pharmacology-study-protocol-development/releases/latest",
            parser.hrefs,
        )
        self.assertIn(
            "/plugin marketplace add kimmingul/clinical-pharmacology-study-protocol-development",
            page_text,
        )
        self.assertIn("v4.2.0", page_text)


if __name__ == "__main__":
    unittest.main()
