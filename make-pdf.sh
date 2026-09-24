#!/bin/zsh
# Builds index.html from build.py, then prints it to PDF with Brave (headless Chrome).
cd "${0:A:h}"
python3 build.py
"/Applications/Brave Browser.app/Contents/MacOS/Brave Browser" \
  --headless=new --disable-gpu --no-pdf-header-footer --run-all-compositor-stages-before-draw \
  --virtual-time-budget=15000 \
  --print-to-pdf="$PWD/10-hooks-i-actually-posted.pdf" \
  "file://$PWD/index.html" 2>/dev/null
ls -lh 10-hooks-i-actually-posted.pdf
