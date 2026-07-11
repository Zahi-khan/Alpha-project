"""Generate a minimal temporary PDF without exposing raw statement details."""

from __future__ import annotations

from pathlib import Path

from application.errors.processing_error import ProcessingError


class PDFGenerator:
    def generate(self, report, output_path: Path) -> Path:
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
        except ImportError as error:
            raise ProcessingError("PDF report generation is unavailable in this runtime.") from error

        output_path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        styles = getSampleStyleSheet()
        story = [Paragraph("SmartSpend Financial Overview", styles["Title"]), Spacer(1, 16)]
        story.append(Paragraph(f"Generated: {report.generated_at.isoformat(timespec='seconds')} UTC", styles["Normal"]))
        story.append(Spacer(1, 12))
        story.append(Paragraph("Summary", styles["Heading2"]))
        for key, value in report.summary.items():
            story.append(Paragraph(f"{key.replace('_', ' ').title()}: {value}", styles["Normal"]))
        if report.insights:
            story.extend([Spacer(1, 12), Paragraph("Financial Insights", styles["Heading2"])])
            for insight in report.insights:
                story.append(Paragraph(f"<b>{insight['title']}</b> - {insight['summary']}", styles["Normal"]))
        if report.conclusions:
            story.extend([Spacer(1, 12), Paragraph("Conclusions", styles["Heading2"])])
            for conclusion in report.conclusions:
                story.append(Paragraph(f"<b>{conclusion['title']}</b> - {conclusion['summary']}", styles["Normal"]))
        story.extend([Spacer(1, 16), Paragraph("Privacy: This report contains aggregated temporary analysis. Raw statement rows and unmasked account identifiers are excluded.", styles["Italic"])])
        SimpleDocTemplate(str(output_path), pagesize=A4, title="SmartSpend Financial Overview").build(story)
        return output_path
