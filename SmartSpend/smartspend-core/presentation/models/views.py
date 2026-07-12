"""Immutable frontend-neutral presentation models."""

from __future__ import annotations

from dataclasses import field
from typing import Any

from models._dataclasses import slotted_dataclass


@slotted_dataclass(frozen=True)
class MetricCardView:
    id: str; label: str; value: Any; formatted_value: str; supporting_text: str = ""; tone: str = "neutral"; icon_key: str = "metric"; action: dict[str, str] | None = None

@slotted_dataclass(frozen=True)
class InsightView:
    id: str; type: str; title: str; summary: str; primary_metric: str | None; severity: str; tone: str; confidence: float; confidence_label: str; evidence_preview: tuple[str, ...]; tags: tuple[str, ...]; generated_at: Any; action: dict[str, str]

@slotted_dataclass(frozen=True)
class TransactionView:
    id: str | None; date: str | None; formatted_date: str | None; merchant_name: str | None; fallback_description: str; original_description: str | None; category_name: str | None; spending_type: str; industry_name: str | None; payment_name: str | None; payment_initiator: str | None; counterparty: str | None; beneficiary_vpa: str | None; payment_reference: str | None; merchant_visibility: str | None; source_type: str | None; statement_reference: str | None; balance: str | None; amount: Any; formatted_amount: str; direction: str; confidence_label: str; warning_flags: tuple[str, ...] = (); review_required: bool = False

@slotted_dataclass(frozen=True)
class ChartSeries:
    id: str; label: str; values: tuple[dict[str, Any], ...]; tone_key: str = "primary"; unit: str = "currency"

@slotted_dataclass(frozen=True)
class ChartView:
    id: str; type: str; title: str; series: tuple[ChartSeries, ...] = (); empty_state: dict[str, str] | None = None; accessibility_summary: str = ""

@slotted_dataclass(frozen=True)
class DashboardView:
    session: dict[str, Any]; summary_cards: tuple[MetricCardView, ...]; top_insights: tuple[InsightView, ...]; conclusions: tuple[dict[str, Any], ...]; charts: tuple[ChartView, ...]; data_quality: dict[str, Any]; generated_at: Any

@slotted_dataclass(frozen=True)
class ExplanationView:
    title: str; plain_language_summary: str; steps: tuple[str, ...]; related_transactions: tuple[str, ...]; technical_trace_available: bool = True

@slotted_dataclass(frozen=True)
class SessionView:
    session_id: str; status: str; status_label: str; current_stage: str; expires_at: Any; report_ready: bool; can_download: bool; privacy_message: str
