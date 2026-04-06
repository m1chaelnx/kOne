"""
kOne PDF Report Generator

Generates a professional NIS2 compliance assessment report.
This is the paid feature — the thing that turns free users into customers.

The report contains:
  1. Cover page with company name, date, overall score
  2. Executive summary with key findings
  3. Domain-by-domain breakdown with scores
  4. Priority actions — what to fix first
  5. Full gap analysis with remediation guidance
  6. Legal references (NIS2 articles, Czech Cybersecurity Act sections)
"""

import io
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

from app.models.schemas import AssessmentResult


# ══════════════════════════════════════
# NOXRA COLOR SYSTEM
# ══════════════════════════════════════

BLACK = HexColor("#0a0a10")
DARK = HexColor("#14141e")
CHROME = HexColor("#4a7cc9")
CHROME_LIGHT = HexColor("#6b9fe0")
TEXT_PRIMARY = HexColor("#2a2a2a")
TEXT_SECONDARY = HexColor("#5a5a6a")
TEXT_MUTED = HexColor("#8a8a96")
WHITE = HexColor("#ffffff")
SIGNAL_RED = HexColor("#c45050")
SIGNAL_AMBER = HexColor("#b8942a")
SIGNAL_GREEN = HexColor("#4a9e78")
LIGHT_GRAY = HexColor("#f0f0f2")
BORDER_GRAY = HexColor("#e0e0e5")


# ══════════════════════════════════════
# STYLES
# ══════════════════════════════════════

def get_styles():
    return {
        "cover_title": ParagraphStyle(
            "cover_title", fontName="Helvetica-Bold", fontSize=28,
            textColor=WHITE, alignment=TA_LEFT, leading=34,
        ),
        "cover_subtitle": ParagraphStyle(
            "cover_subtitle", fontName="Helvetica", fontSize=12,
            textColor=HexColor("#8a8a96"), alignment=TA_LEFT, leading=18,
        ),
        "cover_score": ParagraphStyle(
            "cover_score", fontName="Helvetica-Bold", fontSize=72,
            textColor=WHITE, alignment=TA_CENTER, leading=80,
        ),
        "section_label": ParagraphStyle(
            "section_label", fontName="Helvetica", fontSize=8,
            textColor=CHROME, alignment=TA_LEFT, leading=12,
            spaceAfter=4, spaceBefore=24,
        ),
        "heading1": ParagraphStyle(
            "heading1", fontName="Helvetica-Bold", fontSize=18,
            textColor=TEXT_PRIMARY, alignment=TA_LEFT, leading=24,
            spaceAfter=8,
        ),
        "heading2": ParagraphStyle(
            "heading2", fontName="Helvetica-Bold", fontSize=13,
            textColor=TEXT_PRIMARY, alignment=TA_LEFT, leading=18,
            spaceAfter=4, spaceBefore=16,
        ),
        "body": ParagraphStyle(
            "body", fontName="Helvetica", fontSize=10,
            textColor=TEXT_PRIMARY, alignment=TA_LEFT, leading=16,
            spaceAfter=6,
        ),
        "body_muted": ParagraphStyle(
            "body_muted", fontName="Helvetica", fontSize=10,
            textColor=TEXT_SECONDARY, alignment=TA_LEFT, leading=16,
            spaceAfter=6,
        ),
        "body_small": ParagraphStyle(
            "body_small", fontName="Helvetica", fontSize=9,
            textColor=TEXT_SECONDARY, alignment=TA_LEFT, leading=14,
            spaceAfter=4,
        ),
        "ref": ParagraphStyle(
            "ref", fontName="Helvetica", fontSize=7,
            textColor=TEXT_MUTED, alignment=TA_LEFT, leading=10,
            spaceAfter=2,
        ),
        "remediation": ParagraphStyle(
            "remediation", fontName="Helvetica", fontSize=9,
            textColor=TEXT_PRIMARY, alignment=TA_LEFT, leading=14,
            spaceAfter=4, leftIndent=12,
        ),
        "footer": ParagraphStyle(
            "footer", fontName="Helvetica", fontSize=7,
            textColor=TEXT_MUTED, alignment=TA_CENTER,
        ),
    }


# ══════════════════════════════════════
# COVER PAGE
# ══════════════════════════════════════

