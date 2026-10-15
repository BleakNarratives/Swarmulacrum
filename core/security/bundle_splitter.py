"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: bundle_splitter.py
LAST_SYNC: 2026-08-02T01:13:30Z
[/DNA_TAG]
"""
import os
import sys
from pypdf import PdfReader, PdfWriter

def split_legal_bundle(input_pdf_path, chunk_size=10):
    if not os.path.exists(input_pdf_path):
        print(f"[-] Missing source file at: {input_pdf_path}")
        return

    output_dir = "/storage/emulated/0/RootBase/OutClaw/StagedChunks"
    os.makedirs(output_dir, exist_ok=True)

    print(f"[*] Opening master bundle: {input_pdf_path}")
    reader = PdfReader(input_pdf_path)
    total_pages = len(reader)
    print(f"[+] Total pages detected: {total_pages}")

    chunk_count = 0
    for start_page in range(0, total_pages, chunk_size):
        end_page = min(start_page + chunk_size, total_pages)
        writer = PdfWriter()

        for page_num in range(start_page, end_page):
            writer.add_page(reader.pages[page_num])

        chunk_filename = f"bundle_pages_{start_page + 1}_to_{end_page}.pdf"
        chunk_filepath = os.path.join(output_dir, chunk_filename)

        with open(chunk_filepath, "wb") as f:
            writer.write(f)

        chunk_count += 1
        print(f"    -> Exported Chunk {chunk_count}: Pages {start_page + 1}-{end_page}")

    print(f"\n[+] Splitting complete! {chunk_count} segments stored in: {output_dir}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[-] Usage: python bundle_splitter.py <path_to_giant_bundle.pdf>")
    else:
        split_legal_bundle(sys.argv[1])
