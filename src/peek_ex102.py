import sys, requests
from pathlib import Path
from lxml import etree

UA = {"User-Agent": "mjungk95@gmail.com"}
url = sys.argv[1]
dest = Path("data/raw") / url.split("/")[-1]

if not dest.exists():
    print("다운로드 중...")
    with requests.get(url, headers=UA, stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(1024 * 1024):
                f.write(chunk)
print(f"파일 크기: {dest.stat().st_size / 1e6:.1f} MB")

# 대출 첫 건만 읽고 멈추기
for _, el in etree.iterparse(str(dest), events=("end",)):
    if etree.QName(el).localname == "assets":
        for child in el:
            print(f"{etree.QName(child).localname:45s} {child.text}")
        break