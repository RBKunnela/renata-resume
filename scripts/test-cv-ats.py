"""
ATS-readability test for the rendered CV PDFs.

Simulates what an ATS / AI screener sees when parsing the PDF:
  1. Extracts text using two independent methods (pdftotext and pypdf)
  2. Checks structural requirements: name placement, section headers, contact info
  3. Detects common ATS-breaking issues: broken letter-spacing, missing sections, lost keywords

Run from project root:
    python scripts/test-cv-ats.py
"""
from __future__ import annotations
import subprocess
import sys
import re
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    print("ERROR: pypdf not installed. Run: pip install pypdf")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent

CVS = [
    {
        "name": "EN",
        "pdf": ROOT / "docs" / "cv-en-pdf" / "Renata-Baldissara-Kunnela-CV-EN.pdf",
        "expected_sections": [
            "SUMMARY", "STRENGTHS", "KEY ACHIEVEMENTS", "EXPERIENCE",
            "SKILLS", "FOCUS AREAS", "FEATURED PROJECTS",
            "EDUCATION", "CERTIFICATIONS", "LANGUAGES",
        ],
        "expected_keywords": [
            "Python", "FastAPI", "Pydantic", "PostgreSQL", "Redis",
            "OpenAI", "Anthropic Claude", "Azure OpenAI", "LangChain", "LlamaIndex",
            "RAG", "Fine-tuning", "Guardrails", "LLM-as-judge", "Prompt Engineering",
            "Robot Framework", "Postman", "TestRail", "Jira", "ISTQB",
            "FriendlyAI", "TietoEvry", "Fennia", "Samlink",
            "ALMA-memory", "AGtestari", "VERITAS",
            "Testaus ja AI", "Viitasaari, Finland",
        ],
        "expected_dates": ["02/2025", "09/2023", "01/2016", "03/2023", "02/2025"],
    },
    {
        "name": "FI",
        "pdf": ROOT / "docs" / "cv-fi-pdf" / "Renata-Baldissara-Kunnela-CV-FI.pdf",
        "expected_sections": [
            "PROFIILI", "VAHVUUDET", "TÄRKEIMMÄT SAAVUTUKSET", "TYÖKOKEMUS",
            "TAIDOT", "PAINOPISTEALUEET", "VALITUT PROJEKTIT",
            "KOULUTUS", "SERTIFIOINNIT", "KIELET",
        ],
        "expected_keywords": [
            "Python", "FastAPI", "PostgreSQL", "OpenAI", "Anthropic Claude",
            "LangChain", "LlamaIndex", "RAG", "Fine-tuning", "Guardrails", "LLM-as-judge",
            "Robot Framework", "Postman", "TestRail", "Jira", "ISTQB",
            "FriendlyAI", "TietoEvry", "Fennia", "Samlink",
            "ALMA-memory", "AGtestari", "VERITAS",
            "Pankkijärjestelmät", "Vakuutusjärjestelmät",
            "Testaus ja AI", "Viitasaari, Suomi",
        ],
        "expected_dates": ["02/2025", "09/2023", "01/2016", "03/2023"],
    },
]

# Universal contact fields (same in both languages)
EXPECTED_CONTACT = [
    "renatbk.linkedin@gmail.com",
    "+358 40 182 9008",
    "linkedin.com/in/renata-kunnela",
    "github.com/RBKunnela",
    "renata-resume.vercel.app",
]


