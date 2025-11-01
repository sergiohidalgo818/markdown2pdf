import os
import subprocess
import argparse
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="markdown2pdf",
        description="Convert a Markdown file to a PDF using Pandoc.",
    )
    parser.add_argument(
        "input_md", help="Path to the input Markdown file (e.g., README.md)", type=Path
    )
    parser.add_argument(
        "output_pdf", help="Path to the output PDF file (e.g., output.pdf)", type=Path
    )
    parser.add_argument(
        "--margin", default="1in", help="Set page margin (default: 1in)"
    )
    parser.add_argument(
        "--fontsize", default="11pt", help="Set base font size (default: 11pt)"
    )
    parser.add_argument(
        "--engine", default="xelatex", help="Specify PDF engine (default: xelatex)"
    )

    return parser.parse_args()


def run(input_md: Path, output_pdf: Path):
    tmp_file = str(input_md) + ".tmp"

    input_md = input_md.resolve()
    output_pdf = output_pdf.resolve()
    css_file_path = os.getcwd() + "/pdf.css"
    cmd = [
        "pandoc",
        input_md,
        "--from=gfm+raw_html+tex_math_dollars",
        "--pdf-engine=weasyprint",
        f"--metadata=base_url=file://{input_md.parent.resolve()}/",
        f"--css={css_file_path}",
        "-V",
        "geometry:margin=1in",
        "-V",
        "fontsize=11pt",
        "-o",
        output_pdf,
    ]
    print("Generating PDF...")
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=input_md.parent)
    if os.path.exists(tmp_file):
        os.remove(tmp_file)

    if result.stdout != "":
        print(result.stdout)

    if result.stderr != "":
        print(result.stderr)

    if result.returncode != 0:
        print(f"Pandoc failed with exit code {result.returncode}")
        sys.exit(result.returncode)

    print(f"PDF generated: {output_pdf}")


def main():
    parsed_args = parse_args()
    run(parsed_args.input_md, parsed_args.output_pdf)


if __name__ == "__main__":
    main()
