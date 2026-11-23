from __future__ import annotations
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts/sdgds"))
from validate_glossary import validate_terms

class SDGDSTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.terms = json.loads((ROOT / "docs/glossary/terms.json").read_text(encoding="utf-8"))["terms"]

    def test_seed_registry_is_valid(self):
        self.assertEqual(validate_terms(self.terms), [])

    def test_duplicate_term_id_is_rejected(self):
        broken = [dict(x) for x in self.terms]
        broken.append(dict(broken[0]))
        self.assertTrue(any("duplicate term_id" in e for e in validate_terms(broken)))

    def test_malformed_term_id_is_rejected(self):
        broken = [dict(x) for x in self.terms]
        broken[0] = dict(broken[0], term_id="NOT-A-VALID-ID")
        self.assertTrue(any("invalid term_id" in e for e in validate_terms(broken)))

    def test_duplicate_alias_is_rejected(self):
        broken = [dict(x) for x in self.terms]
        broken[0] = dict(broken[0], aliases=["Capability"])
        self.assertTrue(any("collision" in e for e in validate_terms(broken)))

    def test_unresolved_relationship_is_rejected(self):
        broken = [dict(x) for x in self.terms]
        broken[0] = dict(broken[0], related_term_ids=["MISSING-9999"])
        self.assertTrue(any("unresolved related term" in e for e in validate_terms(broken)))

    def test_invalid_source_scheme_is_rejected(self):
        broken = [dict(x) for x in self.terms]
        broken[0] = dict(broken[0], sources=[{"url":"javascript:alert(1)","role":"bad"}])
        self.assertTrue(any("invalid source URL" in e for e in validate_terms(broken)))

    def test_malformed_source_markdown_is_rejected(self):
        broken = [dict(x) for x in self.terms]
        broken[0] = dict(broken[0], sources=[{"url":"https://example.com/path](https://example.com","role":"bad"}])
        self.assertTrue(any("invalid source URL" in e for e in validate_terms(broken)))

    def test_invalid_review_date_is_rejected(self):
        broken = [dict(x) for x in self.terms]
        broken[0] = dict(broken[0], last_reviewed="2026-99-55")
        self.assertTrue(any("last_reviewed" in e for e in validate_terms(broken)))

if __name__ == "__main__":
    unittest.main()
