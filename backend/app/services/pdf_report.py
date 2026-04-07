"""
kOne PDF Report Generator — v3
Boardroom-quality compliance report.

Structure:
  Page 1: Cover — company name, score, status, key metrics
  Page 2: Executive summary + domain breakdown table
  Page 3: Risk heatmap overview + compliance timeline recommendation
  Page 4+: Priority actions with full remediation
  Final:  Full gap analysis by domain + legal references
"""

import io
import os
from datetime import datetime, timedelta

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as canvas_module

from app.models.schemas import AssessmentResult


# ══════════════════════════════════════
# FONTS
# ══════════════════════════════════════

def _register_fonts():
    for base in ["/usr/share/fonts/truetype/dejavu/", "/usr/share/fonts/dejavu/",
                 "/usr/share/fonts/TTF/", "C:/Windows/Fonts/",
                 "/System/Library/Fonts/Supplemental/"]:
        r = os.path.join(base, "DejaVuSans.ttf")
        b = os.path.join(base, "DejaVuSans-Bold.ttf")
        if os.path.exists(r):
            pdfmetrics.registerFont(TTFont("NX", r))
            pdfmetrics.registerFont(TTFont("NXB", b if os.path.exists(b) else r))
            return "NX", "NXB"
    return "Helvetica", "Helvetica-Bold"

F, FB = _register_fonts()

W, H = A4
LM = 28 * mm  # left margin
RM = W - 28 * mm  # right margin
CONTENT_W = RM - LM


# ══════════════════════════════════════
# COLORS
# ══════════════════════════════════════

VOID = HexColor("#07070c")
SURFACE = HexColor("#0d0d14")
CHROME = HexColor("#4a7cc9")
CHROME_DIM = HexColor("#2d5a9e")
WHITE = HexColor("#e8e6e1")
GRAY = HexColor("#8a8a96")
DARK_GRAY = HexColor("#4a4a56")
RED = HexColor("#c45050")
AMBER = HexColor("#b8942a")
GREEN = HexColor("#4a9e78")
PAPER = HexColor("#fafafa")
TEXT = HexColor("#1a1a24")
TEXT2 = HexColor("#5a5a68")
TEXT3 = HexColor("#8a8a96")
BORDER = HexColor("#e0e0e8")
LIGHT_BG = HexColor("#f4f4f8")


def _sc(status):
    return GREEN if status == "compliant" else AMBER if status == "partial" else RED

def _pc(pct):
    return GREEN if pct >= 80 else AMBER if pct >= 50 else RED

def _sl(status):
    return {"compliant": "Vyhovující", "partial": "Částečně vyhovující", "non_compliant": "Nevyhovující"}.get(status, "")


# ══════════════════════════════════════
# TEXT HELPERS
# ══════════════════════════════════════

def _draw_text(c, x, y, text, font=None, size=9, color=TEXT, align="left", max_width=None):
    """Draw text with optional wrapping. Returns new y position."""
    c.setFont(font or F, size)
    c.setFillColor(color)

    if max_width and c.stringWidth(text, font or F, size) > max_width:
        words = text.split()
        lines = []
        current = ""
        for word in words:
            test = f"{current} {word}".strip()
            if c.stringWidth(test, font or F, size) <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)

        line_h = size * 1.5
        for line in lines:
            if y < 30 * mm:
                return y
            if align == "center":
                c.drawCentredString(x, y, line)
            elif align == "right":
                c.drawRightString(x, y, line)
            else:
                c.drawString(x, y, line)
            y -= line_h
        return y
    else:
        if align == "center":
            c.drawCentredString(x, y, text)
        elif align == "right":
            c.drawRightString(x, y, text)
        else:
            c.drawString(x, y, text)
        return y - size * 1.5


