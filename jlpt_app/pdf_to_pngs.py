#!/usr/bin/env python3
"""Convert each page of a PDF to individual PNG images for reliable OCR."""

import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Install PyMuPDF first: pip install PyMuPDF")
    sys.exit(1)


def pdf_to_pngs(pdf_path: str, output_dir: str | None = None, dpi: int = 300,
                start_page: int = 0, end_page: int | None = None) -> list[Path]:
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        print(f"ERROR: {pdf_path} not found")
        sys.exit(1)

    out = Path(output_dir) if output_dir else pdf_path.parent / f"{pdf_path.stem}_pages"
    out.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    total = len(doc)
    end = end_page if end_page is not None else total
    pages = list(range(max(0, start_page), min(end, total)))
    zoom = dpi / 72  # fitz renders at 72dpi base

    print(f"Converting {len(pages)}/{total} pages @ {dpi}dpi → {out}/")

    results = []
    for i, page_num in enumerate(pages, 1):
        page = doc[page_num]
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
        filename = out / f"page_{page_num+1:04d}.png"
        pix.save(str(filename))
        results.append(filename)
        if i % 50 == 0 or i == 1 or i == len(pages):
            print(f"  [{i}/{len(pages)}] page {page_num+1} → {pix.width}x{pix.height}px")

    doc.close()
    print(f"\nDone — {len(results)} PNGs saved to {out}")
    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert PDF pages to PNG images")
    parser.add_argument("pdf", help="Path to the PDF file")
    parser.add_argument("-o", "--output-dir", help="Output directory (default: <pdf_name>_pages/)")
    parser.add_argument("--dpi", type=int, default=300, help="Render DPI (default: 300)")
    parser.add_argument("--start", type=int, default=0, help="Start page (0-based, default: 0)")
    parser.add_argument("--end", type=int, help="End page (exclusive, default: all pages)")
    args = parser.parse_args()

    pdf_to_pngs(args.pdf, args.output_dir, dpi=args.dpi,
                start_page=args.start, end_page=args.end)
