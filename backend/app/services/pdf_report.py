"""
kOne PDF Report Generator — v2
Fixed: Czech diacritics support using DejaVu Sans font.
"""

import io
import os
from datetime import datetime
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from app.models.schemas import AssessmentResult


# ══════════════════════════════════════
# FONT REGISTRATION — DejaVu Sans supports Czech diacritics
# ══════════════════════════════════════

def register_fonts():
    """Register DejaVu Sans fonts that support Czech characters."""
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/",
        "/usr/share/fonts/dejavu/",
        "/usr/share/fonts/TTF/",
        "C:/Windows/Fonts/",
        "/System/Library/Fonts/Supplemental/",
    ]

    dejavu_regular = None
    dejavu_bold = None

    for base in font_paths:
        r = os.path.join(base, "DejaVuSans.ttf")
        b = os.path.join(base, "DejaVuSans-Bold.ttf")
        if os.path.exists(r):
            dejavu_regular = r
            dejavu_bold = b if os.path.exists(b) else r
            break

    if dejavu_regular:
        pdfmetrics.registerFont(TTFont("DejaVu", dejavu_regular))
        pdfmetrics.registerFont(TTFont("DejaVu-Bold", dejavu_bold))
        return "DejaVu", "DejaVu-Bold"

    return "Helvetica", "Helvetica-Bold"


FONT, FONT_BOLD = register_fonts()


# ══════════════════════════════════════
# COLORS
# ══════════════════════════════════════

BLACK = HexColor("#0a0a10")
CHROME = HexColor("#4a7cc9")
TEXT_PRIMARY = HexColor("#2a2a2a")
TEXT_SECONDARY = HexColor("#5a5a6a")
TEXT_MUTED = HexColor("#8a8a96")
WHITE = HexColor("#ffffff")
SIGNAL_RED = HexColor("#c45050")
SIGNAL_AMBER = HexColor("#b8942a")
SIGNAL_GREEN = HexColor("#4a9e78")
LIGHT_GRAY = HexColor("#f4f4f6")
BORDER_GRAY = HexColor("#e0e0e5")


# ══════════════════════════════════════
# STYLES
# ══════════════════════════════════════

def get_styles():
    return {
        "section_label": ParagraphStyle(
            "section_label", fontName=FONT, fontSize=8,
            textColor=CHROME, alignment=TA_LEFT, leading=12,
            spaceAfter=4, spaceBefore=20,
        ),
        "h1": ParagraphStyle(
            "h1", fontName=FONT_BOLD, fontSize=16,
            textColor=TEXT_PRIMARY, alignment=TA_LEFT, leading=22,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "h2", fontName=FONT_BOLD, fontSize=12,
            textColor=TEXT_PRIMARY, alignment=TA_LEFT, leading=17,
            spaceAfter=4, spaceBefore=14,
        ),
        "body": ParagraphStyle(
            "body", fontName=FONT, fontSize=9.5,
            textColor=TEXT_PRIMARY, alignment=TA_LEFT, leading=15,
            spaceAfter=5,
        ),
        "body_muted": ParagraphStyle(
            "body_muted", fontName=FONT, fontSize=9.5,
            textColor=TEXT_SECONDARY, alignment=TA_LEFT, leading=15,
            spaceAfter=5,
        ),
        "small": ParagraphStyle(
            "small", fontName=FONT, fontSize=8.5,
            textColor=TEXT_SECONDARY, alignment=TA_LEFT, leading=13,
            spaceAfter=3,
        ),
        "ref": ParagraphStyle(
            "ref", fontName=FONT, fontSize=7,
            textColor=TEXT_MUTED, alignment=TA_LEFT, leading=10,
            spaceAfter=2,
        ),
        "remediation": ParagraphStyle(
            "remediation", fontName=FONT, fontSize=9,
            textColor=TEXT_PRIMARY, alignment=TA_LEFT, leading=14,
            spaceAfter=3, leftIndent=14,
        ),
    }


# ══════════════════════════════════════
# HELPERS
# ══════════════════════════════════════

