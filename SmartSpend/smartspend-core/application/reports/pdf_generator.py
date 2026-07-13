"""Generate a spacious, chart-led summary without exposing raw statement rows."""

from __future__ import annotations

from html import escape
from pathlib import Path

from application.errors.processing_error import ProcessingError


class PDFGenerator:
    def generate(self, report, output_path: Path) -> Path:
        try:
            from reportlab.graphics.shapes import Circle, Drawing, Line, Path as DrawingPath, Rect, String
            from reportlab.lib import colors
            from reportlab.lib.enums import TA_CENTER
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
            from reportlab.lib.units import mm
            from reportlab.platypus import (
                KeepTogether,
                PageBreak,
                Paragraph,
                SimpleDocTemplate,
                Spacer,
                Table,
                TableStyle,
            )
        except ImportError as error:
            raise ProcessingError("PDF report generation is unavailable in this runtime.") from error

        output_path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        palette = {
            "ink": colors.HexColor("#202521"),
            "muted": colors.HexColor("#667068"),
            "green": colors.HexColor("#254D45"),
            "green_soft": colors.HexColor("#E5ECE8"),
            "paper": colors.HexColor("#F7F8F5"),
            "line": colors.HexColor("#D7DDD8"),
            "warning": colors.HexColor("#9A6B28"),
        }
        base = getSampleStyleSheet()
        styles = {
            "title": ParagraphStyle("ReportTitle", parent=base["Title"], fontName="Helvetica-Bold", fontSize=25, leading=31, textColor=palette["ink"], spaceAfter=12),
            "subtitle": ParagraphStyle("ReportSubtitle", parent=base["BodyText"], fontName="Helvetica", fontSize=10.5, leading=17, textColor=palette["muted"], spaceAfter=18),
            "section": ParagraphStyle("Section", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=16, leading=21, textColor=palette["ink"], spaceBefore=8, spaceAfter=8),
            "section_note": ParagraphStyle("SectionNote", parent=base["BodyText"], fontName="Helvetica", fontSize=9.5, leading=15, textColor=palette["muted"], spaceAfter=16),
            "metric_label": ParagraphStyle("MetricLabel", parent=base["BodyText"], fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=palette["green"], spaceAfter=7),
            "metric_value": ParagraphStyle("MetricValue", parent=base["BodyText"], fontName="Helvetica-Bold", fontSize=17, leading=21, textColor=palette["ink"], spaceAfter=6),
            "metric_note": ParagraphStyle("MetricNote", parent=base["BodyText"], fontName="Helvetica", fontSize=8.5, leading=13, textColor=palette["muted"]),
            "item_title": ParagraphStyle("ItemTitle", parent=base["Heading3"], fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=palette["ink"], spaceAfter=6),
            "body": ParagraphStyle("Body", parent=base["BodyText"], fontName="Helvetica", fontSize=9.5, leading=15, textColor=palette["muted"], spaceAfter=12),
            "privacy": ParagraphStyle("Privacy", parent=base["BodyText"], fontName="Helvetica", fontSize=8.5, leading=14, textColor=palette["muted"]),
            "empty": ParagraphStyle("Empty", parent=base["BodyText"], fontName="Helvetica-Oblique", fontSize=9.5, leading=15, textColor=palette["muted"], alignment=TA_CENTER),
        }

        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=A4,
            title="SmartSpend Financial Summary",
            author="RK SmartSpend",
            leftMargin=18 * mm,
            rightMargin=18 * mm,
            topMargin=20 * mm,
            bottomMargin=18 * mm,
        )

        def page_frame(canvas, document):
            canvas.saveState()
            width, _ = A4
            canvas.setFont("Helvetica", 7.5)
            canvas.setFillColor(palette["muted"])
            canvas.setStrokeColor(palette["line"])
            canvas.line(document.leftMargin, 11 * mm, width - document.rightMargin, 11 * mm)
            canvas.drawString(document.leftMargin, 6.5 * mm, "Aggregated findings only - raw statement rows are excluded")
            canvas.drawRightString(width - document.rightMargin, 6.5 * mm, f"Page {document.page}")
            canvas.restoreState()

        def plain(value) -> str:
            return str(value or "").replace("₹", "INR ").replace("–", "-").replace("—", "-").replace("‑", "-").replace("…", "...")

        def text(value) -> str:
            return escape(plain(value))

        def currency(value) -> str:
            number = float(value or 0)
            sign = "-" if number < 0 else ""
            return f"{sign}INR {abs(number):,.0f}"

        def chart_values(chart_id: str):
            chart = next((item for item in report.charts if item.get("id") == chart_id), None)
            if not chart or not chart.get("series"):
                return []
            return [(str(point.get("x", "")), float(point.get("y", 0))) for point in chart["series"][0].get("values", ())]

        def bar_chart(values, color=None):
            values = sorted(values, key=lambda item: abs(item[1]), reverse=True)[:6]
            if not values:
                return Paragraph("Not enough grouped data is available for this chart.", styles["empty"])
            height = 18 + len(values) * 40
            drawing = Drawing(doc.width, height)
            maximum = max(abs(value) for _, value in values) or 1
            for index, (label, value) in enumerate(values):
                y = height - 16 - index * 40
                drawing.add(String(0, y, plain(label)[:42], fontName="Helvetica", fontSize=8.5, fillColor=palette["ink"]))
                drawing.add(String(doc.width, y, currency(value), fontName="Helvetica-Bold", fontSize=8.5, fillColor=palette["ink"], textAnchor="end"))
                drawing.add(Rect(0, y - 17, doc.width, 7, rx=3.5, ry=3.5, fillColor=palette["line"], strokeColor=None))
                drawing.add(Rect(0, y - 17, max(4, doc.width * abs(value) / maximum), 7, rx=3.5, ry=3.5, fillColor=color or palette["green"], strokeColor=None))
            return drawing

        def line_chart(values):
            if not values:
                return Paragraph("Not enough monthly history is available for a trend chart.", styles["empty"])
            drawing = Drawing(doc.width, 175)
            left, right, bottom, top = 42, doc.width - 8, 30, 152
            amounts = [value for _, value in values]
            low, high = min(amounts + [0]), max(amounts + [0])
            if high == low:
                high = low + 1
            for step in range(4):
                y = bottom + (top - bottom) * step / 3
                drawing.add(Line(left, y, right, y, strokeColor=palette["line"], strokeWidth=.6))
                amount = low + (high - low) * step / 3
                drawing.add(String(left - 5, y - 2, currency(amount), fontName="Helvetica", fontSize=6.5, fillColor=palette["muted"], textAnchor="end"))
            points = []
            for index, (label, value) in enumerate(values):
                x = left if len(values) == 1 else left + (right - left) * index / (len(values) - 1)
                y = bottom + (top - bottom) * (value - low) / (high - low)
                points.append((x, y))
                drawing.add(Circle(x, y, 3, fillColor=palette["green"], strokeColor=colors.white, strokeWidth=1))
                drawing.add(String(x, 13, plain(label)[:12], fontName="Helvetica", fontSize=7, fillColor=palette["muted"], textAnchor="middle"))
            path = DrawingPath()
            path.moveTo(*points[0])
            for point in points[1:]:
                path.lineTo(*point)
            drawing.add(path, name="cashflow_line")
            drawing.contents[-1].strokeColor = palette["green"]
            drawing.contents[-1].strokeWidth = 2
            drawing.contents[-1].fillColor = None
            return drawing

        story = [
            Spacer(1, 8),
            Paragraph("Your SmartSpend financial summary", styles["title"]),
            Paragraph(
                f"Generated {text(report.generated_at.strftime('%d %B %Y at %H:%M UTC'))}. This report summarizes the patterns found in your temporary analysis session.",
                styles["subtitle"],
            ),
            Paragraph("At a glance", styles["section"]),
            Paragraph("A concise view of income, spending, net cash flow, and savings across the uploaded statement.", styles["section_note"]),
        ]

        metric_cells = []
        for metric in report.metrics[:4]:
            metric_cells.append([
                Paragraph(text(metric.get("label", "Metric")).upper(), styles["metric_label"]),
                Paragraph(text(metric.get("formatted_value", metric.get("value", 0))), styles["metric_value"]),
                Paragraph(text(metric.get("supporting_text", "")), styles["metric_note"]),
            ])
        while len(metric_cells) < 4:
            metric_cells.append([Paragraph("-", styles["metric_value"])])
        metric_table = Table([metric_cells[:2], metric_cells[2:4]], colWidths=[doc.width / 2 - 5, doc.width / 2 - 5], hAlign="LEFT")
        metric_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), palette["paper"]),
            ("BOX", (0, 0), (-1, -1), .7, palette["line"]),
            ("INNERGRID", (0, 0), (-1, -1), .7, palette["line"]),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 14),
            ("RIGHTPADDING", (0, 0), (-1, -1), 14),
            ("TOPPADDING", (0, 0), (-1, -1), 14),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ]))
        story.extend([metric_table, Spacer(1, 22)])

        cashflow_metrics = [(metric.get("label", ""), float(metric.get("value", 0))) for metric in report.metrics if metric.get("id") in {"income", "expenses", "net_cash_flow"}]
        story.extend([
            Paragraph("Cash-flow overview", styles["section"]),
            Paragraph("Income, expenses, and the amount remaining during the statement period.", styles["section_note"]),
            bar_chart(cashflow_metrics),
        ])

        categories = chart_values("category_spending")
        monthly = chart_values("monthly_cashflow")
        if categories or monthly:
            story.extend([PageBreak(), Paragraph("Spending patterns", styles["section"]), Paragraph("Grouped totals help show where money went and how cash flow changed over time.", styles["section_note"])])
        if categories:
            story.extend([Paragraph("Spending by category", styles["item_title"]), Spacer(1, 4), bar_chart(categories, palette["warning"]), Spacer(1, 24)])
        if monthly:
            story.extend([Paragraph("Monthly cash flow", styles["item_title"]), Spacer(1, 4), line_chart(monthly), Spacer(1, 20)])

        if report.insights:
            story.extend([Paragraph("Key insights", styles["section"]), Paragraph("The most useful patterns SmartSpend found in the reviewed statement.", styles["section_note"])])
            for insight in report.insights[:6]:
                story.append(KeepTogether([
                    Paragraph(text(insight.get("title", "Financial insight")), styles["item_title"]),
                    Paragraph(text(insight.get("summary", "")), styles["body"]),
                    Spacer(1, 6),
                ]))

        if report.conclusions:
            story.extend([Spacer(1, 6), Paragraph("What this may mean", styles["section"]), Paragraph("Plain-language conclusions based on the aggregated evidence above.", styles["section_note"])])
            for conclusion in report.conclusions[:5]:
                story.append(KeepTogether([
                    Paragraph(text(conclusion.get("title", "Conclusion")), styles["item_title"]),
                    Paragraph(text(conclusion.get("summary", "")), styles["body"]),
                    Spacer(1, 6),
                ]))

        privacy_panel = Table([[[
            Paragraph("PRIVACY NOTE", styles["metric_label"]),
            Paragraph("This downloadable summary contains aggregated findings only. Raw statement rows, PDF passwords, and unmasked account identifiers are excluded. The temporary SmartSpend session is deleted when it expires.", styles["privacy"]),
        ]]], colWidths=[doc.width])
        privacy_panel.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), palette["green_soft"]),
            ("BOX", (0, 0), (-1, -1), .7, palette["line"]),
            ("LEFTPADDING", (0, 0), (-1, -1), 14),
            ("RIGHTPADDING", (0, 0), (-1, -1), 14),
            ("TOPPADDING", (0, 0), (-1, -1), 13),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 13),
        ]))
        story.extend([Spacer(1, 18), privacy_panel])

        doc.build(story, onFirstPage=page_frame, onLaterPages=page_frame)
        return output_path