def _draw_chrome_line(c, y, width_pct=1.0):
    """Draw the signature chrome blue gradient line."""
    cx = W / 2
    half = (CONTENT_W * width_pct) / 2
    c.setStrokeColor(CHROME)
    c.setLineWidth(0.8)
    c.line(cx - half, y, cx + half, y)


def _page_header(c, page_num, total=None):
    """Standard page header for content pages."""
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.3)
    c.line(LM, H - 16 * mm, RM, H - 16 * mm)

    c.setFont(F, 6.5)
    c.setFillColor(TEXT3)
    c.drawString(LM, H - 13 * mm, "kOne — NIS2 Compliance Report")
    c.drawRightString(RM, H - 13 * mm, "Noxra Enterprises  ·  noxra.ai")

    # Footer
    c.setStrokeColor(BORDER)
    c.line(LM, 16 * mm, RM, 16 * mm)
    c.setFont(F, 6.5)
    c.setFillColor(TEXT3)
    c.drawCentredString(W / 2, 10 * mm, f"Strana {page_num}")
    c.drawString(LM, 10 * mm, "Důvěrné")
    c.drawRightString(RM, 10 * mm, "© 2026 Noxra Enterprises")


# ══════════════════════════════════════
# PAGE 1: COVER
# ══════════════════════════════════════

def _page_cover(c, r):
    c.setFillColor(VOID)
    c.rect(0, 0, W, H, fill=True, stroke=False)

    # Top chrome line
    _draw_chrome_line(c, H - 20 * mm)

    # Branding
    c.setFont(FB, 10)
    c.setFillColor(CHROME)
    c.drawString(LM, H - 32 * mm, "kOne")
    c.setFont(F, 7)
    c.setFillColor(DARK_GRAY)
    c.drawString(LM + 30 * mm, H - 32 * mm, "NIS2 COMPLIANCE REPORT")

    # Report date
    date_str = datetime.fromisoformat(r.timestamp).strftime("%d. %m. %Y")
    c.setFont(F, 8)
    c.setFillColor(GRAY)
    c.drawRightString(RM, H - 32 * mm, date_str)

    # Company name — large
    c.setFont(FB, 30)
    c.setFillColor(WHITE)
    c.drawString(LM, H - 62 * mm, r.company_name)

    # Metadata line
    c.setFont(F, 9)
    c.setFillColor(GRAY)
    size_labels = {"micro": "1–9 zaměstnanců", "small": "10–49", "medium": "50–249", "large": "250+"}
    c.drawString(LM, H - 74 * mm, f"{r.sector}  ·  {size_labels.get(r.company_size, r.company_size)}")

    # Thin divider
    c.setStrokeColor(HexColor("#ffffff08"))
    c.setLineWidth(0.3)
    c.line(LM, H - 82 * mm, RM, H - 82 * mm)

    # Score — centered, large
    pct = round(r.overall_percentage)
    cx = W / 2
    cy = H / 2 - 8 * mm
    radius = 42 * mm
    color = _sc(r.overall_status)

    # Outer ring
    c.setStrokeColor(color)
    c.setLineWidth(2)
    c.circle(cx, cy, radius, fill=False, stroke=True)

    # Inner subtle ring
    c.setStrokeColor(color)
    c.setLineWidth(0.3)
    c.circle(cx, cy, radius - 6 * mm, fill=False, stroke=True)

    # Score text
    c.setFont(FB, 64)
    c.setFillColor(color)
    c.drawCentredString(cx, cy - 18, f"{pct}%")

    c.setFont(F, 10)
    c.setFillColor(GRAY)
    c.drawCentredString(cx, cy - 36, f"{r.overall_score} / {r.max_score} bodů")

    # Status label
    c.setFont(F, 10)
    c.setFillColor(color)
    label = _sl(r.overall_status).upper()
    c.drawCentredString(cx, cy - radius - 16 * mm, label)

    # Three stat boxes at bottom
    box_y = 50 * mm
    box_h = 36 * mm
    box_w = CONTENT_W / 3 - 3 * mm
    positions = [
        (LM, str(r.critical_gaps), "Kritických mezer"),
        (LM + CONTENT_W / 3 + 1.5 * mm, str(r.total_gaps), "Celkem mezer"),
        (LM + 2 * CONTENT_W / 3 + 3 * mm, f"{len([d for d in r.domain_scores if d.status == 'compliant'])}/{len(r.domain_scores)}", "Domén v souladu"),
    ]

    for bx, val, lbl in positions:
        c.setFillColor(SURFACE)
        c.roundRect(bx, box_y, box_w, box_h, 3, fill=True, stroke=False)
        c.setFillColor(WHITE)
        c.setFont(FB, 24)
        c.drawCentredString(bx + box_w / 2, box_y + box_h / 2 + 2, val)
        c.setFillColor(GRAY)
        c.setFont(F, 7)
        c.drawCentredString(bx + box_w / 2, box_y + 8, lbl)

    # Bottom chrome line
    _draw_chrome_line(c, 38 * mm)

    # Footer
    c.setFont(F, 6.5)
    c.setFillColor(DARK_GRAY)
    c.drawCentredString(W / 2, 28 * mm, "© 2026 Noxra Enterprises  ·  noxra.ai  ·  Zákon č. 264/2025 Sb.  ·  Důvěrné")


