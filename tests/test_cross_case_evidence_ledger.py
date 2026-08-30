import unittest

from scripts.cross_case_evidence_ledger import _fmt


class CrossCaseEvidenceLedgerTests(unittest.TestCase):
    def test_format_handles_missing_and_numbers(self):
        self.assertEqual(_fmt(None), "—")
        self.assertEqual(_fmt(-0.123456), "-0.1235")


if __name__ == "__main__":
    unittest.main()
