from __future__ import annotations
import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts/sdgds"))
from validate_roadmap import validate
class SDGDSRoadmapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads((ROOT/"docs/roadmap/SDGDS-PROGRESS.json").read_text(encoding="utf-8"))
    def test_current_ledger_is_valid(self): self.assertEqual(validate(self.data),[])
    def test_duplicate_work_item_ids_are_rejected(self):
        broken=json.loads(json.dumps(self.data)); broken["work_items"].append(dict(broken["work_items"][0]))
        self.assertTrue(any("duplicate ID" in e for e in validate(broken)))
    def test_unresolved_dependency_is_rejected(self):
        broken=json.loads(json.dumps(self.data)); broken["work_items"][0]["deps"]=["SDGDS-MISSING"]
        self.assertTrue(any("unresolved dependency" in e for e in validate(broken)))
    def test_invalid_evidence_url_is_rejected(self):
        broken=json.loads(json.dumps(self.data)); broken["work_items"][0]["evidence"]=["javascript:alert(1)"]
        self.assertTrue(any("invalid evidence URL" in e for e in validate(broken)))
    def test_overall_completion_is_not_invented(self):
        self.assertIsNone(self.data["progress_measurement"]["overall_completion"])
        self.assertTrue(self.data["progress_measurement"]["overall_completion_reason"])
if __name__=="__main__": unittest.main()