# ══════════════════════════════════════
# PAGE 2: EXECUTIVE SUMMARY + DOMAIN TABLE
# ══════════════════════════════════════

def _page_summary(c, r):
    c.setFillColor(HexColor("#ffffff"))
    c.rect(0, 0, W, H, fill=True, stroke=False)
    _page_header(c, 2)

    y = H - 28 * mm

    # Section label
    c.setFont(F, 7)
    c.setFillColor(CHROME)
    c.drawString(LM, y, "EXECUTIVE SUMMARY")
    y -= 6 * mm

    c.setFont(FB, 16)
    c.setFillColor(TEXT)
    c.drawString(LM, y, "Shrnutí hodnocení")
    y -= 10 * mm

    date_str = datetime.fromisoformat(r.timestamp).strftime("%d. %m. %Y")
    color = _sc(r.overall_status)
    sl = _sl(r.overall_status)
    compliant_count = len([d for d in r.domain_scores if d.status == "compliant"])

    text1 = (f"Organizace {r.company_name} dosáhla celkového skóre souladu "
             f"{round(r.overall_percentage)}% ({r.overall_score}/{r.max_score} bodů), "
             f"což odpovídá statusu '{sl}'. Hodnocení provedeno dne {date_str}.")
    y = _draw_text(c, LM, y, text1, size=9.5, color=TEXT, max_width=CONTENT_W)

    y -= 4 * mm

    text2 = (f"Celkem bylo identifikováno {r.total_gaps} mezer v souladu s požadavky "
             f"zákona o kybernetické bezpečnosti, z toho {r.critical_gaps} kritických "
             f"(váha 4–5 z 5). Z {len(r.domain_scores)} hodnocených domén je "
             f"{compliant_count} v plném souladu.")
    y = _draw_text(c, LM, y, text2, size=9.5, color=TEXT, max_width=CONTENT_W)
    y -= 12 * mm

    # Domain breakdown table
    c.setFont(F, 7)
    c.setFillColor(CHROME)
    c.drawString(LM, y, "DOMAIN BREAKDOWN")
    y -= 6 * mm

    c.setFont(FB, 14)
    c.setFillColor(TEXT)
    c.drawString(LM, y, "Přehled domén")
    y -= 10 * mm

    # Table header
    col_x = [LM, LM + 100 * mm, LM + 125 * mm, LM + 142 * mm]
    c.setFillColor(LIGHT_BG)
    c.rect(LM - 2 * mm, y - 2, CONTENT_W + 4 * mm, 14, fill=True, stroke=False)
    c.setFont(FB, 7)
    c.setFillColor(TEXT3)
    c.drawString(col_x[0], y + 2, "Doména")
    c.drawString(col_x[1], y + 2, "Skóre")
    c.drawString(col_x[2], y + 2, "%")
    c.drawString(col_x[3], y + 2, "Status")
    y -= 6 * mm

    c.setStrokeColor(BORDER)
    c.setLineWidth(0.3)
    c.line(LM, y, RM, y)
    y -= 5 * mm

    # Table rows
    for ds in r.domain_scores:
        pct = round(ds.percentage)
        pc = _pc(ds.percentage)
        status_text = {"compliant": "OK", "partial": "Částečně", "non_compliant": "Nesplněno"}.get(ds.status, "")

        c.setFont(F, 8.5)
        c.setFillColor(TEXT)
        c.drawString(col_x[0], y, ds.domain_name_cs)

        c.setFillColor(TEXT2)
        c.drawString(col_x[1], y, f"{ds.score}/{ds.max_score}")

        c.setFont(FB, 8.5)
        c.setFillColor(pc)
        c.drawString(col_x[2], y, f"{pct}%")

        c.setFont(F, 8.5)
        c.setFillColor(pc)
        c.drawString(col_x[3], y, status_text)

        y -= 5 * mm
        c.setStrokeColor(HexColor("#f0f0f4"))
        c.setLineWidth(0.2)
        c.line(LM, y, RM, y)
        y -= 5 * mm

    y -= 6 * mm

    # Recommendation box
    c.setFillColor(LIGHT_BG)
    c.roundRect(LM, y - 40 * mm, CONTENT_W, 38 * mm, 4, fill=True, stroke=False)

    c.setStrokeColor(CHROME)
    c.setLineWidth(2)
    c.line(LM, y - 2 * mm, LM, y - 40 * mm)

    c.setFont(FB, 9)
    c.setFillColor(TEXT)
    c.drawString(LM + 8 * mm, y - 8 * mm, "Doporučení")

    if r.overall_percentage >= 80:
        rec = ("Vaše organizace vykazuje vysokou úroveň souladu. Zaměřte se na uzavření "
               "zbývajících mezer a zavedení pravidelného cyklu hodnocení (min. 1× ročně).")
    elif r.overall_percentage >= 50:
        rec = ("Vaše organizace má základy kybernetické bezpečnosti, ale vykazuje významné "
               "mezery. Doporučujeme prioritně řešit kritické nedostatky (váha 5/5) a "
               "vytvořit 90denní plán nápravy.")
    else:
        rec = ("Vaše organizace vykazuje závažné nedostatky v souladu s NIS2. Doporučujeme "
               "okamžitě zahájit nápravu kritických mezer, zvážit angažování externího "
               "konzultanta a vytvořit 30denní akční plán.")

    _draw_text(c, LM + 8 * mm, y - 16 * mm, rec, size=8.5, color=TEXT2, max_width=CONTENT_W - 16 * mm)


