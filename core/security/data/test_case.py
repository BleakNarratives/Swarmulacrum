"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: test_case.py
LAST_SYNC: 2026-08-02T01:13:31Z
[/DNA_TAG]
"""
from pypdf import PdfWriter
writer = PdfWriter()
writer.add_blank_page(width=72, height=72)
with open("/storage/emulated/0/RootBase/OutClaw/data/test_case.pdf", "wb") as f:
    writer.write(f)
