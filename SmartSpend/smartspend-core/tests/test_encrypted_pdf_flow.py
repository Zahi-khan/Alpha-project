from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from fastapi import HTTPException
from pypdf import PdfWriter
import pandas as pd
from starlette.datastructures import UploadFile

from api.sessions import preview as preview_endpoint
from api.sessions import unlock_and_preview
from application.container import ApplicationContainer
from application.errors.pdf_password_error import (
    InvalidPdfPasswordError,
    PdfPasswordRequiredError,
)
from application.errors.validation_error import ValidationError
from application.sessions.session_manager import SessionManager
from parsers.csv_parser import dataframe_to_transactions
from parsers.pdf_parser import (
    _extract_narration_statement,
    _validated_pdf_password,
    pdf_bytes_to_transactions,
)


def encrypted_pdf(password: str = "bank-secret") -> bytes:
    output = BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    writer.encrypt(password)
    writer.write(output)
    return output.getvalue()


class EncryptedPdfTests(unittest.TestCase):
    def test_encrypted_pdf_reports_password_required(self):
        with self.assertRaises(PdfPasswordRequiredError):
            _validated_pdf_password(encrypted_pdf(), None)

    def test_encrypted_pdf_rejects_incorrect_password(self):
        with self.assertRaises(InvalidPdfPasswordError):
            _validated_pdf_password(encrypted_pdf(), "wrong-password")

    def test_encrypted_pdf_accepts_correct_password_in_memory(self):
        password = "bank-secret"
        self.assertEqual(password, _validated_pdf_password(encrypted_pdf(password), password))

    def test_unlocked_encrypted_pdf_reaches_normal_text_pipeline(self):
        with self.assertRaisesRegex(ValueError, "No transaction table"):
            pdf_bytes_to_transactions(encrypted_pdf(), "bank-secret")


class PreviewLifecycleTests(unittest.TestCase):
    def test_preview_is_session_local_and_consumed_once(self):
        service = ApplicationContainer().statement_service
        sample = Path(__file__).parents[1] / "data" / "sample_transactions.csv"
        preview = service.preview_statement(sample.read_bytes(), "statement.csv")

        self.assertTrue(preview["preview_id"].startswith("preview_"))
        imported = service.import_preview(preview["preview_id"])
        self.assertEqual(preview["total_rows"], imported["total_rows"])
        with self.assertRaises(ValidationError):
            service.import_preview(preview["preview_id"])


class NarrationStatementTests(unittest.TestCase):
    def test_compact_bank_headers_map_to_debit_and_credit_amounts(self):
        frame = pd.DataFrame([
            {"Date": "10/07/26", "Narration": "Card purchase", "WithdrawalAmt.": "100.00", "DepositAmt.": "", "ClosingBalance": "900.00"},
            {"Date": "11/07/26", "Narration": "Refund", "WithdrawalAmt.": "", "DepositAmt.": "200.00", "ClosingBalance": "1100.00"},
        ])

        transactions = dataframe_to_transactions(frame)

        self.assertEqual(2, len(transactions))
        self.assertEqual(-100, transactions[0].amount)
        self.assertEqual(200, transactions[1].amount)
        self.assertEqual("2026-07-10", transactions[0].date.date().isoformat())

    def test_collapsed_narration_table_is_rebuilt_from_word_positions(self):
        class Page:
            width = 638

            @staticmethod
            def extract_text():
                return "Date Narration WithdrawalAmt. DepositAmt. ClosingBalance"

            @staticmethod
            def extract_words(**_kwargs):
                return [
                    {"text": "10/07/26", "x0": 34, "top": 250},
                    {"text": "UPI-TEST", "x0": 72, "top": 250},
                    {"text": "10/07/26", "x0": 362, "top": 250},
                    {"text": "100.00", "x0": 448, "top": 250},
                    {"text": "900.00", "x0": 599, "top": 250},
                    {"text": "11/07/26", "x0": 34, "top": 284},
                    {"text": "REFUND", "x0": 72, "top": 284},
                    {"text": "11/07/26", "x0": 362, "top": 284},
                    {"text": "200.00", "x0": 520, "top": 284},
                    {"text": "1100.00", "x0": 599, "top": 284},
                ]

        pdf = type("Pdf", (), {"pages": [Page()]})()
        transactions = _extract_narration_statement(pdf)

        self.assertEqual(2, len(transactions))
        self.assertEqual(-100, transactions[0].amount)
        self.assertEqual(200, transactions[1].amount)


class EncryptedPdfApiTests(unittest.IsolatedAsyncioTestCase):
    async def test_api_returns_structured_password_required_error(self):
        with TemporaryDirectory() as root:
            manager = SessionManager(root=Path(root))
            session = manager.create()
            upload = UploadFile(file=BytesIO(encrypted_pdf()), filename="statement.pdf")

            with self.assertRaises(HTTPException) as raised:
                await preview_endpoint(session.session_id, upload, manager)

            self.assertEqual(422, raised.exception.status_code)
            self.assertEqual("pdf_password_required", raised.exception.detail["code"])
            self.assertFalse(hasattr(session, "password"))

    async def test_incorrect_password_attempts_are_limited_per_session(self):
        with TemporaryDirectory() as root:
            manager = SessionManager(root=Path(root))
            session = manager.create()
            pdf = encrypted_pdf()

            for attempt in range(1, 6):
                upload = UploadFile(file=BytesIO(pdf), filename="statement.pdf")
                with self.assertRaises(HTTPException) as raised:
                    await unlock_and_preview(session.session_id, upload, "wrong", manager)
                expected = "pdf_password_attempt_limit" if attempt == 5 else "invalid_pdf_password"
                self.assertEqual(expected, raised.exception.detail["code"])

            self.assertEqual(5, session.pdf_password_failures)


if __name__ == "__main__":
    unittest.main()
