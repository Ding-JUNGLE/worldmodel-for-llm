#!/usr/bin/env bash
set -euo pipefail

export PATH="$HOME/.local/bin:$PATH"

if command -v tectonic >/dev/null 2>&1; then
  tectonic --keep-logs --keep-intermediates main.tex
elif command -v pdflatex >/dev/null 2>&1; then
  pdflatex -interaction=nonstopmode main.tex
  bibtex main || true
  pdflatex -interaction=nonstopmode main.tex
  pdflatex -interaction=nonstopmode main.tex
else
  echo "No LaTeX engine found." >&2
  exit 1
fi

if command -v pdfinfo >/dev/null 2>&1; then
  PAGES=$(pdfinfo main.pdf | awk '/Pages:/ {print $2}')
else
  PAGES="UNKNOWN"
fi

echo "PAGES=$PAGES" > page_count.txt
if [ "$PAGES" != "UNKNOWN" ] && [ "$PAGES" -le 4 ]; then
  echo "STATUS=PASS_PAGE_LIMIT" >> page_count.txt
else
  echo "STATUS=UNKNOWN_OR_FAIL_PAGE_LIMIT" >> page_count.txt
fi
