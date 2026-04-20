"""
kOne PDF Report Generator — v4
Fixes: page 3 timeline text cutoff, Noxra Enterprises -> Noxra everywhere.
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
LM = 28 * mm
RM = W - 28 * mm
CONTENT_W = RM - LM

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
    return {"compliant": "Vyhovujici", "partial": "Castecne vyhovujici", "non_compliant": "Nevyhovujici"}.get(status, "")


def _draw_text(c, x, y, text, font=None, size=9, color=TEXT, max_width=None):
    c.setFont(font or F, size)
    c.setFillColor(color)
    if max_width and c.stringWidth(text, font or F, size) > max_width:
        words = text.split()
        lines = []
        current = ""
        for word in words:
            test = (current + " " + word).strip()
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
            c.drawString(x, y, line)
            y -= line_h
        return y
    else:
        c.drawString(x, y, text)
        return y - size * 1.5


def _chrome_line(c, y, width_pct=1.0):
    cx = W / 2
    half = (CONTENT_W * width_pct) / 2
    c.setStrokeColor(CHROME)
    c.setLineWidth(0.8)
    c.line(cx - half, y, cx + half, y)


def _page_header(c, page_num):
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.3)
    c.line(LM, H - 16 * mm, RM, H - 16 * mm)
    c.line(LM, 16 * mm, RM, 16 * mm)
    c.setFont(F, 6.5)
    c.setFillColor(TEXT3)
    c.drawString(LM, H - 13 * mm, "kOne - NIS2 Compliance Report")
    c.drawRightString(RM, H - 13 * mm, "Noxra  |  noxra.ai")
    c.drawCentredString(W / 2, 10 * mm, "Strana %d" % page_num)
    c.drawString(LM, 10 * mm, "Duverne")
    c.drawRightString(RM, 10 * mm, "2026 Noxra")


# ═══ PAGE 1: COVER ═══

def _page_cover(c, r):
    c.setFillColor(VOID)
    c.rect(0, 0, W, H, fill=True, stroke=False)
    _chrome_line(c, H - 20 * mm)

    c.setFont(FB, 10)
    c.setFillColor(CHROME)
    c.drawString(LM, H - 32 * mm, "kOne")
    c.setFont(F, 7)
    c.setFillColor(DARK_GRAY)
    c.drawString(LM + 30 * mm, H - 32 * mm, "NIS2 COMPLIANCE REPORT")

    date_str = datetime.fromisoformat(r.timestamp).strftime("%d. %m. %Y")
    c.setFont(F, 8)
    c.setFillColor(GRAY)
    c.drawRightString(RM, H - 32 * mm, date_str)

    c.setFont(FB, 30)
    c.setFillColor(WHITE)
    c.drawString(LM, H - 62 * mm, r.company_name)

    c.setFont(F, 9)
    c.setFillColor(GRAY)
    size_labels = {"micro": "1-9 zamestnancu", "small": "10-49", "medium": "50-249", "large": "250+"}
    c.drawString(LM, H - 74 * mm, "%s  |  %s" % (r.sector, size_labels.get(r.company_size, r.company_size)))

    c.setStrokeColor(HexColor("#ffffff08"))
    c.setLineWidth(0.3)
    c.line(LM, H - 82 * mm, RM, H - 82 * mm)

    pct = round(r.overall_percentage)
    cx = W / 2
    cy = H / 2 - 8 * mm
    radius = 42 * mm
    color = _sc(r.overall_status)

    c.setStrokeColor(color)
    c.setLineWidth(2)
    c.circle(cx, cy, radius, fill=False, stroke=True)
    c.setLineWidth(0.3)
    c.circle(cx, cy, radius - 6 * mm, fill=False, stroke=True)

    c.setFont(FB, 64)
    c.setFillColor(color)
    c.drawCentredString(cx, cy - 18, "%d%%" % pct)

    c.setFont(F, 10)
    c.setFillColor(GRAY)
    c.drawCentredString(cx, cy - 36, "%s / %s bodu" % (r.overall_score, r.max_score))

    c.setFont(F, 10)
    c.setFillColor(color)
    c.drawCentredString(cx, cy - radius - 16 * mm, _sl(r.overall_status).upper())

    sy = 50 * mm
    box_h = 36 * mm
    box_w = CONTENT_W / 3 - 3 * mm
    positions = [
        (LM, str(r.critical_gaps), "Kritickych mezer"),
        (LM + CONTENT_W / 3 + 1.5 * mm, str(r.total_gaps), "Celkem mezer"),
        (LM + 2 * CONTENT_W / 3 + 3 * mm, "%d/%d" % (len([d for d in r.domain_scores if d.status == "compliant"]), len(r.domain_scores)), "Domen v souladu"),
    ]
    for bx, val, lbl in positions:
        c.setFillColor(SURFACE)
        c.roundRect(bx, sy, box_w, box_h, 3, fill=True, stroke=False)
        c.setFillColor(WHITE)
        c.setFont(FB, 24)
        c.drawCentredString(bx + box_w / 2, sy + box_h / 2 + 2, val)
        c.setFillColor(GRAY)
        c.setFont(F, 7)
        c.drawCentredString(bx + box_w / 2, sy + 8, lbl)

    _chrome_line(c, 38 * mm)
    c.setFont(F, 6.5)
    c.setFillColor(DARK_GRAY)
    c.drawCentredString(W / 2, 28 * mm, "2026 Noxra  |  noxra.ai  |  Zakon c. 264/2025 Sb.  |  Duverne")


# ═══ PAGE 2: EXECUTIVE SUMMARY + DOMAIN TABLE ═══

def _page_summary(c, r):
    c.setFillColor(HexColor("#ffffff"))
    c.rect(0, 0, W, H, fill=True, stroke=False)
    _page_header(c, 2)

    y = H - 28 * mm

    c.setFont(F, 7)
    c.setFillColor(CHROME)
    c.drawString(LM, y, "EXECUTIVE SUMMARY")
    y -= 6 * mm

    c.setFont(FB, 16)
    c.setFillColor(TEXT)
    c.drawString(LM, y, "Shrnuti hodnoceni")
    y -= 10 * mm

    date_str = datetime.fromisoformat(r.timestamp).strftime("%d. %m. %Y")
    sl = _sl(r.overall_status)
    compliant_count = len([d for d in r.domain_scores if d.status == "compliant"])

    text1 = ("Organizace %s dosahla celkoveho skore souladu "
             "%d%% (%s/%s bodu), "
             "coz odpovida statusu \"%s\". Hodnoceni provedeno dne %s." % (
                 r.company_name, round(r.overall_percentage),
                 r.overall_score, r.max_score, sl, date_str))
    y = _draw_text(c, LM, y, text1, size=9.5, color=TEXT, max_width=CONTENT_W)
    y -= 4 * mm

    text2 = ("Identifikovano %d mezer v souladu, "
             "z toho %d kritickych (vaha 4-5 z 5). "
             "Z %d hodnocenych domen je %d v plnem souladu." % (
                 r.total_gaps, r.critical_gaps,
                 len(r.domain_scores), compliant_count))
    y = _draw_text(c, LM, y, text2, size=9.5, color=TEXT, max_width=CONTENT_W)
    y -= 12 * mm

    c.setFont(F, 7)
    c.setFillColor(CHROME)
    c.drawString(LM, y, "DOMAIN BREAKDOWN")
    y -= 6 * mm

    c.setFont(FB, 14)
    c.setFillColor(TEXT)
    c.drawString(LM, y, "Prehled domen")
    y -= 10 * mm

    col_x = [LM, LM + 100 * mm, LM + 125 * mm, LM + 142 * mm]
    c.setFillColor(LIGHT_BG)
    c.rect(LM - 2 * mm, y - 2, CONTENT_W + 4 * mm, 14, fill=True, stroke=False)
    c.setFont(FB, 7)
    c.setFillColor(TEXT3)
    c.drawString(col_x[0], y + 2, "Domena")
    c.drawString(col_x[1], y + 2, "Skore")
    c.drawString(col_x[2], y + 2, "%")
    c.drawString(col_x[3], y + 2, "Status")
    y -= 6 * mm

    c.setStrokeColor(BORDER)
    c.setLineWidth(0.3)
    c.line(LM, y, RM, y)
    y -= 5 * mm

    for ds in r.domain_scores:
        pct = round(ds.percentage)
        pc = _pc(ds.percentage)
        status_text = {"compliant": "OK", "partial": "Castecne", "non_compliant": "Nesplneno"}.get(ds.status, "")

        c.setFont(F, 8.5)
        c.setFillColor(TEXT)
        c.drawString(col_x[0], y, ds.domain_name_cs)
        c.setFillColor(TEXT2)
        c.drawString(col_x[1], y, "%s/%s" % (ds.score, ds.max_score))
        c.setFont(FB, 8.5)
        c.setFillColor(pc)
        c.drawString(col_x[2], y, "%d%%" % pct)
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
    c.drawString(LM + 8 * mm, y - 8 * mm, "Doporuceni")

    if r.overall_percentage >= 80:
        rec = ("Vase organizace vykazuje vysokou uroven souladu. Zamerte se na uzavreni "
               "zbyvajicich mezer a zavedeni pravidelneho cyklu hodnoceni.")
    elif r.overall_percentage >= 50:
        rec = ("Vase organizace ma zaklady kyberneticke bezpecnosti, ale vykazuje vyznamne "
               "mezery. Doporucujeme prioritne resit kriticke nedostatky a "
               "vytvorit 90denni plan napravy.")
    else:
        rec = ("Vase organizace vykazuje zavazne nedostatky v souladu s NIS2. Doporucujeme "
               "okamzite zahajit napravu kritickych mezer a vytvorit 30denni akcni plan.")

    _draw_text(c, LM + 8 * mm, y - 16 * mm, rec, size=8.5, color=TEXT2, max_width=CONTENT_W - 16 * mm)


# ═══ PAGE 3: RISK OVERVIEW ═══

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
    c.drawString(LM, y, "Prehled rizik")
    y -= 12 * mm

    bar_max_w = CONTENT_W - 60 * mm

    for ds in r.domain_scores:
        pct = round(ds.percentage)
        pc = _pc(ds.percentage)
        bar_w = bar_max_w * (ds.percentage / 100)

        c.setFont(F, 8)
        c.setFillColor(TEXT)
        c.drawString(LM, y, ds.domain_name_cs)

        bar_x = LM + 62 * mm
        c.setFillColor(HexColor("#f0f0f4"))
        c.rect(bar_x, y - 2, bar_max_w, 10, fill=True, stroke=False)
        c.setFillColor(pc)
        c.rect(bar_x, y - 2, bar_w, 10, fill=True, stroke=False)

        c.setFont(FB, 8)
        c.setFillColor(pc)
        c.drawRightString(RM, y, "%d%%" % pct)

        y -= 16 * mm

    # Check remaining space — if not enough for timeline, go to page 4
    # Timeline needs roughly 120mm
    if y < 140 * mm:
        return y  # Signal that we need a new page for timeline

    y -= 6 * mm
    _draw_timeline(c, r, y)
    return 0  # Signal timeline was drawn


def _draw_timeline(c, r, y):
    c.setFont(F, 7)
    c.setFillColor(CHROME)
    c.drawString(LM, y, "REMEDIATION TIMELINE")
    y -= 6 * mm

    c.setFont(FB, 14)
    c.setFillColor(TEXT)
    c.drawString(LM, y, "Doporuceny harmonogram napravy")
    y -= 14 * mm

    today = datetime.fromisoformat(r.timestamp)
    phases = [
        ("0-30 dni", (today + timedelta(days=30)).strftime("%d. %m. %Y"),
         "Reseni kritickych mezer (vaha 5/5), registrace u NUKIB, jmenovani odpovedne osoby"),
        ("30-60 dni", (today + timedelta(days=60)).strftime("%d. %m. %Y"),
         "Reseni mezer s vahou 4/5, zavedeni MFA, vytvoreni planu kontinuity"),
        ("60-90 dni", (today + timedelta(days=90)).strftime("%d. %m. %Y"),
         "Reseni zbyvajicich mezer, skoleni zamestnancu, provedeni penetracniho testu"),
        ("90+ dni", "Prubezne",
         "Pravidelne hodnoceni, aktualizace politik, cviceni reakce na incidenty"),
    ]

    for i, (phase, deadline, desc) in enumerate(phases):
        c.setFillColor(CHROME)
        c.circle(LM + 3, y + 2, 2.5, fill=True, stroke=False)

        if i < len(phases) - 1:
            c.setStrokeColor(HexColor("#e0e0e8"))
            c.setLineWidth(0.5)
            c.line(LM + 3, y - 1, LM + 3, y - 20 * mm)

        c.setFont(FB, 9)
        c.setFillColor(TEXT)
        c.drawString(LM + 10 * mm, y, phase)

        c.setFont(F, 7.5)
        c.setFillColor(TEXT3)
        c.drawRightString(RM, y, "Do: %s" % deadline)

        y -= 5 * mm
        y = _draw_text(c, LM + 10 * mm, y, desc, size=8, color=TEXT2, max_width=CONTENT_W - 20 * mm)
        y -= 14 * mm


# ═══ PAGES 4+: PRIORITY ACTIONS ═══

def _pages_priorities(c, r, start_page):
    if not r.priority_actions:
        return start_page

    page_num = start_page
    c.showPage()
    c.setFillColor(HexColor("#ffffff"))
    c.rect(0, 0, W, H, fill=True, stroke=False)
    _page_header(c, page_num)

    y = H - 28 * mm

    c.setFont(F, 7)
    c.setFillColor(CHROME)
    c.drawString(LM, y, "PRIORITY ACTIONS")
    y -= 6 * mm

    c.setFont(FB, 16)
    c.setFillColor(TEXT)
    c.drawString(LM, y, "Prioritni akce")
    y -= 4 * mm

    c.setFont(F, 8.5)
    c.setFillColor(TEXT2)
    c.drawString(LM, y, "Nasledujici kroky maji nejvyssi prioritu. Serazeno podle zavaznosti.")
    y -= 12 * mm

    for gap in r.priority_actions:
        if y < 50 * mm:
            c.showPage()
            page_num += 1
            c.setFillColor(HexColor("#ffffff"))
            c.rect(0, 0, W, H, fill=True, stroke=False)
            _page_header(c, page_num)
            y = H - 28 * mm

        wt = gap["weight"]
        wc = RED if wt >= 5 else AMBER if wt >= 4 else DARK_GRAY

        c.setStrokeColor(wc)
        c.setLineWidth(2)
        c.line(LM, y + 4, LM, y - 28 * mm)

        c.setFillColor(wc)
        c.setFont(FB, 7)
        c.drawString(LM + 6 * mm, y, "[%d/5]" % wt)

        c.setFont(FB, 9)
        c.setFillColor(TEXT)
        y = _draw_text(c, LM + 22 * mm, y, gap["question_cs"], font=FB, size=9, color=TEXT, max_width=CONTENT_W - 24 * mm)
        y -= 1 * mm

        y = _draw_text(c, LM + 6 * mm, y, gap["question_en"], size=8, color=TEXT3, max_width=CONTENT_W - 8 * mm)
        y -= 3 * mm

        c.setFont(F, 8)
        c.setFillColor(CHROME)
        c.drawString(LM + 6 * mm, y, "->")
        y = _draw_text(c, LM + 12 * mm, y, gap["remediation"], size=8.5, color=TEXT2, max_width=CONTENT_W - 14 * mm)
        y -= 2 * mm

        c.setFont(F, 6.5)
        c.setFillColor(TEXT3)
        c.drawString(LM + 6 * mm, y, "%s  |  %s" % (gap["article_ref"], gap["domain_name_cs"]))
        y -= 10 * mm

    return page_num


# ═══ FINAL PAGES: FULL GAP ANALYSIS ═══

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
    c.drawString(LM, y, "Kompletni analyza mezer")
    y -= 10 * mm

    for ds in r.domain_scores:
        if not ds.gaps:
            continue

        if y < 50 * mm:
            c.showPage()
            page_num += 1
            c.setFillColor(HexColor("#ffffff"))
            c.rect(0, 0, W, H, fill=True, stroke=False)
            _page_header(c, page_num)
            y = H - 28 * mm

        pct = round(ds.percentage)
        pc = _pc(ds.percentage)
        c.setFont(FB, 10)
        c.setFillColor(pc)
        c.drawString(LM, y, "%d%%" % pct)
        c.setFont(FB, 10)
        c.setFillColor(TEXT)
        c.drawString(LM + 16 * mm, y, ds.domain_name_cs)
        y -= 8 * mm

        for gap in ds.gaps:
            if y < 40 * mm:
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
            c.drawString(LM + 4 * mm, y, "[%d/5]" % wt)

            c.setFont(FB, 8.5)
            c.setFillColor(TEXT)
            y = _draw_text(c, LM + 18 * mm, y, gap["question_cs"], font=FB, size=8.5, color=TEXT, max_width=CONTENT_W - 20 * mm)

            y = _draw_text(c, LM + 4 * mm, y, gap["question_en"], size=7.5, color=TEXT3, max_width=CONTENT_W - 6 * mm)
            y -= 2 * mm

            c.setFillColor(CHROME)
            c.setFont(F, 7.5)
            c.drawString(LM + 4 * mm, y, "->")
            y = _draw_text(c, LM + 10 * mm, y, gap["remediation"], size=8, color=TEXT2, max_width=CONTENT_W - 12 * mm)
            y -= 1 * mm

            c.setFont(F, 6)
            c.setFillColor(TEXT3)
            c.drawString(LM + 4 * mm, y, gap["article_ref"])
            y -= 8 * mm

        y -= 4 * mm

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
        c.drawString(LM, y, "Domeny v plnem souladu")
        y -= 8 * mm

        for d in ok:
            c.setFont(F, 8.5)
            c.setFillColor(GREEN)
            c.drawString(LM, y, ">")
            c.setFillColor(TEXT)
            c.drawString(LM + 6 * mm, y, "%s - %d%%" % (d.domain_name_cs, round(d.percentage)))
            y -= 5 * mm

    y -= 8 * mm
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.3)
    c.line(LM, y, RM, y)
    y -= 6 * mm

    c.setFont(F, 7)
    c.setFillColor(CHROME)
    c.drawString(LM, y, "PRAVNI ODKAZY")
    y -= 5 * mm

    legal = ("Hodnoceni vychazi z pozadavku zakona c. 264/2025 Sb. o kyberneticke bezpecnosti "
             "(smernice EU NIS2 2022/2555) a pokynu NUKIB. Report slouzi jako interni nastroj "
             "a nepredstavuje pravni posouzeni ani certifikaci souladu.")
    _draw_text(c, LM, y, legal, size=7.5, color=TEXT3, max_width=CONTENT_W)


# ═══ MAIN ═══

def generate_report(result: AssessmentResult) -> bytes:
    buf = io.BytesIO()
    c = canvas_module.Canvas(buf, pagesize=A4)

    # Page 1: Cover
    _page_cover(c, result)

    # Page 2: Executive summary + domain table
    c.showPage()
    _page_summary(c, result)

    # Page 3: Risk overview
    c.showPage()
    remaining_y = _page_risk(c, result)

    # If timeline didn't fit on page 3, put it on page 4
    if remaining_y > 0:
        c.showPage()
        c.setFillColor(HexColor("#ffffff"))
        c.rect(0, 0, W, H, fill=True, stroke=False)
        _page_header(c, 4)
        _draw_timeline(c, result, H - 28 * mm)
        next_page = 5
    else:
        next_page = 4

    # Priority actions
    last_page = _pages_priorities(c, result, next_page)

    # Full gap analysis
    _pages_gaps(c, result, last_page)

    c.save()
    buf.seek(0)
    return buf.getvalue()
