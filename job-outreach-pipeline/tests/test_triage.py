import os
import shutil
import tempfile
import unittest
from io import StringIO
from rich.console import Console

import db
from triage import run_review


class TestTriage(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.test_dir, "test.db")
        self.conn = db.connect(self.db_path)
        self.console = Console(file=StringIO(), force_terminal=False)

    def tearDown(self):
        self.conn.close()
        shutil.rmtree(self.test_dir)

    def test_triage_approve_with_primary_contact(self):
        """Approve marks company Approved when primary contact exists."""
        cid, _ = db.upsert_company(self.conn, "Alpha Tech", company_type="ai", status="Pending")
        db.add_contact(self.conn, cid, "lead@alpha.com", full_name="Alice Lead", make_primary=True)

        # Answers: 'A' to approve
        answers = iter(["A"])
        def scripted_ask(prompt, choices=None, default=None):
            return next(answers)

        result = run_review(conn=self.conn, statuses=("Pending",), console=self.console, ask_fn=scripted_ask)
        self.assertEqual(result["approved"], 1)

        row = db.get_company(self.conn, cid)
        self.assertEqual(row["status"], "Approved")

    def test_triage_approve_refused_without_primary_contact(self):
        """Approve refuses when company has no primary contact; user skips instead."""
        cid, _ = db.upsert_company(self.conn, "Beta Tech", company_type="fintech", status="Pending")
        # No primary contact added

        # Answers: try 'A' (refused), then 'S' (skip)
        answers = iter(["A", "S"])
        def scripted_ask(prompt, choices=None, default=None):
            return next(answers)

        result = run_review(conn=self.conn, statuses=("Pending",), console=self.console, ask_fn=scripted_ask)
        self.assertEqual(result["approved"], 0)
        self.assertEqual(result["skipped"], 1)

        row = db.get_company(self.conn, cid)
        self.assertEqual(row["status"], "Skipped")

    def test_triage_skip_action(self):
        """Skip marks company Skipped."""
        cid, _ = db.upsert_company(self.conn, "Gamma Corp", company_type="consultancy", status="Pending")

        answers = iter(["S"])
        def scripted_ask(prompt, choices=None, default=None):
            return next(answers)

        result = run_review(conn=self.conn, statuses=("Pending",), console=self.console, ask_fn=scripted_ask)
        self.assertEqual(result["skipped"], 1)

        row = db.get_company(self.conn, cid)
        self.assertEqual(row["status"], "Skipped")

    def test_triage_edit_manual_contact_and_role_override(self):
        """Edit menu allows adding manual primary contact and overriding role title, then approves."""
        cid, _ = db.upsert_company(self.conn, "Delta Systems", company_type="ai", status="Pending")

        # Session:
        # 1. 'E' -> enter edit menu
        # 2. '2' -> add manual contact
        #    - email: "hr@delta.com"
        #    - name: "David HR"
        #    - title: "Head of Talent"
        #    - kind: "person"
        # 3. 'E' -> enter edit menu again
        # 4. '3' -> override role
        #    - role: "Lead Systems Architect"
        # 5. 'A' -> approve
        answers = iter([
            "E", "2", "hr@delta.com", "David HR", "Head of Talent", "person",
            "E", "3", "Lead Systems Architect",
            "A"
        ])
        def scripted_ask(prompt, choices=None, default=None):
            return next(answers)

        result = run_review(conn=self.conn, statuses=("Pending",), console=self.console, ask_fn=scripted_ask)
        self.assertEqual(result["approved"], 1)

        row = db.get_company(self.conn, cid)
        self.assertEqual(row["status"], "Approved")
        self.assertEqual(row["role_title"], "Lead Systems Architect")

        primary = db.get_primary_contact(self.conn, cid)
        self.assertIsNotNone(primary)
        self.assertEqual(primary["email"], "hr@delta.com")
        self.assertEqual(primary["source"], "manual")

    def test_triage_quit_action(self):
        """Quit exits immediately and returns counts."""
        db.upsert_company(self.conn, "Company 1", status="Pending")
        db.upsert_company(self.conn, "Company 2", status="Pending")

        answers = iter(["Q"])
        def scripted_ask(prompt, choices=None, default=None):
            return next(answers)

        result = run_review(conn=self.conn, statuses=("Pending",), console=self.console, ask_fn=scripted_ask)
        self.assertEqual(result["approved"], 0)
        self.assertEqual(result["skipped"], 0)


if __name__ == "__main__":
    unittest.main()