def extract_pdftotext(pdf: Path) -> str:
    """Extract text using pdftotext (poppler) — the most ATS-equivalent."""
    result = subprocess.run(
        ["pdftotext", "-enc", "UTF-8", "-layout", str(pdf), "-"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    return result.stdout


def extract_pdftotext_stream(pdf: Path) -> str:
    """Extract text in stream order (no layout) — what naive ATS parsers see."""
    result = subprocess.run(
        ["pdftotext", "-enc", "UTF-8", str(pdf), "-"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    return result.stdout


def extract_pypdf(pdf: Path) -> str:
    """Extract text using pypdf — alternative ATS-equivalent parser."""
    reader = PdfReader(str(pdf))
    return "\n".join(page.extract_text() for page in reader.pages)


def detect_broken_letter_spacing(text: str) -> list[str]:
    """Detect words broken by letter-spacing — pattern: single letter followed by space then letters."""
    suspicious = []
    # Pattern: word boundary, single uppercase letter, space, then more uppercase letters
    # Example: "S UMMARY" or "EXPERI ENCE"
    for match in re.finditer(r"\b([A-Z])\s+([A-Z]{2,})\b", text):
        prefix = match.group(1)
        suffix = match.group(2)
        word = prefix + suffix
        # Filter out legitimate cases like "I AM" or initials
        if word in ("IM", "IS", "AT", "IN", "ON", "TO", "OR", "BE", "WE", "OF", "BY", "DO", "GO", "NO", "SO", "UP"):
            continue
        if len(word) >= 5:  # only flag substantial broken words
            suspicious.append(match.group(0))
    return suspicious


def find_name_position(text: str) -> tuple[bool, int]:
    """Check if name appears in the first 200 characters (top of extraction stream)."""
    head = text[:200]
    if "Renata Baldissara-Kunnela" in head:
        return True, head.find("Renata Baldissara-Kunnela")
    # Fallback: search whole document
    if "Renata Baldissara-Kunnela" in text:
        return False, text.find("Renata Baldissara-Kunnela")
    return False, -1


def check_section_order(text: str, sections: list[str]) -> tuple[bool, list[str]]:
    """Check that section headers appear in the expected order in the extraction."""
    positions = []
    for section in sections:
        idx = text.find(section)
        positions.append((section, idx))
    found = [(s, p) for s, p in positions if p >= 0]
    if len(found) != len(sections):
        missing = [s for s, p in positions if p < 0]
        return False, missing
    # Check monotonic order
    sorted_by_pos = sorted(found, key=lambda x: x[1])
    if [s for s, _ in sorted_by_pos] == [s for s, _ in found]:
        return True, []
    out_of_order = []
    for i in range(len(found) - 1):
        if found[i][1] > found[i + 1][1]:
            out_of_order.append(f"'{found[i][0]}' appears after '{found[i+1][0]}'")
    return False, out_of_order


def run_tests_for_cv(cv: dict) -> dict:
    pdf = cv["pdf"]
    results = {"name": cv["name"], "tests": []}

    if not pdf.exists():
        results["tests"].append(("PDF exists", False, f"Not found: {pdf}"))
        return results
    results["tests"].append(("PDF exists", True, f"{pdf.stat().st_size:,} bytes"))

    # Extract with all three methods
    text_layout = extract_pdftotext(pdf)
    text_stream = extract_pdftotext_stream(pdf)
    text_pypdf = extract_pypdf(pdf)

    # Test 1: Name appears at top of extraction (pdftotext stream — what naive ATS sees)
    at_top, pos = find_name_position(text_stream)
    if at_top:
        results["tests"].append(("Name appears in top 200 chars (pdftotext stream)", True, f"at char {pos}"))
    elif pos >= 0:
        results["tests"].append((
            "Name appears in top 200 chars (pdftotext stream)",
            False,
            f"found at char {pos} — too far down for some ATS heuristics",
        ))
    else:
        results["tests"].append(("Name appears in extraction (pdftotext stream)", False, "MISSING"))

    # Test 2: Name appears at top in pypdf extraction too
    at_top_pypdf, pos_pypdf = find_name_position(text_pypdf)
    results["tests"].append((
        "Name appears in top 200 chars (pypdf)",
        at_top_pypdf,
        f"at char {pos_pypdf}" if pos_pypdf >= 0 else "MISSING",
    ))

    # Test 3: All expected section headers present and in order (pdftotext stream)
    order_ok, issues = check_section_order(text_stream, cv["expected_sections"])
    if order_ok:
        results["tests"].append((
            f"All {len(cv['expected_sections'])} section headers in correct order",
            True,
            ", ".join(cv["expected_sections"][:4]) + "...",
        ))
    else:
        results["tests"].append((
            f"All {len(cv['expected_sections'])} section headers in correct order",
            False,
            "; ".join(issues),
        ))

    # Test 4: No broken letter-spacing artifacts
    broken = detect_broken_letter_spacing(text_stream)
    if broken:
        results["tests"].append((
            "No broken letter-spacing in section headers",
            False,
            f"found: {broken[:5]}",
        ))
    else:
        results["tests"].append(("No broken letter-spacing in section headers", True, "clean"))

    # Test 5: All contact fields present
    missing_contact = [c for c in EXPECTED_CONTACT if c not in text_stream]
    if missing_contact:
        results["tests"].append((
            f"All {len(EXPECTED_CONTACT)} contact fields present",
            False,
            f"missing: {missing_contact}",
        ))
    else:
        results["tests"].append((
            f"All {len(EXPECTED_CONTACT)} contact fields present",
            True,
            "email, phone, linkedin, github, portfolio",
        ))

    # Test 6: All expected keywords present
    missing_kw = [k for k in cv["expected_keywords"] if k not in text_stream]
    if missing_kw:
        results["tests"].append((
            f"All {len(cv['expected_keywords'])} keywords present",
            False,
            f"missing: {missing_kw}",
        ))
    else:
        results["tests"].append((
            f"All {len(cv['expected_keywords'])} keywords present",
            True,
            f"all found",
        ))

    # Test 7: All expected dates present
    missing_dates = [d for d in cv["expected_dates"] if d not in text_stream]
    if missing_dates:
        results["tests"].append((
            f"All employment dates present",
            False,
            f"missing: {missing_dates}",
        ))
    else:
        results["tests"].append((f"All employment dates present", True, "all found"))

    # Test 8: Two-page document (1 or 2 pages OK, more is bloat)
    reader = PdfReader(str(pdf))
    pages = len(reader.pages)
    if pages <= 2:
        results["tests"].append((f"Page count <= 2", True, f"{pages} pages"))
    else:
        results["tests"].append((f"Page count <= 2", False, f"{pages} pages — too long"))

    # Test 9: Extraction methods agree on content (sanity check)
    # Both extractions should find roughly similar amount of content
    layout_len = len(text_layout)
    pypdf_len = len(text_pypdf)
    ratio = min(layout_len, pypdf_len) / max(layout_len, pypdf_len, 1)
    if ratio > 0.7:
        results["tests"].append((
            "pdftotext and pypdf extract similar content",
            True,
            f"{layout_len} vs {pypdf_len} chars (ratio {ratio:.2f})",
        ))
    else:
        results["tests"].append((
            "pdftotext and pypdf extract similar content",
            False,
            f"{layout_len} vs {pypdf_len} chars (ratio {ratio:.2f}) — one parser may be struggling",
        ))

    return results


def main():
    print("=" * 78)
    print("CV PDF — ATS Readability Test Suite")
    print("=" * 78)

    total_pass = 0
    total_fail = 0

    for cv in CVS:
        print(f"\n--- {cv['name']} CV ({cv['pdf'].name}) ---")
        results = run_tests_for_cv(cv)
        for name, passed, detail in results["tests"]:
            mark = "PASS" if passed else "FAIL"
            print(f"  [{mark}] {name}")
            if detail:
                print(f"         {detail}")
            if passed:
                total_pass += 1
            else:
                total_fail += 1

    print()
    print("=" * 78)
    print(f"RESULT: {total_pass} passed, {total_fail} failed")
    print("=" * 78)
    return 0 if total_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
