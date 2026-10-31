import requests, pandas, duckdb, lxml

UA = {"User-Agent": "mjungk95@gmail.com"}
r = requests.get("https://data.sec.gov/submissions/CIK0002003263.json", headers=UA, timeout=30)
r.raise_for_status()
d = r.json()

forms = d["filings"]["recent"]["form"]
print("트러스트:", d["name"])
print("ABS-EE 공시 수:", forms.count("ABS-EE"))
print("10-D 공시 수:", forms.count("10-D"))
print("환경 OK")