def status_color(status):
    if status == "compliant": return "#4a9e78"
    if status == "partial": return "#b8942a"
    return "#c45050"

def pct_color(pct):
    if pct >= 80: return "#4a9e78"
    if pct >= 50: return "#b8942a"
    return "#c45050"

def status_label_cs(status):
    return {"compliant": "Vyhovující", "partial": "Částečně vyhovující", "non_compliant": "Nevyhovující"}.get(status, "")

def status_label_table(status):
    return {"compliant": "OK", "partial": "Částečně", "non_compliant": "Nesplněno"}.get(status, "")


# ══════════════════════════════════════
# COVER PAGE
# ══════════════════════════════════════

def draw_cover(c, result, width, height):
    c.setFillColor(BLACK)
    c.rect(0, 0, width, height, fill=True, stroke=False)

    # Chrome line top
    c.setStrokeColor(CHROME)
    c.setLineWidth(1.5)
    c.line(30*mm, height - 22*mm, width - 30*mm, height - 22*mm)

    # Branding
    c.setFillColor(CHROME)
    c.setFont(FONT, 9)
    c.drawString(30*mm, height - 34*mm, "kOne")
    c.setFillColor(TEXT_MUTED)
    c.setFont(FONT, 7)
    c.drawString(48*mm, height - 34*mm, "NIS2 COMPLIANCE REPORT")

    # Company name
    c.setFillColor(WHITE)
    c.setFont(FONT_BOLD, 26)
    c.drawString(30*mm, height - 70*mm, result.company_name)

    # Metadata
    c.setFillColor(TEXT_MUTED)
    c.setFont(FONT, 9)
    date_str = datetime.fromisoformat(result.timestamp).strftime("%d. %m. %Y")
    c.drawString(30*mm, height - 82*mm, f"{date_str}  ·  {result.sector}  ·  {result.company_size}")

    # Score
    pct = round(result.overall_percentage)
    cx, cy = width / 2, height / 2 - 12*mm
    r = 38*mm
    sc = HexColor(status_color(result.overall_status))

    c.setStrokeColor(sc)
    c.setLineWidth(1.5)
    c.circle(cx, cy, r, fill=False, stroke=True)

    c.setFillColor(sc)
    c.setFont(FONT_BOLD, 58)
    c.drawCentredString(cx, cy - 16, f"{pct}%")

    c.setFillColor(TEXT_MUTED)
    c.setFont(FONT, 9)
    c.drawCentredString(cx, cy - 34, f"{result.overall_score} / {result.max_score}")

    c.setFillColor(sc)
    c.setFont(FONT, 9)
    c.drawCentredString(cx, cy - r - 14*mm, status_label_cs(result.overall_status).upper())

    # Stats
    sy = 42*mm
    stats = [
        (width * 0.2, str(result.critical_gaps), "KRITICKÝCH MEZER"),
        (width * 0.5, str(result.total_gaps), "CELKEM MEZER"),
        (width * 0.8, f"{len([d for d in result.domain_scores if d.status == 'compliant'])}/{len(result.domain_scores)}", "DOMÉN OK"),
    ]
    for x, val, lbl in stats:
        c.setFillColor(WHITE)
        c.setFont(FONT_BOLD, 20)
        c.drawCentredString(x, sy + 10, val)
        c.setFillColor(TEXT_MUTED)
        c.setFont(FONT, 6.5)
        c.drawCentredString(x, sy - 4, lbl)

    # Bottom line
    c.setStrokeColor(CHROME)
    c.setLineWidth(0.5)
    c.line(30*mm, 24*mm, width - 30*mm, 24*mm)

    c.setFillColor(TEXT_MUTED)
    c.setFont(FONT, 6.5)
    c.drawCentredString(width / 2, 17*mm, "© 2026 Noxra Enterprises  ·  noxra.ai  ·  Zákon č. 264/2025 Sb.")


# ══════════════════════════════════════
# PAGE HEADER/FOOTER
# ══════════════════════════════════════

