"""
HR Dashboard - Mock Data Generator
產生人力資源報表所需的模擬資料
"""
import random
from datetime import datetime, timedelta
from collections import defaultdict

random.seed(42)

# ============================================================
# 基礎設定
# ============================================================
DEPARTMENTS = ["研發部", "銷售部", "行銷部", "財務部", "人資部", "客服部", "製造部", "品管部"]
RANKS = ["實習生", "助理工程師", "工程師", "資深工程師", "主管", "經理", "副總", "總經理"]
EDUCATION = ["高中", "專科", "學士", "碩士", "博士"]
GENDERS = ["男", "女"]
AGE_GROUPS = ["20-25", "26-30", "31-35", "36-40", "41-45", "46-50", "51-55", "56-60", "60+"]
TENURE_GROUPS = ["<1年", "1-3年", "3-5年", "5-10年", "10-15年", "15年以上"]
MONTHS = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
LEAVE_REASONS = ["個人生涯規劃", "薪資不滿意", "工作壓力大", "家庭因素", "公司文化不適應", "升遷受限", "被挖角", "退休", "其他"]

# ============================================================
# 1. 招募漏斗 & 用人需求
# ============================================================

def get_recruitment_funnel():
    """招募漏斗：從投遞履歷到錄取的各階段數據"""
    stages = []
    total = random.randint(1200, 1800)
    labels = ["投遞履歷", "履歷篩選通過", "電話面試", "一面", "二面", "錄取", "報到"]
    rates = [1.0, 0.45, 0.30, 0.20, 0.12, 0.08, 0.065]
    for label, rate in zip(labels, rates):
        count = int(total * rate)
        stages.append({"stage": label, "count": count})
    return stages


def get_recruitment_by_department():
    """各部門招募漏斗統計"""
    result = []
    for dept in DEPARTMENTS:
        applied = random.randint(80, 300)
        screened = int(applied * random.uniform(0.35, 0.55))
        interviewed = int(screened * random.uniform(0.50, 0.75))
        offered = int(interviewed * random.uniform(0.30, 0.50))
        accepted = int(offered * random.uniform(0.60, 0.90))
        result.append({
            "department": dept,
            "applied": applied,
            "screened": screened,
            "interviewed": interviewed,
            "offered": offered,
            "accepted": accepted,
            "acceptance_rate": round(accepted / max(offered, 1) * 100, 1),
        })
    return result


def get_vacancy_status():
    """缺編情況 & 平均錄取天數"""
    result = []
    for dept in DEPARTMENTS:
        headcount_budget = random.randint(20, 80)
        current = headcount_budget - random.randint(0, 12)
        vacancy = headcount_budget - current
        avg_days = random.randint(18, 65)
        result.append({
            "department": dept,
            "budget_headcount": headcount_budget,
            "current_headcount": current,
            "vacancy": vacancy,
            "vacancy_rate": round(vacancy / headcount_budget * 100, 1),
            "avg_days_to_fill": avg_days,
        })
    return result


def get_monthly_recruitment_trend():
    """月度招募趨勢"""
    result = []
    for m in MONTHS:
        result.append({
            "month": m,
            "applications": random.randint(80, 220),
            "interviews": random.randint(30, 90),
            "offers": random.randint(8, 35),
            "hires": random.randint(5, 25),
        })
    return result


# ============================================================
# 2. 人才結構
# ============================================================

def _generate_employees(n=520):
    """產生 n 筆模擬員工資料"""
    employees = []
    for i in range(n):
        dept = random.choice(DEPARTMENTS)
        rank = random.choices(RANKS, weights=[3, 10, 25, 20, 15, 10, 5, 2])[0]
        gender = random.choices(GENDERS, weights=[55, 45])[0]
        age = random.randint(22, 62)
        tenure = round(random.uniform(0.2, 25), 1)
        edu = random.choices(EDUCATION, weights=[5, 8, 40, 35, 12])[0]
        employees.append({
            "id": f"EMP{i+1:04d}",
            "department": dept,
            "rank": rank,
            "gender": gender,
            "age": age,
            "tenure_years": tenure,
            "education": edu,
        })
    return employees


EMPLOYEES = _generate_employees()


def get_headcount_overview():
    """在職人數總覽"""
    return {
        "total": len(EMPLOYEES),
        "by_department": _count_by(EMPLOYEES, "department", DEPARTMENTS),
        "by_rank": _count_by(EMPLOYEES, "rank", RANKS),
        "by_gender": _count_by(EMPLOYEES, "gender", GENDERS),
        "by_education": _count_by(EMPLOYEES, "education", EDUCATION),
        "by_age_group": _count_age_groups(EMPLOYEES),
        "by_tenure_group": _count_tenure_groups(EMPLOYEES),
    }