# ══════════════════════════════════════
# PAGE 3: RISK OVERVIEW + TIMELINE
# ══════════════════════════════════════

def _page_risk(c, r):
    c.setFillColor(HexColor("#ffffff"))
    c.rect(0, 0, W, H, fill=True, stroke=False)
    _page_header(c, 3)

    y = H - 28 * mm

    c.setFont(F, 7)
    c.setFillColor(CHROME)
    c.drawString(LM, y, "RISK OVERVIEW")
    y -= 6 * mm

    c.setFont(FB, 16)
    c.setFillColor(TEXT)
    c.drawString(LM, y, "Přehled rizik")
    y -= 12 * mm

    # Domain bars — visual risk heatmap
    bar_height = 10
    bar_max_w = CONTENT_W - 60 * mm

    for ds in r.domain_scores:
        pct = round(ds.percentage)
        pc = _pc(ds.percentage)
        bar_w = bar_max_w * (ds.percentage / 100)

        # Domain name
        c.setFont(F, 8)
        c.setFillColor(TEXT)
        c.drawString(LM, y, ds.domain_name_cs)

        # Bar track
        bar_x = LM + 62 * mm
        c.setFillColor(HexColor("#f0f0f4"))
        c.rect(bar_x, y - 2, bar_max_w, bar_height, fill=True, stroke=False)

        # Bar fill
        c.setFillColor(pc)
        c.rect(bar_x, y - 2, bar_w, bar_height, fill=True, stroke=False)

        # Percentage
        c.setFont(FB, 8)
        c.setFillColor(pc)
        c.drawRightString(RM, y, f"{pct}%")

        y -= 16 * mm

    y -= 6 * mm

    # Compliance timeline
    c.setFont(F, 7)
    c.setFillColor(CHROME)
    c.drawString(LM, y, "REMEDIATION TIMELINE")
    y -= 6 * mm

    c.setFont(FB, 14)
    c.setFillColor(TEXT)
    c.drawString(LM, y, "Doporučený harmonogram nápravy")
    y -= 12 * mm

    today = datetime.fromisoformat(r.timestamp)
    phases = [
        ("0–30 dní", (today + timedelta(days=30)).strftime("%d. %m. %Y"),
         "Řešení kritických mezer (váha 5/5), registrace u NÚKIB, jmenování odpovědné osoby"),
        ("30–60 dní", (today + timedelta(days=60)).strftime("%d. %m. %Y"),
         "Řešení mezer s váhou 4/5, zavedení MFA, vytvoření plánu kontinuity"),
        ("60–90 dní", (today + timedelta(days=90)).strftime("%d. %m. %Y"),
         "Řešení zbývajících mezer, školení zaměstnanců, provedení penetračního testu"),
        ("90+ dní", "Průběžně",
         "Pravidelné hodnocení, aktualizace politik, cvičení reakce na incidenty"),
    ]

    for phase, deadline, desc in phases:
        # Phase marker
        c.setFillColor(CHROME)
        c.circle(LM + 3, y + 2, 2.5, fill=True, stroke=False)

        # Vertical connector line
        if phase != "90+ dní":
            c.setStrokeColor(HexColor("#e0e0e8"))
            c.setLineWidth(0.5)
            c.line(LM + 3, y - 1, LM + 3, y - 18 * mm)

        c.setFont(FB, 9)
        c.setFillColor(TEXT)
        c.drawString(LM + 10 * mm, y, phase)

        c.setFont(F, 7.5)
        c.setFillColor(TEXT3)
        c.drawRightString(RM, y, f"Do: {deadline}")

        y -= 5 * mm
        y = _draw_text(c, LM + 10 * mm, y, desc, size=8, color=TEXT2, max_width=CONTENT_W - 20 * mm)
        y -= 12 * mm


