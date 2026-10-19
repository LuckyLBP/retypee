"""Command line automation for the PDF text editor.

Replace text in one file:
    python cli.py replace offer.pdf -r "2026-104=2026-219" -r "Borås=Göteborg"

Replace text in every PDF in a folder, using a JSON file of replacements:
    python cli.py batch ./in ./out --map replacements.json

List the editable text runs in a PDF (handy for writing replacement maps):
    python cli.py inspect offer.pdf
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from pdfedit.core import EditorDocument, replace_text


def parse_pairs(items: list[str]) -> list[tuple[str, str]]:
    pairs = []
    for item in items or []:
        if "=" not in item:
            sys.exit(f'Replacement "{item}" needs the form old=new')
        old, new = item.split("=", 1)
        pairs.append((old, new))
    return pairs


def load_map(path: str | None) -> list[tuple[str, str]]:
    if not path:
        return []
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return list(data.items()) if isinstance(data, dict) else [tuple(p) for p in data]


def process(src: Path, dst: Path, pairs, args) -> dict[str, int]:
    ed = EditorDocument(src.read_bytes(), src.name)
    counts = {}
    for old, new in pairs:
        n, _ = replace_text(ed.doc, old, new, ed.resolver, case_sensitive=args.case_sensitive,
                            whole_word=args.whole_word, fit=args.fit)
        counts[old] = n
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(ed.export(strip_metadata=not args.keep_metadata))
    ed.doc.close()
    return counts


def report(name: str, counts: dict[str, int]) -> None:
    detail = ", ".join(f'"{k}": {v}' for k, v in counts.items())
    print(f"{name}: {sum(counts.values())} replacements ({detail})")


def main() -> None:
    ap = argparse.ArgumentParser(description="Edit text in PDFs from the command line.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p):
        p.add_argument("-r", "--replace", action="append", metavar="OLD=NEW",
                       help="text to replace, can be repeated")
        p.add_argument("-m", "--map", help='JSON file: {"old": "new", ...}')
        p.add_argument("--case-sensitive", action="store_true")
        p.add_argument("--whole-word", action="store_true")
        p.add_argument("--fit", action="store_true",
                       help="squeeze replacement text that is wider than the original")
        p.add_argument("--keep-metadata", action="store_true",
                       help="keep author, creator app, dates and other metadata (removed by default)")

    p1 = sub.add_parser("replace", help="replace text in one PDF")
    p1.add_argument("input")
    p1.add_argument("-o", "--output", help="default: <input>-edited.pdf")
    common(p1)

    p2 = sub.add_parser("batch", help="replace text in every PDF in a folder")
    p2.add_argument("input_dir")
    p2.add_argument("output_dir")
    common(p2)

    p3 = sub.add_parser("inspect", help="list editable text runs")
    p3.add_argument("input")

    args = ap.parse_args()

    if args.cmd == "inspect":
        ed = EditorDocument(Path(args.input).read_bytes(), args.input)
        for pno in range(ed.doc.page_count):
            for u in ed.units(pno):
                print(f"p{pno + 1}  {u.font:<28} {u.size:5.1f}pt  {u.text}")
        return

    pairs = parse_pairs(args.replace) + load_map(args.map)
    if not pairs:
        sys.exit("Give at least one replacement with -r old=new or --map file.json")

    if args.cmd == "replace":
        src = Path(args.input)
        dst = Path(args.output) if args.output else src.with_name(f"{src.stem}-edited.pdf")
        report(dst.name, process(src, dst, pairs, args))
    else:
        src_dir, dst_dir = Path(args.input_dir), Path(args.output_dir)
        files = sorted(p for p in src_dir.iterdir() if p.suffix.lower() == ".pdf")
        if not files:
            sys.exit(f"No PDF files in {src_dir}")
        for src in files:
            try:
                report(src.name, process(src, dst_dir / src.name, pairs, args))
            except Exception as exc:
                print(f"{src.name}: FAILED ({exc})")


if __name__ == "__main__":
    main()