def draw_cover_page(c, result: AssessmentResult, width, height):
    """Draw the cover page directly on the canvas."""

    # Full black background
    c.setFillColor(BLACK)
    c.rect(0, 0, width, height, fill=True, stroke=False)

    # Chrome accent line at top
    c.setStrokeColor(CHROME)
    c.setLineWidth(2)
    c.line(30 * mm, height - 20 * mm, width - 30 * mm, height - 20 * mm)

    # kOne branding
    c.setFillColor(CHROME)
    c.setFont("Helvetica", 10)
    c.drawString(30 * mm, height - 35 * mm, "kOne")
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 8)
    c.drawString(50 * mm, height - 35 * mm, "NIS2 COMPLIANCE REPORT")

    # Company name
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(30 * mm, height - 75 * mm, result.company_name)

    # Date and metadata
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 10)
    date_str = datetime.fromisoformat(result.timestamp).strftime("%d. %m. %Y")
    c.drawString(30 * mm, height - 88 * mm, f"{date_str}  ·  {result.sector}  ·  {result.company_size}")

    # Score circle
    score_pct = round(result.overall_percentage)
    center_x = width / 2
    center_y = height / 2 - 15 * mm
    radius = 40 * mm

    # Circle border
    status_color = (
        SIGNAL_GREEN if result.overall_status == "compliant"
        else SIGNAL_AMBER if result.overall_status == "partial"
        else SIGNAL_RED
    )
    c.setStrokeColor(status_color)
    c.setLineWidth(2)
    c.circle(center_x, center_y, radius, fill=False, stroke=True)

    # Score number
    c.setFillColor(status_color)
    c.setFont("Helvetica-Bold", 64)
    score_text = f"{score_pct}%"
    c.drawCentredString(center_x, center_y - 18, score_text)

    # Score subtitle
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 10)
    c.drawCentredString(center_x, center_y - 38, f"{result.overall_score} / {result.max_score}")

    # Status label
    status_labels = {
        "compliant": "VYHOVUJÍCÍ",
        "partial": "ČÁSTEČNĚ VYHOVUJÍCÍ",
        "non_compliant": "NEVYHOVUJÍCÍ",
    }
    c.setFillColor(status_color)
    c.setFont("Helvetica", 10)
    c.drawCentredString(center_x, center_y - radius - 16 * mm, status_labels.get(result.overall_status, ""))

    # Key stats at bottom
    stats_y = 45 * mm
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 8)

    stat_positions = [
        (width * 0.2, f"{result.critical_gaps}", "KRITICKÝCH MEZER"),
        (width * 0.5, f"{result.total_gaps}", "CELKEM MEZER"),
        (width * 0.8, f"{len([d for d in result.domain_scores if d.status == 'compliant'])}/{len(result.domain_scores)}", "DOMÉN OK"),
    ]

    for x, val, label in stat_positions:
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 22)
        c.drawCentredString(x, stats_y + 12, val)
        c.setFillColor(TEXT_MUTED)
        c.setFont("Helvetica", 7)
        c.drawCentredString(x, stats_y - 4, label)

    # Chrome line at bottom
    c.setStrokeColor(CHROME)
    c.setLineWidth(0.5)
    c.line(30 * mm, 25 * mm, width - 30 * mm, 25 * mm)

    # Footer
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 7)
    c.drawCentredString(width / 2, 18 * mm, "© 2026 Noxra Enterprises  ·  noxra.ai  ·  Zákon č. 264/2025 Sb.")


# ══════════════════════════════════════
# PAGE TEMPLATE
# ══════════════════════════════════════

def add_page_header_footer(c, doc):
    """Called on each page (except cover) to draw header and footer."""
    width, height = A4

    # Header line
    c.setStrokeColor(BORDER_GRAY)
    c.setLineWidth(0.5)
    c.line(20 * mm, height - 18 * mm, width - 20 * mm, height - 18 * mm)

    # Header text
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 7)
    c.drawString(20 * mm, height - 15 * mm, "kOne NIS2 Compliance Report")
    c.drawRightString(width - 20 * mm, height - 15 * mm, "Noxra Enterprises")

    # Footer
    c.setStrokeColor(BORDER_GRAY)
    c.setLineWidth(0.5)
    c.line(20 * mm, 18 * mm, width - 20 * mm, 18 * mm)

    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 7)
    c.drawCentredString(width / 2, 12 * mm, f"Strana {doc.page}")


