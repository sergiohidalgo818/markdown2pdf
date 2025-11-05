from pyppeteer import launch

import os
import sys
import asyncio
import argparse
import subprocess
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
        "-o",
        "--output",
        help="Path to the output PDF file (e.g., output.pdf)",
        type=Path,
        default=Path(os.getcwd()) / "output.pdf",
    )

    return parser.parse_args()


async def html_to_pdf(input_html, output_pdf):
    browser = await launch(headless=True, args=["--no-sandbox"])
    page = await browser.newPage()

    await page.goto(f"file://{input_html}", {"waitUntil": "networkidle0"})

    try:
        await page.evaluate("MathJax.typesetPromise && MathJax.typesetPromise()")
    except Exception:
        pass

    await page.pdf({"path": output_pdf, "format": "A4", "printBackground": True})

    await browser.close()


def run(input_md: Path, output_pdf: Path):
    input_md = input_md.resolve()
    output_pdf = output_pdf.resolve()
    css_file_path = Path(os.getcwd()) / "style.css"
    tmp_file_path = Path(input_md.parent) / input_md.with_suffix(".tmp.html")
    cmd = [
        "pandoc",
        input_md,
        "--from=gfm+tex_math_dollars+raw_tex",
        "--to=html5",
        "--standalone",
        "--katex=https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/",
        f"--metadata=base_url=file://{input_md.parent.resolve()}/",
        f"--resource-path={input_md.parent.resolve()}",
        f"--css={css_file_path}",
        "-V",
        "geometry:margin=1in",
        "-V",
        "fontsize=11pt",
        "-o",
        tmp_file_path,
    ]

    print("Generating PDF...")
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=input_md.parent)
    asyncio.get_event_loop().run_until_complete(
        html_to_pdf(
            tmp_file_path.resolve(),
            output_pdf,
        )
    )

    if os.path.exists(tmp_file_path):
        os.remove(tmp_file_path)

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
    run(parsed_args.input_md, parsed_args.output)


if __name__ == "__main__":
    main()
