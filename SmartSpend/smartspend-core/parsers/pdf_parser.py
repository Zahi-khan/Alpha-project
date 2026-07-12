"""Extract transaction tables from text-based bank-statement PDFs."""

from __future__ import annotations

from io import BytesIO
import re

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
            if not transactions:
                transactions = _extract_positioned_transaction_history(pdf)
    except Exception as error:
        raise ValueError("The PDF could not be read. Use an unlocked, text-based bank statement PDF.") from error

    if not transactions:
        raise ValueError(
            "No transaction table was found in this PDF. Upload a text-based statement PDF or CSV; scanned PDFs require OCR support."
        )
    return transactions


_DATE = re.compile(r"^\d{2}[./-]\d{2}[./-]\d{4}$")
_AMOUNT = re.compile(r"^-?[\d,]+(?:\.\d{1,2})?$")


def _extract_positioned_transaction_history(pdf):
    """Read bank PDFs whose visual rows are text-positioned instead of table-tagged.

    ICICI transaction-history exports use this layout: date and serial on the
    left, remarks in the centre, then withdrawal, deposit, and balance columns.
    """
    records = []
    for page in pdf.pages:
        words = page.extract_words(x_tolerance=2, y_tolerance=2)
        dates = [word for word in words if word["x0"] < 125 and _DATE.fullmatch(word["text"])]
        for index, date_word in enumerate(dates):
            top = date_word["top"]
            next_top = dates[index + 1]["top"] if index + 1 < len(dates) else float("inf")
            row_words = [word for word in words if abs(word["top"] - top) <= 3]
            withdrawal = _amount_in_column(row_words, 380, 460)
            deposit = _amount_in_column(row_words, 460, 530)
            balance = _amount_in_column(row_words, 530, 590)
            if withdrawal is None and deposit is None:
                continue
            remarks = _remarks_between(words, top - 6, next_top - 6)
            if not remarks:
                continue
            vendor = remarks[0]
            full_remarks = " ".join(remarks)
            amount = deposit if deposit is not None else f"-{withdrawal}"
            records.append({
                "Date": date_word["text"],
                "Description": full_remarks,
                "Vendor": vendor,
                "Amount": amount,
                "Balance": balance or "",
                "Mode": _payment_mode(full_remarks),
                "Type": "Credit" if deposit is not None else "Debit",
            })
    if not records:
        return []
    return dataframe_to_transactions(pd.DataFrame(records))


def _amount_in_column(words, start: float, end: float) -> str | None:
    candidates = [word["text"] for word in words if start <= word["x0"] < end and _AMOUNT.fullmatch(word["text"])]
    return candidates[-1].replace(",", "") if candidates else None


def _remarks_between(words, start_top: float, end_top: float) -> list[str]:
    selected = [word for word in words if 185 <= word["x0"] < 390 and start_top <= word["top"] < end_top]
    lines: dict[float, list[dict]] = {}
    for word in selected:
        lines.setdefault(round(word["top"], 1), []).append(word)
    return [" ".join(word["text"] for word in sorted(line, key=lambda item: item["x0"])) for _, line in sorted(lines.items())]


def _payment_mode(remarks: str) -> str:
    upper = remarks.upper()
    for marker, mode in (("UPI", "UPI"), ("NEFT", "NEFT"), ("IMPS", "IMPS"), ("RTGS", "RTGS"), ("CARD", "Card")):
        if marker in upper:
            return mode
    return "Unknown"


def _table_to_dataframe(table) -> pd.DataFrame | None:
    if not table or len(table) < 2:
        return None
    header = [str(cell or "").strip() for cell in table[0]]
    if not any(header) or len(set(header)) != len(header):
        return None
    rows = [[str(cell or "").strip() for cell in row] for row in table[1:] if row]
    return pd.DataFrame(rows, columns=header) if rows else None
