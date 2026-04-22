"""Generate Finnish CV PDF matching the EN layout (2-column, dark sidebar)."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.platypus import Paragraph, Frame, PageTemplate, BaseDocTemplate, Spacer, Table, TableStyle, PageBreak, FrameBreak, Flowable
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.units import mm, cm
import os

OUT = r"D:\1.GITHUB\renata-resume\docs\cv-fi-pdf\Renata-Baldissara-Kunnela-CV-FI.pdf"
os.makedirs(os.path.dirname(OUT), exist_ok=True)

# Colors from EN PDF
SIDEBAR_BG = HexColor("#0f1e3a")
MAIN_BG = HexColor("#ffffff")
ACCENT = HexColor("#4ea5ff")
ACCENT_DARK = HexColor("#1e3a5f")
TEXT_LIGHT = HexColor("#c6d2e4")
TEXT_LIGHT_DIM = HexColor("#8a9bb5")
TEXT_DARK = HexColor("#1a1f2e")
TEXT_MUTED = HexColor("#5a6578")
CHIP_BG = HexColor("#e9f1fc")
QUOTE_BORDER = ACCENT
STAT_BG = HexColor("#e9f1fc")
CARD_BORDER = ACCENT

PAGE_W, PAGE_H = A4
SIDEBAR_W = 65 * mm
MAIN_W = PAGE_W - SIDEBAR_W
MARGIN = 8 * mm

# Try to register Helvetica family — default in reportlab supports Latin1 with ä/ö
FONT_REG = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
FONT_OBL = "Helvetica-Oblique"


def p(text, style):
    return Paragraph(text, style)


# ---------- Styles ----------
STY = {}
STY["sb_name"] = ParagraphStyle("sb_name", fontName=FONT_BOLD, fontSize=18, leading=21, textColor=white, spaceAfter=0)
STY["sb_name_accent"] = ParagraphStyle("sb_name_accent", fontName=FONT_BOLD, fontSize=18, leading=21, textColor=ACCENT, spaceAfter=2)
STY["sb_title"] = ParagraphStyle("sb_title", fontName=FONT_BOLD, fontSize=9, leading=12, textColor=ACCENT, spaceAfter=10, spaceBefore=4)
STY["sb_h"] = ParagraphStyle("sb_h", fontName=FONT_BOLD, fontSize=9, leading=12, textColor=ACCENT, spaceBefore=12, spaceAfter=6)
STY["sb_label"] = ParagraphStyle("sb_label", fontName=FONT_REG, fontSize=8, leading=11, textColor=TEXT_LIGHT_DIM)
STY["sb_value"] = ParagraphStyle("sb_value", fontName=FONT_REG, fontSize=8, leading=11, textColor=TEXT_LIGHT)
STY["sb_skill_cat"] = ParagraphStyle("sb_skill_cat", fontName=FONT_BOLD, fontSize=9, leading=12, textColor=white, spaceBefore=6, spaceAfter=4)
STY["sb_cert"] = ParagraphStyle("sb_cert", fontName=FONT_REG, fontSize=8, leading=11, textColor=TEXT_LIGHT, leftIndent=8)
STY["sb_cert_date"] = ParagraphStyle("sb_cert_date", fontName=FONT_REG, fontSize=7, leading=10, textColor=TEXT_LIGHT_DIM, leftIndent=8, spaceAfter=4)
STY["sb_focus_h"] = ParagraphStyle("sb_focus_h", fontName=FONT_BOLD, fontSize=9, leading=12, textColor=white, spaceBefore=6, spaceAfter=2)
STY["sb_focus_b"] = ParagraphStyle("sb_focus_b", fontName=FONT_REG, fontSize=8, leading=11, textColor=TEXT_LIGHT, spaceAfter=6)
STY["sb_quote"] = ParagraphStyle("sb_quote", fontName=FONT_OBL, fontSize=8, leading=11, textColor=TEXT_LIGHT_DIM, leftIndent=6, spaceBefore=10)
STY["sb_lang_name"] = ParagraphStyle("sb_lang_name", fontName=FONT_BOLD, fontSize=9, leading=12, textColor=white)
STY["sb_lang_lvl"] = ParagraphStyle("sb_lang_lvl", fontName=FONT_OBL, fontSize=8, leading=12, textColor=TEXT_LIGHT_DIM, alignment=TA_RIGHT)

STY["m_name"] = ParagraphStyle("m_name", fontName=FONT_BOLD, fontSize=24, leading=28, textColor=TEXT_DARK, spaceAfter=2)
STY["m_sub"] = ParagraphStyle("m_sub", fontName=FONT_REG, fontSize=12, leading=15, textColor=ACCENT, spaceAfter=6)
STY["m_avail"] = ParagraphStyle("m_avail", fontName=FONT_BOLD, fontSize=9, leading=12, textColor=HexColor("#1f9d55"), spaceAfter=10)
STY["m_quote"] = ParagraphStyle("m_quote", fontName=FONT_REG, fontSize=10, leading=14, textColor=TEXT_DARK, leftIndent=8, spaceAfter=12)
STY["m_h"] = ParagraphStyle("m_h", fontName=FONT_BOLD, fontSize=11, leading=14, textColor=TEXT_DARK, spaceBefore=10, spaceAfter=6)
STY["m_h_side"] = ParagraphStyle("m_h_side", fontName=FONT_REG, fontSize=8, leading=10, textColor=TEXT_MUTED, alignment=TA_RIGHT)
STY["m_body"] = ParagraphStyle("m_body", fontName=FONT_REG, fontSize=9, leading=13, textColor=TEXT_DARK, spaceAfter=8)
STY["m_job"] = ParagraphStyle("m_job", fontName=FONT_BOLD, fontSize=10, leading=13, textColor=TEXT_DARK, spaceAfter=2)
STY["m_job_co"] = ParagraphStyle("m_job_co", fontName=FONT_BOLD, fontSize=10, leading=13, textColor=ACCENT)
STY["m_date"] = ParagraphStyle("m_date", fontName=FONT_REG, fontSize=8, leading=11, textColor=TEXT_MUTED, alignment=TA_RIGHT)
STY["m_stat_n"] = ParagraphStyle("m_stat_n", fontName=FONT_BOLD, fontSize=18, leading=20, textColor=TEXT_DARK)
STY["m_stat_l"] = ParagraphStyle("m_stat_l", fontName=FONT_REG, fontSize=7, leading=9, textColor=TEXT_MUTED)
STY["m_proj_name"] = ParagraphStyle("m_proj_name", fontName=FONT_BOLD, fontSize=10, leading=13, textColor=TEXT_DARK)
STY["m_proj_tag"] = ParagraphStyle("m_proj_tag", fontName=FONT_BOLD, fontSize=7, leading=10, textColor=TEXT_MUTED, alignment=TA_RIGHT)
STY["m_stack"] = ParagraphStyle("m_stack", fontName=FONT_REG, fontSize=8, leading=11, textColor=TEXT_MUTED, spaceBefore=4)
STY["m_edu_deg"] = ParagraphStyle("m_edu_deg", fontName=FONT_BOLD, fontSize=9, leading=12, textColor=TEXT_DARK)
STY["m_edu_inst"] = ParagraphStyle("m_edu_inst", fontName=FONT_REG, fontSize=9, leading=12, textColor=TEXT_DARK)
STY["m_edu_yr"] = ParagraphStyle("m_edu_yr", fontName=FONT_REG, fontSize=8, leading=11, textColor=TEXT_MUTED)
STY["m_foot"] = ParagraphStyle("m_foot", fontName=FONT_REG, fontSize=7, leading=10, textColor=TEXT_MUTED)


class ChipFlow(Flowable):
    """Flow of rounded pill chips with wrapping."""
    def __init__(self, items, max_width, font=FONT_REG, font_size=7,
                 pad_x=6, pad_y=3, gap_x=4, gap_y=4,
                 bg=HexColor("#1b2d4e"), border=HexColor("#30466e"),
                 text_color=white, radius=7):
        super().__init__()
        self.items = items
        self.max_width = max_width
        self.font = font
        self.font_size = font_size
        self.pad_x = pad_x
        self.pad_y = pad_y
        self.gap_x = gap_x
        self.gap_y = gap_y
        self.bg = bg
        self.border = border
        self.text_color = text_color
        self.radius = radius
        self._layout()

    def _layout(self):
        lines, cur, cur_w = [], [], 0
        chip_h = self.font_size + 2 * self.pad_y
        for it in self.items:
            tw = stringWidth(it, self.font, self.font_size) + 2 * self.pad_x
            if cur and cur_w + self.gap_x + tw > self.max_width:
                lines.append(cur); cur = [(it, tw)]; cur_w = tw
            else:
                if cur: cur_w += self.gap_x
                cur.append((it, tw)); cur_w += tw
        if cur: lines.append(cur)
        self._lines = lines
        self._chip_h = chip_h
        self.width = self.max_width
        self.height = len(lines) * chip_h + max(0, len(lines) - 1) * self.gap_y

    def wrap(self, aw, ah):
        return self.width, self.height

    def draw(self):
        c = self.canv
        y = self.height - self._chip_h
        for line in self._lines:
            x = 0
            for text, tw in line:
                c.setFillColor(self.bg)
                c.setStrokeColor(self.border)
                c.setLineWidth(0.4)
                c.roundRect(x, y, tw, self._chip_h, self.radius, stroke=1, fill=1)
                c.setFillColor(self.text_color)
                c.setFont(self.font, self.font_size)
                c.drawString(x + self.pad_x, y + self.pad_y + 1, text)
                x += tw + self.gap_x
            y -= self._chip_h + self.gap_y


def chip_table(items, per_row=3):
    return ChipFlow(items, SIDEBAR_W - 2 * MARGIN)


def lang_row(name, level):
    t = Table([[Paragraph(name, STY["sb_lang_name"]), Paragraph(level, STY["sb_lang_lvl"])]],
              colWidths=[(SIDEBAR_W - 2 * MARGIN) * 0.55, (SIDEBAR_W - 2 * MARGIN) * 0.45])
    t.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 0.3, TEXT_LIGHT_DIM),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def stats_bar(stats):
    rows = [[]]
    for n, lbl in stats:
        inner = [[Paragraph(n, STY["m_stat_n"])], [Paragraph(lbl, STY["m_stat_l"])]]
        it = Table(inner, colWidths=[(MAIN_W - 2 * MARGIN) / len(stats) - 6])
        it.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), STAT_BG),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        rows[0].append(it)
    t = Table(rows, colWidths=[(MAIN_W - 2 * MARGIN) / len(stats)] * len(stats))
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
    ]))
    return t


def quote_block(text):
    inner = Table([[Paragraph(text, STY["m_quote"])]], colWidths=[MAIN_W - 2 * MARGIN - 12])
    inner.setStyle(TableStyle([
        ("LINEBEFORE", (0, 0), (0, 0), 2, QUOTE_BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return inner


def job_header(company, role, date):
    t = Table([[Paragraph(f'<font color="#4ea5ff"><b>{company}</b></font> — <b>{role}</b>', STY["m_job"]),
                Paragraph(date, STY["m_date"])]],
              colWidths=[(MAIN_W - 2 * MARGIN) * 0.72, (MAIN_W - 2 * MARGIN) * 0.28])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    return t


def section_h(left, right):
    t = Table([[Paragraph(f"<b>{left}</b>", STY["m_h"]), Paragraph(right, STY["m_h_side"])]],
              colWidths=[(MAIN_W - 2 * MARGIN) * 0.5, (MAIN_W - 2 * MARGIN) * 0.5])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
                           ("LINEBELOW", (0, 0), (-1, -1), 0.5, HexColor("#d1d9e3")),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    return t


def project_card(name, tag, desc, stack):
    inner = [
        [Paragraph(name, STY["m_proj_name"]), Paragraph(tag, STY["m_proj_tag"])],
        [Paragraph(desc, STY["m_body"]), ""],
        [Paragraph(f'<font color="#5a6578"><b>TEKNOLOGIAT</b> {stack}</font>', STY["m_stack"]), ""],
    ]
    t = Table(inner, colWidths=[(MAIN_W - 2 * MARGIN) * 0.66 - 10, (MAIN_W - 2 * MARGIN) * 0.34 - 10])
    t.setStyle(TableStyle([
        ("SPAN", (0, 1), (1, 1)),
        ("SPAN", (0, 2), (1, 2)),
        ("LINEBEFORE", (0, 0), (0, -1), 2, ACCENT),
        ("BACKGROUND", (0, 0), (-1, -1), HexColor("#fafbfd")),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def edu_row(deg, inst, yrs):
    return [Paragraph(deg, STY["m_edu_deg"]), Paragraph(inst, STY["m_edu_inst"]), Paragraph(yrs, STY["m_edu_yr"])]


# ---------- Content ----------
SIDEBAR_1 = [
    p("Renata", STY["sb_name"]),
    p("Baldissara-", STY["sb_name_accent"]),
    p("Kunnela", STY["sb_name_accent"]),
    p("AI-KEHITTÄJÄ", STY["sb_title"]),
    p("YHTEYSTIEDOT", STY["sb_h"]),
]

contact_rows = [
    ("Sähköposti", "renatbk.linkedin@gmail.com"),
    ("Puhelin", "+358 401829008"),
    ("LinkedIn", "renata-kunnela-4002a726a"),
    ("GitHub", "RBKunnela"),
    ("Sijainti", "Viitasaari, Suomi"),
    ("Portfolio", "renata-resume.vercel.app"),
]
for k, v in contact_rows:
    tt = Table([[Paragraph(k, STY["sb_label"]), Paragraph(v, STY["sb_value"])]],
               colWidths=[(SIDEBAR_W - 2 * MARGIN) * 0.35, (SIDEBAR_W - 2 * MARGIN) * 0.65])
    tt.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ("TOPPADDING", (0, 0), (-1, -1), 1),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 1)]))
    SIDEBAR_1.append(tt)

SIDEBAR_1 += [
    p("YDINOSAAMINEN", STY["sb_h"]),
    p("AI &amp; LLM", STY["sb_skill_cat"]),
    chip_table(["OpenAI", "Claude", "Azure OpenAI", "Gemini", "LangChain", "LlamaIndex",
                "RAG", "Fine-tuning", "Guardrails", "LLM-as-judge"]),
    p("Engineering", STY["sb_skill_cat"]),
    chip_table(["Python", "FastAPI", "Pydantic", "PostgreSQL", "Redis", "REST",
                "OAuth2", "Docker", "CI/CD"]),
    p("QA &amp; Testing", STY["sb_skill_cat"]),
    chip_table(["Robot Framework", "Postman", "TestRail", "Jira", "RAML/MuleSoft", "ISTQB"]),
    p("KIELET", STY["sb_h"]),
    lang_row("Portugali", "Äidinkieli"),
    lang_row("Englanti", "Erinomainen"),
    lang_row("Suomi", "Sujuva (työskentelykieli)"),
    lang_row("Espanja", "Sujuva"),
]

MAIN_1 = [
    p("Renata Baldissara-Kunnela", STY["m_name"]),
    p("AI Developer — LLM- &amp; agenttiratkaisut", STY["m_sub"]),
    p("● Avoinna uusille mahdollisuuksille", STY["m_avail"]),
    quote_block("Rakennan tuotantotason LLM- ja agenttijärjestelmiä yli 15 vuoden kokemuksella enterprise-järjestelmistä. Muutan monimutkaisen tekoälyn luotettavaksi, mitattavaksi liiketoiminta-arvoksi."),
    stats_bar([
        ("15+", "VUODEN<br/>KOKEMUS"),
        ("4", "AI-TUOTETTA<br/>TUOTANNOSSA"),
        ("3", "AVOIMEN<br/>LÄHDEKOODIN<br/>KEHYSTÄ"),
        ("4", "PUHUTTUA<br/>KIELTÄ"),
    ]),
    Spacer(1, 8),
    section_h("PROFIILI", ""),
    p("AI Developer ja AI Quality Engineering -osaaja, jolla on yli 15 vuoden tausta enterprise-järjestelmissä (pankki-, vakuutus- ja integraatioympäristöt). Rakennan tuotantotason LLM- ja agenttiratkaisuja liiketoimintaprosesseihin (structured prompting, RAG, fine-tuning, tool-orkestrointi) sekä toteutan luotettavuuden varmistavat mekanismit: guardrails, fallback-logiikka ja automaattinen evaluointi (LLM-as-judge + sääntöpohjaiset tarkistukset) regressiotestauksen ja jatkuvan parantamisen tueksi. Olen tottunut ottamaan vastuuta laadusta, testattavuudesta ja tuotantovalmiudesta koko kehityssyklin läpi.", STY["m_body"]),
    section_h("TYÖKOKEMUS", "URAPOLKU"),
    job_header("FriendlyAI", "AI Developer &amp; Quality Engineering", "02/2025 — Nykyhetki"),
    p("Tuotantotason avustimia ja automaatioratkaisuja asiakaspalveluun ja liidien generointiin. Toteutin seurannan ja laatumetriikat, jatkuva parantaminen evaluointisilmukoiden kautta. Keskittyminen LLM:n luotettavaan käyttäytymiseen, mitattaviin tuloksiin ja integrointiin olemassa oleviin liiketoimintaprosesseihin.", STY["m_body"]),
    job_header("TietoEvry / Fennia", "API Tester &amp; Quality Engineering", "09/2023 — 02/2025"),
    p("API-laatu ja testausstrategia RAML/MuleSoft-rajapinnoille (TestRail, Jira). Postman-automaatio ja evidenssi release-valmiuden tueksi. Yhteistyö kehittäjien ja arkkitehtien kanssa integraatio-ongelmien ratkaisemiseksi monimutkaisissa vakuutusjärjestelmissä.", STY["m_body"]),
    job_header("Samlink Oyj", "Senior Test Automation Engineer", "01/2016 — 03/2023"),
    p("Testiautomaation kehitys pankkitason järjestelmiin (Robot Framework + Python). Skaalautuvat QA-käytännöt integraatiokeskeisiin palveluketjuihin ja tuotantovalmiuden varmistus tiukoissa luotettavuus- ja auditointivaatimuksissa.", STY["m_body"]),
]

# Page 2
SIDEBAR_2 = [
    p("Renata", STY["sb_name"]),
    p("Baldissara-Kunnela", STY["sb_name_accent"]),
    p("AI DEVELOPER", STY["sb_title"]),
    p("SERTIFIOINNIT", STY["sb_h"]),
]
certs = [
    ("● ISTQB® Foundation Level — Certified Tester", "01/2014"),
    ("● ISTQB® Foundation Level — Agile Tester", "04/2015"),
    ("● Advanced Robot Framework", "11/2015"),
    ("● Multimodal Prompting with Google Gemini", "05/2024"),
    ("● AI Show: Prompt Engineering Basics — Azure OpenAI", "05/2024"),
    ("● Puhuja — Testaus ja AI 2024", "2024"),
]
for n, d in certs:
    SIDEBAR_2.append(p(n, STY["sb_cert"]))
    SIDEBAR_2.append(p(d, STY["sb_cert_date"]))

SIDEBAR_2.append(p("PAINOPISTEALUEET", STY["sb_h"]))
focus = [
    ("LLM &amp; NLP", "Structured prompting, RAG-grounding, fine-tuning, hallusinaatioiden vähentäminen, epävarmuuden hallinta."),
    ("AI-agentit", "Multi-agentti-orkestrointi, protokollat, kontrolloitu työkalujen käyttö ja käyttöoikeudet."),
    ("AI-luotettavuus", "Guardrails, prompt injection -torjunta, fallback-strategiat, turvallinen eskalointi."),
    ("Evaluointi &amp; testaus", "LLM-as-judge + sääntötarkistukset, laadun metriikat, regressiotestaus, jatkuva parantaminen."),
]
for h, b in focus:
    SIDEBAR_2.append(p(h, STY["sb_focus_h"]))
    SIDEBAR_2.append(p(b, STY["sb_focus_b"]))

SIDEBAR_2.append(p('"Muutan monimutkaisen tekoälyn luotettavaksi, mitattavaksi liiketoiminta-arvoksi."', STY["sb_quote"]))

MAIN_2 = [
    section_h("VALITUT PROJEKTIT", "AVOIN LÄHDEKOODI & TUOTANTO"),
    project_card("ALMA-memory", "AVOIN LÄHDEKOODI · PYPI · NPM",
                 "Pysyvä muisti AI-agenteille — oppii, muistaa, kehittyy. Vaihtoehto Mem0:lle: rajattu oppiminen, antipatterns, multi-agent-jakaminen ja MCP-integraatio. Yksi muistikerros jokaiselle tekoälylle.",
                 "Python · SQLite · MCP · FastAPI · npm"),
    Spacer(1, 6),
    project_card("AGtestari", "AVOIN LÄHDEKOODI · SAAS",
                 "AI-pohjainen yhtenäinen testausalusta, joka tuo autonomiset QA-agentit asiakkaan Azure-ympäristöön. Yhdistää frontend-, backend-, mobiili-, saavutettavuus- ja suorituskykytestauksen 24/7-AI-agenteilla ja 12-vaiheisella enterprise-työnkululla.",
                 "FastAPI · React · Azure · AI-agentit · Jira"),
    Spacer(1, 6),
    project_card("VERITAS-framework", "AVOIN LÄHDEKOODI",
                 "Evaluointikehys AI-järjestelmille: LLM-as-judge-ominaisuudet, kattavat laatumetriikat ja regressiotestauksen tuki.",
                 "Python · LLM-as-judge · Evaluointi"),
    Spacer(1, 6),
    project_card("Jurevo", "LUOTTAMUKSELLINEN · AI-ARKKITEHTI",
                 "Multi-agentti-orkestrointi kontrolloiduilla työkaluilla ja chat-evaluointikehyksellä (LLM-as-judge + rule checks). Modulaarinen backend ja suorituskykyinen yrityshaku.",
                 "FastAPI · PostgreSQL · Redis · Multi-agent"),
    Spacer(1, 6),
    project_card("Lumanela.fi", "TUOTANTO · 100–500 KESKUSTELUA/KK",
                 "LLM + RAG + fine-tuning. Strukturoitu prompt-logiikka ja edge-funktioilla orkestroitu työnkulku tuotannossa.",
                 "LLM · RAG · Fine-tuning · Edge Functions"),
    Spacer(1, 10),
    section_h("KOULUTUS", "AKATEEMINEN TAUSTA"),
]

edu_items = [
    ("Tietojenkäsittelyn Tradenomi (AMK)", "Jyväskylän ammattikorkeakoulu (JAMK)", "2011 — 2016"),
    ("MBA — International Business and Law", "Åbo Akademi", "2004 — 2006"),
    ("BBA — Management", "Faculdade Cândido Mendes, Brasilia", "1985 — 1990"),
    ("Vierasluennoitsija", "Jyväskylän ammattikorkeakoulu (JAMK)", "2007 — 2016"),
]
# Two-column education grid
edu_cells = []
for i in range(0, len(edu_items), 2):
    left = edu_items[i]
    right = edu_items[i + 1] if i + 1 < len(edu_items) else ("", "", "")
    left_block = [Paragraph(left[0], STY["m_edu_deg"]),
                  Paragraph(left[1], STY["m_edu_inst"]),
                  Paragraph(left[2], STY["m_edu_yr"])]
    right_block = [Paragraph(right[0], STY["m_edu_deg"]) if right[0] else Paragraph("", STY["m_edu_deg"]),
                   Paragraph(right[1], STY["m_edu_inst"]) if right[1] else Paragraph("", STY["m_edu_inst"]),
                   Paragraph(right[2], STY["m_edu_yr"]) if right[2] else Paragraph("", STY["m_edu_yr"])]
    lt = Table([[x] for x in left_block], colWidths=[(MAIN_W - 2 * MARGIN) / 2 - 10])
    rt = Table([[x] for x in right_block], colWidths=[(MAIN_W - 2 * MARGIN) / 2 - 10])
    for tt in (lt, rt):
        tt.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0),
                                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                                ("TOPPADDING", (0, 0), (-1, -1), 1),
                                ("BOTTOMPADDING", (0, 0), (-1, -1), 1)]))
    edu_cells.append([lt, rt])
edu_tbl = Table(edu_cells, colWidths=[(MAIN_W - 2 * MARGIN) / 2, (MAIN_W - 2 * MARGIN) / 2])
edu_tbl.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                             ("LEFTPADDING", (0, 0), (-1, -1), 0),
                             ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                             ("BOTTOMPADDING", (0, 0), (-1, -1), 10)]))
MAIN_2.append(edu_tbl)
MAIN_2.append(Spacer(1, 20))
MAIN_2.append(p("Renata Baldissara-Kunnela — AI-kehittäjä                                                                                     Sivu 2 / 2", STY["m_foot"]))


# ---------- Build ----------
def draw_background(canv, doc):
    canv.saveState()
    canv.setFillColor(SIDEBAR_BG)
    canv.rect(0, 0, SIDEBAR_W, PAGE_H, stroke=0, fill=1)
    canv.setFillColor(MAIN_BG)
    canv.rect(SIDEBAR_W, 0, MAIN_W, PAGE_H, stroke=0, fill=1)
    canv.restoreState()


class CVDoc(BaseDocTemplate):
    def __init__(self, filename, **kw):
        super().__init__(filename, pagesize=A4, **kw)
        sidebar_frame_p1 = Frame(MARGIN, MARGIN, SIDEBAR_W - 2 * MARGIN, PAGE_H - 2 * MARGIN,
                                 id="sb1", showBoundary=0, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        main_frame_p1 = Frame(SIDEBAR_W + MARGIN, MARGIN, MAIN_W - 2 * MARGIN, PAGE_H - 2 * MARGIN,
                              id="mn1", showBoundary=0, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        sidebar_frame_p2 = Frame(MARGIN, MARGIN, SIDEBAR_W - 2 * MARGIN, PAGE_H - 2 * MARGIN,
                                 id="sb2", showBoundary=0, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        main_frame_p2 = Frame(SIDEBAR_W + MARGIN, MARGIN, MAIN_W - 2 * MARGIN, PAGE_H - 2 * MARGIN,
                              id="mn2", showBoundary=0, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([
            PageTemplate(id="P1", frames=[sidebar_frame_p1, main_frame_p1], onPage=draw_background),
            PageTemplate(id="P2", frames=[sidebar_frame_p2, main_frame_p2], onPage=draw_background),
        ])


doc = CVDoc(OUT)
story = []
story += SIDEBAR_1
story.append(FrameBreak())
story += MAIN_1
story.append(FrameBreak())  # move to next page's sidebar
story += SIDEBAR_2
story.append(FrameBreak())
story += MAIN_2
doc.build(story)

print(f"OK -> {OUT}")
