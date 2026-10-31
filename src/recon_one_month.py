from pathlib import Path
from lxml import etree

path = Path("data/raw/cart20241.xml")

n_all = 0          # XML에 있는 전체 대출 수
n_open = 0         # 월말 잔액이 0보다 큰 대출 수
total_end = 0.0    # 월말 잔액 합계
total_begin = 0.0  # 월초 잔액 합계
n_delinq = 0         # 월말 연체 대출 수

for _, el in etree.iterparse(str(path), events=("end",)):
    if etree.QName(el).localname == "assets":
        n_all += 1
        for child in el:
            if etree.QName(child).localname == "reportingPeriodActualEndBalanceAmount":
                bal = float(child.text or 0)
                total_end += bal
                if bal > 0:
                    n_open += 1
            if etree.QName(child).localname == "currentDelinquencyStatus":
                status = int(child.text or 0)
                if status > 0:
                    n_delinq += 1
            if etree.QName(child).localname == "reportingPeriodBeginningLoanBalanceAmount":
                bal = float(child.text or 0)
                total_begin += bal
        el.clear()

SERVICER_BAL_BEGIN = 438_720_495.08   # 직전 기간 말 (8월 말)
SERVICER_BAL_END = 416_563_294.35     # 이번 기간 말 (9월 말)
SERVICER_CNT = 33_728

print(f"XML 전체 대출 수:      {n_all:,}")
print(f"XML 잔액>0 대출 수:    {n_open:,}   (서비서 {SERVICER_CNT:,}, 차이 {n_open - SERVICER_CNT:,})")
print(f"월초 잔액: XML {total_begin:,.2f} / 서비서 {SERVICER_BAL_BEGIN:,.2f} / 차이 {total_begin - SERVICER_BAL_BEGIN:,.2f}")
print(f"월말 잔액: XML {total_end:,.2f} / 서비서 {SERVICER_BAL_END:,.2f} / 차이 {total_end - SERVICER_BAL_END:,.2f}")
print(f"연체 중인 대출 수:     {n_delinq:,}")
print(f"연체 비율(건수 기준):  {n_delinq / n_open:.2%}")