# ══════════════════════════════════════
# HELPER: STATUS COLOR FOR TEXT
# ══════════════════════════════════════

def status_color_hex(status):
    if status == "compliant":
        return "#4a9e78"
    elif status == "partial":
        return "#b8942a"
    return "#c45050"


def pct_color_hex(pct):
    if pct >= 80:
        return "#4a9e78"
    elif pct >= 50:
        return "#b8942a"
    return "#c45050"


# ══════════════════════════════════════
# MAIN GENERATOR
# ══════════════════════════════════════

def generate_report(result: AssessmentResult) -> bytes:
    """
    Generate a complete PDF report from an assessment result.
    Returns the PDF as bytes (ready to send as HTTP response).
    """
    buffer = io.BytesIO()
    styles = get_styles()
    width, height = A4

    # Create the document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=25 * mm,
        bottomMargin=25 * mm,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
    )

    story = []

    # ── EXECUTIVE SUMMARY ──

    story.append(Paragraph("EXECUTIVE SUMMARY", styles["section_label"]))
    story.append(Paragraph("Shrnutí hodnocení", styles["heading1"]))

    date_str = datetime.fromisoformat(result.timestamp).strftime("%d. %m. %Y")
    color = status_color_hex(result.overall_status)
    status_cs = {"compliant": "vyhovující", "partial": "částečně vyhovující", "non_compliant": "nevyhovující"}

    summary_text = (
        f"Organizace <b>{result.company_name}</b> dosáhla celkového skóre "
        f"<font color='{color}'><b>{round(result.overall_percentage)}%</b></font> "
        f"({result.overall_score}/{result.max_score} bodů), "
        f"což odpovídá statusu <font color='{color}'><b>{status_cs.get(result.overall_status, '')}</b></font>. "
        f"Hodnocení bylo provedeno dne {date_str}."
    )
    story.append(Paragraph(summary_text, styles["body"]))

    story.append(Paragraph(
        f"Bylo identifikováno <b>{result.total_gaps} mezer</b> v souladu, "
        f"z toho <font color='#c45050'><b>{result.critical_gaps} kritických</b></font> "
        f"(váha 4-5 z 5). "
        f"Z {len(result.domain_scores)} hodnocených domén je "
        f"<font color='#4a9e78'><b>{len([d for d in result.domain_scores if d.status == 'compliant'])}</b></font> "
        f"v plném souladu.",
        styles["body"]
    ))

    story.append(Spacer(1, 8 * mm))

    # ── DOMAIN OVERVIEW TABLE ──

    story.append(Paragraph("DOMAIN BREAKDOWN", styles["section_label"]))
    story.append(Paragraph("Přehled domén", styles["heading1"]))

    table_data = [["Doména", "Skóre", "%", "Status"]]
    for ds in result.domain_scores:
        pct = round(ds.percentage)
        color = pct_color_hex(ds.percentage)
        status_label = {"compliant": "OK", "partial": "Částečně", "non_compliant": "Nesplněno"}
        table_data.append([
            Paragraph(ds.domain_name_cs, styles["body_small"]),
            Paragraph(f"{ds.score}/{ds.max_score}", styles["body_small"]),
            Paragraph(f"<font color='{color}'><b>{pct}%</b></font>", styles["body_small"]),
            Paragraph(f"<font color='{color}'>{status_label.get(ds.status, '')}</font>", styles["body_small"]),
        ])

    col_widths = [90 * mm, 25 * mm, 20 * mm, 30 * mm]
    table = Table(table_data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), LIGHT_GRAY),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("TEXTCOLOR", (0, 0), (-1, 0), TEXT_SECONDARY),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
        ("TOPPADDING", (0, 1), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, BORDER_GRAY),
        ("LINEBELOW", (0, 1), (-1, -2), 0.25, BORDER_GRAY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(table)
    story.append(Spacer(1, 8 * mm))

    # ── PRIORITY ACTIONS ──

    if result.priority_actions:
        story.append(Paragraph("PRIORITY ACTIONS", styles["section_label"]))
        story.append(Paragraph("Prioritní akce", styles["heading1"]))
        story.append(Paragraph(
            "Následující kroky mají nejvyšší prioritu pro dosažení souladu. "
            "Jsou seřazeny podle závažnosti.",
            styles["body_muted"]
        ))
        story.append(Spacer(1, 4 * mm))

        for i, gap in enumerate(result.priority_actions, 1):
            w = gap["weight"]
            wcolor = "#c45050" if w >= 5 else "#b8942a" if w >= 4 else "#5a5a6a"

            story.append(Paragraph(
                f"<font color='{wcolor}'><b>[{w}/5]</b></font>  "
                f"<b>{gap['question_cs']}</b>",
                styles["body"]
            ))
            story.append(Paragraph(gap["question_en"], styles["body_small"]))
            story.append(Paragraph(
                f"<font color='#4a7cc9'>→</font> {gap['remediation']}",
                styles["remediation"]
            ))
            story.append(Paragraph(
                f"{gap['article_ref']}  ·  {gap['domain_name_cs']}",
                styles["ref"]
            ))
            story.append(Spacer(1, 3 * mm))

    story.append(PageBreak())

    # ── FULL GAP ANALYSIS BY DOMAIN ──

    story.append(Paragraph("FULL GAP ANALYSIS", styles["section_label"]))
    story.append(Paragraph("Kompletní analýza mezer", styles["heading1"]))
    story.append(Paragraph(
        "Podrobný přehled všech zjištěných nedostatků podle jednotlivých domén "
        "s konkrétními kroky k nápravě.",
        styles["body_muted"]
    ))
    story.append(Spacer(1, 4 * mm))

    for ds in result.domain_scores:
        if not ds.gaps:
            continue

        color = pct_color_hex(ds.percentage)
        story.append(Paragraph(
            f"<font color='{color}'><b>{round(ds.percentage)}%</b></font>  "
            f"<b>{ds.domain_name_cs}</b>  "
            f"<font color='#8a8a96'>({ds.domain_name_en})</font>",
            styles["heading2"]
        ))

        for gap in ds.gaps:
            w = gap["weight"]
            wcolor = "#c45050" if w >= 5 else "#b8942a" if w >= 4 else "#5a5a6a"

            story.append(Paragraph(
                f"<font color='{wcolor}'>[{w}/5]</font>  {gap['question_cs']}",
                styles["body"]
            ))
            story.append(Paragraph(gap["question_en"], styles["body_small"]))
            story.append(Paragraph(
                f"<font color='#4a7cc9'>→</font> {gap['remediation']}",
                styles["remediation"]
            ))
            story.append(Paragraph(gap["article_ref"], styles["ref"]))
            story.append(Spacer(1, 2 * mm))

        story.append(Spacer(1, 4 * mm))

    # ── COMPLIANT DOMAINS ──

    compliant = [ds for ds in result.domain_scores if not ds.gaps]
    if compliant:
        story.append(Paragraph("COMPLIANT DOMAINS", styles["section_label"]))
        story.append(Paragraph("Domény v plném souladu", styles["heading2"]))
        for ds in compliant:
            story.append(Paragraph(
                f"<font color='#4a9e78'>●</font>  {ds.domain_name_cs} — {round(ds.percentage)}%",
                styles["body"]
            ))
        story.append(Spacer(1, 8 * mm))

    # ── LEGAL REFERENCES ──

    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_GRAY, spaceAfter=8))
    story.append(Paragraph("PRÁVNÍ ODKAZY", styles["section_label"]))
    story.append(Paragraph(
        "Toto hodnocení vychází z požadavků zákona č. 264/2025 Sb. o kybernetické bezpečnosti "
        "(implementace směrnice EU NIS2 2022/2555) a pokynů Národního úřadu pro kybernetickou "
        "a informační bezpečnost (NÚKIB).",
        styles["body_small"]
    ))
    story.append(Paragraph(
        "Tento report slouží jako interní nástroj pro hodnocení připravenosti organizace. "
        "Nepředstavuje právní posouzení ani certifikaci souladu.",
        styles["body_small"]
    ))
    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph(
        "Vygenerováno systémem kOne  ·  noxra.ai  ·  © 2026 Noxra Enterprises",
        styles["ref"]
    ))

    # ── BUILD ──

    def on_first_page(canvas_obj, doc):
        draw_cover_page(canvas_obj, result, width, height)

    def on_later_pages(canvas_obj, doc):
        add_page_header_footer(canvas_obj, doc)

    doc.build(story, onFirstPage=on_first_page, onLaterPages=on_later_pages)
    buffer.seek(0)
    return buffer.getvalue()