# ══════════════════════════════════════
# PAGES 4+: PRIORITY ACTIONS
# ══════════════════════════════════════

def _pages_priorities(c, r):
    if not r.priority_actions:
        return

    c.showPage()
    c.setFillColor(HexColor("#ffffff"))
    c.rect(0, 0, W, H, fill=True, stroke=False)
    _page_header(c, 4)

    y = H - 28 * mm

    c.setFont(F, 7)
    c.setFillColor(CHROME)
    c.drawString(LM, y, "PRIORITY ACTIONS")
    y -= 6 * mm

    c.setFont(FB, 16)
    c.setFillColor(TEXT)
    c.drawString(LM, y, "Prioritní akce")
    y -= 4 * mm

    c.setFont(F, 8.5)
    c.setFillColor(TEXT2)
    c.drawString(LM, y, "Následující kroky mají nejvyšší prioritu. Seřazeno podle závažnosti.")
    y -= 12 * mm

    page_num = 4
    for i, gap in enumerate(r.priority_actions):
        needed_space = 40 * mm
        if y < needed_space:
            c.showPage()
            page_num += 1
            c.setFillColor(HexColor("#ffffff"))
            c.rect(0, 0, W, H, fill=True, stroke=False)
            _page_header(c, page_num)
            y = H - 28 * mm

        wt = gap["weight"]
        wc = RED if wt >= 5 else AMBER if wt >= 4 else DARK_GRAY

        # Severity indicator + left border
        c.setStrokeColor(wc)
        c.setLineWidth(2)
        c.line(LM, y + 4, LM, y - 28 * mm)

        # Weight badge
        c.setFillColor(wc)
        c.setFont(FB, 7)
        c.drawString(LM + 6 * mm, y, f"[{wt}/5]")

        # Question Czech
        c.setFont(FB, 9)
        c.setFillColor(TEXT)
        y = _draw_text(c, LM + 22 * mm, y, gap["question_cs"], font=FB, size=9, color=TEXT, max_width=CONTENT_W - 24 * mm)
        y -= 1 * mm

        # Question English
        y = _draw_text(c, LM + 6 * mm, y, gap["question_en"], size=8, color=TEXT3, max_width=CONTENT_W - 8 * mm)
        y -= 3 * mm

        # Remediation
        c.setFont(F, 8)
        c.setFillColor(CHROME)
        c.drawString(LM + 6 * mm, y, "→")
        y = _draw_text(c, LM + 12 * mm, y, gap["remediation"], size=8.5, color=TEXT2, max_width=CONTENT_W - 14 * mm)
        y -= 2 * mm

        # Reference
        c.setFont(F, 6.5)
        c.setFillColor(TEXT3)
        c.drawString(LM + 6 * mm, y, f"{gap['article_ref']}  ·  {gap['domain_name_cs']}")
        y -= 10 * mm

    return page_num