def _count_by(employees, field, ordered_keys):
    counter = defaultdict(int)
    for e in employees:
        counter[e[field]] += 1
    return [{"label": k, "count": counter.get(k, 0)} for k in ordered_keys]


def _age_bucket(age):
    if age <= 25: return "20-25"
    if age <= 30: return "26-30"
    if age <= 35: return "31-35"
    if age <= 40: return "36-40"
    if age <= 45: return "41-45"
    if age <= 50: return "46-50"
    if age <= 55: return "51-55"
    if age <= 60: return "56-60"
    return "60+"


def _tenure_bucket(yrs):
    if yrs < 1: return "<1年"
    if yrs < 3: return "1-3年"
    if yrs < 5: return "3-5年"
    if yrs < 10: return "5-10年"
    if yrs < 15: return "10-15年"
    return "15年以上"


def _count_age_groups(employees):
    counter = defaultdict(int)
    for e in employees:
        counter[_age_bucket(e["age"])] += 1
    return [{"label": g, "count": counter.get(g, 0)} for g in AGE_GROUPS]


def _count_tenure_groups(employees):
    counter = defaultdict(int)
    for e in employees:
        counter[_tenure_bucket(e["tenure_years"])] += 1
    return [{"label": g, "count": counter.get(g, 0)} for g in TENURE_GROUPS]


# ============================================================
# 3. 人力異動 & 離職率
# ============================================================

def get_monthly_movement():
    """月度人力異動紀錄：期初/期末、新進、離職、調遷"""
    records = []
    hc = 500
    for m in MONTHS:
        new_hires = random.randint(5, 25)
        resignations = random.randint(3, 18)
        transfers_in = random.randint(0, 5)
        transfers_out = random.randint(0, 5)
        end_hc = hc + new_hires - resignations + transfers_in - transfers_out
        records.append({
            "month": m,
            "beginning_hc": hc,
            "new_hires": new_hires,
            "resignations": resignations,
            "transfers_in": transfers_in,
            "transfers_out": transfers_out,
            "ending_hc": end_hc,
            "monthly_turnover_rate": round(resignations / ((hc + end_hc) / 2) * 100, 2),
        })
        hc = end_hc
    return records


def get_turnover_by_department():
    """各部門離職率分析"""
    result = []
    for dept in DEPARTMENTS:
        dept_size = random.randint(30, 80)
        resignations = random.randint(2, 15)
        rate = round(resignations / dept_size * 100, 1)
        # 離職原因分佈
        reasons = {}
        remaining = resignations
        for reason in random.sample(LEAVE_REASONS, min(4, len(LEAVE_REASONS))):
            if remaining <= 0:
                break
            c = random.randint(1, max(1, remaining))
            reasons[reason] = c
            remaining -= c
        result.append({
            "department": dept,
            "headcount": dept_size,
            "resignations": resignations,
            "turnover_rate": rate,
            "reasons": reasons,
        })
    return sorted(result, key=lambda x: x["turnover_rate"], reverse=True)


def get_turnover_by_rank():
    """各職級離職率"""
    result = []
    for rank in RANKS:
        size = random.randint(15, 120)
        resignations = random.randint(1, int(size * 0.25))
        result.append({
            "rank": rank,
            "headcount": size,
            "resignations": resignations,
            "turnover_rate": round(resignations / size * 100, 1),
        })
    return result


def get_turnover_trend():
    """年度離職率趨勢 (近 5 年)"""
    result = []
    for y in range(2022, 2027):
        result.append({
            "year": str(y),
            "annual_turnover_rate": round(random.uniform(8, 18), 1),
            "voluntary_rate": round(random.uniform(5, 12), 1),
            "involuntary_rate": round(random.uniform(1, 5), 1),
        })
    return result


def get_leave_reason_distribution():
    """離職原因分佈"""
    result = []
    total = 0
    for reason in LEAVE_REASONS:
        count = random.randint(3, 30)
        result.append({"reason": reason, "count": count})
        total += count
    for r in result:
        r["percentage"] = round(r["count"] / total * 100, 1)
    return sorted(result, key=lambda x: x["count"], reverse=True)


def get_department_rank_turnover_detail():
    """重點部門 × 職級離職明細 (如：銷售部主管流失)"""
    details = []
    for dept in DEPARTMENTS:
        for rank in RANKS:
            size = random.randint(2, 25)
            left = random.randint(0, min(5, size))
            if left > 0:
                details.append({
                    "department": dept,
                    "rank": rank,
                    "headcount": size,
                    "resignations": left,
                    "turnover_rate": round(left / size * 100, 1),
                })
    # 回傳離職率最高的前 15 筆
    return sorted(details, key=lambda x: x["turnover_rate"], reverse=True)[:15]
