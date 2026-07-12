"""Extract transaction tables from text-based bank-statement PDFs."""

from __future__ import annotations

from io import BytesIO

import pandas as pd

from parsers.csv_parser import dataframe_to_transactions


def pdf_bytes_to_transactions(file_bytes: bytes):
    """Return canonical transactions from readable PDF tables.

    This deliberately rejects scanned/image-only and password-protected PDFs,
    because guessing financial rows without extracted table text is unsafe.
    """
    try:
        import pdfplumber
    except ImportError as error:
        raise ValueError("PDF statement processing is unavailable in this runtime.") from error

    try:
        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            transactions = []
            for page in pdf.pages:
                for table in page.extract_tables() or ():
                    frame = _table_to_dataframe(table)
                    if frame is None:
                        continue
                    try:
                        parsed = dataframe_to_transactions(frame)
                    except ValueError:
                        continue
                    transactions.extend(parsed)
    except Exception as error:
        raise ValueError("The PDF could not be read. Use an unlocked, text-based bank statement PDF.") from error

    if not transactions:
        raise ValueError(
            "No transaction table was found in this PDF. Upload a text-based statement PDF or CSV; scanned PDFs require OCR support."
        )
    return transactions


def _table_to_dataframe(table) -> pd.DataFrame | None:
    if not table or len(table) < 2:
        return None
    header = [str(cell or "").strip() for cell in table[0]]
    if not any(header) or len(set(header)) != len(header):
        return None
    rows = [[str(cell or "").strip() for cell in row] for row in table[1:] if row]
    return pd.DataFrame(rows, columns=header) if rows else None