# ══════════════════════════════════════
# FINAL PAGES: FULL GAP ANALYSIS
# ══════════════════════════════════════

def _pages_gaps(c, r, start_page):
    page_num = start_page + 1
    c.showPage()
    c.setFillColor(HexColor("#ffffff"))
    c.rect(0, 0, W, H, fill=True, stroke=False)
    _page_header(c, page_num)

    y = H - 28 * mm

    c.setFont(F, 7)
    c.setFillColor(CHROME)
    c.drawString(LM, y, "FULL GAP ANALYSIS")
    y -= 6 * mm

    c.setFont(FB, 16)
    c.setFillColor(TEXT)
    c.drawString(LM, y, "Kompletní analýza mezer")
    y -= 10 * mm

    for ds in r.domain_scores:
        if not ds.gaps:
            continue

        needed = (len(ds.gaps) * 28 + 16) * mm
        if y < 50 * mm:
            c.showPage()
            page_num += 1
            c.setFillColor(HexColor("#ffffff"))
            c.rect(0, 0, W, H, fill=True, stroke=False)
            _page_header(c, page_num)
            y = H - 28 * mm

        # Domain header
        pct = round(ds.percentage)
        pc = _pc(ds.percentage)
        c.setFont(FB, 10)
        c.setFillColor(pc)
        c.drawString(LM, y, f"{pct}%")
        c.setFont(FB, 10)
        c.setFillColor(TEXT)
        c.drawString(LM + 16 * mm, y, ds.domain_name_cs)
        c.setFont(F, 8)
        c.setFillColor(TEXT3)
        c.drawString(LM + 16 * mm + c.stringWidth(ds.domain_name_cs, FB, 10) + 4 * mm, y, ds.domain_name_en)
        y -= 8 * mm

        for gap in ds.gaps:
            if y < 36 * mm:
                c.showPage()
                page_num += 1
                c.setFillColor(HexColor("#ffffff"))
                c.rect(0, 0, W, H, fill=True, stroke=False)
                _page_header(c, page_num)
                y = H - 28 * mm

            wt = gap["weight"]
            wc = RED if wt >= 5 else AMBER if wt >= 4 else DARK_GRAY

            c.setStrokeColor(wc)
            c.setLineWidth(1.5)
            c.line(LM, y + 3, LM, y - 20 * mm)

            c.setFont(F, 7)
            c.setFillColor(wc)
            c.drawString(LM + 4 * mm, y, f"[{wt}/5]")

            c.setFont(FB, 8.5)
            c.setFillColor(TEXT)
            y = _draw_text(c, LM + 18 * mm, y, gap["question_cs"], font=FB, size=8.5, color=TEXT, max_width=CONTENT_W - 20 * mm)

            y = _draw_text(c, LM + 4 * mm, y, gap["question_en"], size=7.5, color=TEXT3, max_width=CONTENT_W - 6 * mm)
            y -= 2 * mm

            c.setFillColor(CHROME)
            c.setFont(F, 7.5)
            c.drawString(LM + 4 * mm, y, "→")
            y = _draw_text(c, LM + 10 * mm, y, gap["remediation"], size=8, color=TEXT2, max_width=CONTENT_W - 12 * mm)
            y -= 1 * mm

            c.setFont(F, 6)
            c.setFillColor(TEXT3)
            c.drawString(LM + 4 * mm, y, gap["article_ref"])
            y -= 8 * mm

        y -= 4 * mm

    # Compliant domains
    ok = [d for d in r.domain_scores if not d.gaps]
    if ok:
        if y < 40 * mm:
            c.showPage()
            page_num += 1
            c.setFillColor(HexColor("#ffffff"))
            c.rect(0, 0, W, H, fill=True, stroke=False)
            _page_header(c, page_num)
            y = H - 28 * mm

        c.setFont(F, 7)
        c.setFillColor(CHROME)
        c.drawString(LM, y, "COMPLIANT DOMAINS")
        y -= 6 * mm

        c.setFont(FB, 11)
        c.setFillColor(TEXT)
        c.drawString(LM, y, "Domény v plném souladu")
        y -= 8 * mm

        for d in ok:
            c.setFont(F, 8.5)
            c.setFillColor(GREEN)
            c.drawString(LM, y, "●")
            c.setFillColor(TEXT)
            c.drawString(LM + 6 * mm, y, f"{d.domain_name_cs} — {round(d.percentage)}%")
            y -= 5 * mm

    # Legal footer
    y -= 8 * mm
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.3)
    c.line(LM, y, RM, y)
    y -= 6 * mm

    c.setFont(F, 7)
    c.setFillColor(CHROME)
    c.drawString(LM, y, "PRÁVNÍ ODKAZY")
    y -= 5 * mm

    legal = ("Hodnocení vychází z požadavků zákona č. 264/2025 Sb. o kybernetické bezpečnosti "
             "(směrnice EU NIS2 2022/2555) a pokynů NÚKIB. Report slouží jako interní nástroj "
             "a nepředstavuje právní posouzení ani certifikaci souladu.")
    _draw_text(c, LM, y, legal, size=7.5, color=TEXT3, max_width=CONTENT_W)


# ══════════════════════════════════════
# MAIN
# ══════════════════════════════════════

def generate_report(result: AssessmentResult) -> bytes:
    buf = io.BytesIO()
    c = canvas_module.Canvas(buf, pagesize=A4)

    # Page 1: Cover
    _page_cover(c, result)

    # Page 2: Executive summary + domain table
    c.showPage()
    _page_summary(c, result)

    # Page 3: Risk overview + timeline
    c.showPage()
    _page_risk(c, result)

    # Page 4+: Priority actions
    last_page = _pages_priorities(c, result) or 4

    # Final pages: Full gap analysis
    _pages_gaps(c, result, last_page)

    c.save()
    buf.seek(0)
    return buf.getvalue()
