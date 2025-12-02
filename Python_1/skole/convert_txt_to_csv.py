from pathlib import Path
import csv

SRC_DIR = Path(__file__).resolve().parent / 'convertcsv'
OUT_DIR = Path(__file__).resolve().parent

FILES = [
    ('file-01.txt', 'microbit_day1.csv'),
    ('file-02.txt', 'microbit_day2.csv'),
]

HEADERS = ['Time (seconds)', 'temp']

def detect_split(line: str):
    for sep in [',', '\t', ' ']:
        if sep in line:
            parts = [p for p in line.strip().split(sep) if p != '']
            if len(parts) == 2:
                return sep
    return None

def convert_one(src: Path, dest: Path):
    if not src.exists():
        raise FileNotFoundError(f"Missing input: {src}")
    with src.open('r', encoding='utf-8') as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    if not lines:
        raise ValueError(f"No data in {src}")
    # If first line is headers, skip it
    first = lines[0]
    sep = detect_split(first)
    if sep is None:
        raise ValueError(f"Cannot detect delimiter in line: '{first}'")
    def looks_like_header(s: str):
        s_lower = s.lower()
        return ('time' in s_lower and 'temp' in s_lower) or (',' in s_lower and s_lower.count(',')==1 and not any(ch.isdigit() for ch in s_lower))
    if looks_like_header(first):
        data_lines = lines[1:]
    else:
        data_lines = lines
    rows = []
    for ln in data_lines:
        parts = [p for p in ln.split(sep) if p != '']
        if len(parts) != 2:
            continue
        try:
            t = float(parts[0])
            temp = float(parts[1])
        except ValueError:
            # skip malformed
            continue
        rows.append((t, int(temp)))
    if not rows:
        raise ValueError(f"No valid rows parsed from {src}")
    with dest.open('w', newline='', encoding='utf-8') as out:
        w = csv.writer(out)
        w.writerow(HEADERS)
        for r in rows:
            w.writerow(r)
    print(f"Wrote {len(rows)} rows to {dest.name}")

def main():
    for src_name, dest_name in FILES:
        convert_one(SRC_DIR / src_name, OUT_DIR / dest_name)

if __name__ == '__main__':
    main()