def draw_page_chrome(c, doc):
    w, h = A4
    c.setStrokeColor(BORDER_GRAY)
    c.setLineWidth(0.4)
    c.line(20*mm, h - 17*mm, w - 20*mm, h - 17*mm)
    c.line(20*mm, 17*mm, w - 20*mm, 17*mm)

    c.setFillColor(TEXT_MUTED)
    c.setFont(FONT, 6.5)
    c.drawString(20*mm, h - 14*mm, "kOne NIS2 Compliance Report")
    c.drawRightString(w - 20*mm, h - 14*mm, "Noxra Enterprises")
    c.drawCentredString(w / 2, 11*mm, f"Strana {doc.page}")


# ══════════════════════════════════════
# GENERATE
# ══════════════════════════════════════

def generate_report(result: AssessmentResult) -> bytes:
    buf = io.BytesIO()
    s = get_styles()
    w, h = A4

    doc = SimpleDocTemplate(buf, pagesize=A4,
        topMargin=24*mm, bottomMargin=24*mm,
        leftMargin=20*mm, rightMargin=20*mm)

    story = []

    # ── EXECUTIVE SUMMARY ──

    story.append(Paragraph("EXECUTIVE SUMMARY", s["section_label"]))
    story.append(Paragraph("Shrnutí hodnocení", s["h1"]))

    date_str = datetime.fromisoformat(result.timestamp).strftime("%d. %m. %Y")
    sc = status_color(result.overall_status)
    sl = status_label_cs(result.overall_status)

    story.append(Paragraph(
        f'Organizace <b>{result.company_name}</b> dosáhla celkového skóre '
        f'<font color="{sc}"><b>{round(result.overall_percentage)}%</b></font> '
        f'({result.overall_score}/{result.max_score} bodů), '
        f'což odpovídá statusu <font color="{sc}"><b>{sl}</b></font>. '
        f'Hodnocení provedeno dne {date_str}.',
        s["body"]
    ))

    compliant_count = len([d for d in result.domain_scores if d.status == "compliant"])
    story.append(Paragraph(
        f'Identifikováno <b>{result.total_gaps} mezer</b>, '
        f'z toho <font color="#c45050"><b>{result.critical_gaps} kritických</b></font> '
        f'(váha 4–5). '
        f'Z {len(result.domain_scores)} domén je '
        f'<font color="#4a9e78"><b>{compliant_count}</b></font> v plném souladu.',
        s["body"]
    ))

    story.append(Spacer(1, 6*mm))

    # ── DOMAIN TABLE ──

    story.append(Paragraph("DOMAIN BREAKDOWN", s["section_label"]))
    story.append(Paragraph("Přehled domén", s["h1"]))

    data = [["Doména", "Skóre", "%", "Status"]]
    for ds in result.domain_scores:
        pc = pct_color(ds.percentage)
        data.append([
            Paragraph(ds.domain_name_cs, s["small"]),
            Paragraph(f"{ds.score}/{ds.max_score}", s["small"]),
            Paragraph(f'<font color="{pc}"><b>{round(ds.percentage)}%</b></font>', s["small"]),
            Paragraph(f'<font color="{pc}">{status_label_table(ds.status)}</font>', s["small"]),
        ])

    t = Table(data, colWidths=[88*mm, 24*mm, 20*mm, 30*mm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), LIGHT_GRAY),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD),
        ("FONTSIZE", (0, 0), (-1, 0), 7.5),
        ("TEXTCOLOR", (0, 0), (-1, 0), TEXT_SECONDARY),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, BORDER_GRAY),
        ("LINEBELOW", (0, 1), (-1, -2), 0.25, BORDER_GRAY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(t)
    story.append(Spacer(1, 6*mm))

    # ── PRIORITY ACTIONS ──

    if result.priority_actions:
        story.append(Paragraph("PRIORITY ACTIONS", s["section_label"]))
        story.append(Paragraph("Prioritní akce", s["h1"]))
        story.append(Paragraph(
            "Následující kroky mají nejvyšší prioritu. Seřazeno podle závažnosti.",
            s["body_muted"]
        ))
        story.append(Spacer(1, 3*mm))

        for gap in result.priority_actions:
            wt = gap["weight"]
            wc = "#c45050" if wt >= 5 else "#b8942a" if wt >= 4 else "#5a5a6a"

            story.append(Paragraph(
                f'<font color="{wc}"><b>[{wt}/5]</b></font>  '
                f'<b>{gap["question_cs"]}</b>',
                s["body"]
            ))
            story.append(Paragraph(gap["question_en"], s["small"]))
            story.append(Paragraph(
                f'<font color="#4a7cc9">→</font> {gap["remediation"]}',
                s["remediation"]
            ))
            story.append(Paragraph(
                f'{gap["article_ref"]}  ·  {gap["domain_name_cs"]}',
                s["ref"]
            ))
            story.append(Spacer(1, 2.5*mm))

    story.append(PageBreak())

    # ── FULL GAP ANALYSIS ──

    story.append(Paragraph("FULL GAP ANALYSIS", s["section_label"]))
    story.append(Paragraph("Kompletní analýza mezer", s["h1"]))
    story.append(Paragraph(
        "Podrobný přehled zjištěných nedostatků podle domén s kroky k nápravě.",
        s["body_muted"]
    ))
    story.append(Spacer(1, 3*mm))

    for ds in result.domain_scores:
        if not ds.gaps:
            continue

        pc = pct_color(ds.percentage)
        story.append(Paragraph(
            f'<font color="{pc}"><b>{round(ds.percentage)}%</b></font>  '
            f'<b>{ds.domain_name_cs}</b>  '
            f'<font color="#8a8a96">({ds.domain_name_en})</font>',
            s["h2"]
        ))

        for gap in ds.gaps:
            wt = gap["weight"]
            wc = "#c45050" if wt >= 5 else "#b8942a" if wt >= 4 else "#5a5a6a"

            story.append(Paragraph(
                f'<font color="{wc}">[{wt}/5]</font>  {gap["question_cs"]}',
                s["body"]
            ))
            story.append(Paragraph(gap["question_en"], s["small"]))
            story.append(Paragraph(
                f'<font color="#4a7cc9">→</font> {gap["remediation"]}',
                s["remediation"]
            ))
            story.append(Paragraph(gap["article_ref"], s["ref"]))
            story.append(Spacer(1, 2*mm))

        story.append(Spacer(1, 3*mm))

    # ── COMPLIANT DOMAINS ──

    ok = [d for d in result.domain_scores if not d.gaps]
    if ok:
        story.append(Paragraph("COMPLIANT DOMAINS", s["section_label"]))
        story.append(Paragraph("Domény v plném souladu", s["h2"]))
        for d in ok:
            story.append(Paragraph(
                f'<font color="#4a9e78">●</font>  {d.domain_name_cs} — {round(d.percentage)}%',
                s["body"]
            ))
        story.append(Spacer(1, 6*mm))

    # ── LEGAL ──

    story.append(HRFlowable(width="100%", thickness=0.4, color=BORDER_GRAY, spaceAfter=6))
    story.append(Paragraph("PRÁVNÍ ODKAZY", s["section_label"]))
    story.append(Paragraph(
        "Hodnocení vychází z požadavků zákona č. 264/2025 Sb. o kybernetické bezpečnosti "
        "(implementace směrnice EU NIS2 2022/2555) a pokynů NÚKIB. "
        "Report slouží jako interní nástroj a nepředstavuje právní posouzení.",
        s["small"]
    ))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(
        "Vygenerováno systémem kOne  ·  noxra.ai  ·  © 2026 Noxra Enterprises",
        s["ref"]
    ))

    # ── BUILD ──

    def first_page(canvas_obj, doc):
        draw_cover(canvas_obj, result, w, h)

    def later_pages(canvas_obj, doc):
        draw_page_chrome(canvas_obj, doc)

    doc.build(story, onFirstPage=first_page, onLaterPages=later_pages)
    buf.seek(0)
    return buf.getvalue()
