import subprocess
import sys


def main():
    if len(sys.argv) < 3:
        print("Usage: python md_to_pdf.py input.md output.pdf")
        sys.exit(1)

    input_md = sys.argv[1]
    output_pdf = sys.argv[2]

    cmd = [
        "pandoc",
        input_md,
        "--from",
        "markdown",
        "--pdf-engine=xelatex",
        "-V",
        "geometry:margin=1in",
        "-V",
        "fontsize=11pt",
        "-o",
        output_pdf,
    ]

    print("Generating PDF...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)

    if result.returncode != 0:
        print(f"Pandoc failed with exit code {result.returncode}")
        sys.exit(result.returncode)

    print(f"PDF generated: {output_pdf}")


if __name__ == "__main__":
    main()
