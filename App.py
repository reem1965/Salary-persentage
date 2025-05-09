import streamlit as st
import json
import os
import pandas as pd

# --- عداد الزوار المحلي ---
COUNTER_FILE = "counter.json"

if not os.path.exists(COUNTER_FILE):
    with open(COUNTER_FILE, "w") as f:
        json.dump({"count": 0}, f)

def increment_counter():
    with open(COUNTER_FILE, "r") as f:
        data = json.load(f)
    data["count"] += 1
    with open(COUNTER_FILE, "w") as f:
        json.dump(data, f)
    return data["count"]

# عرض عداد الزوار
count = increment_counter()
st.markdown(f"<div style='padding: 10px; background-color: #f0f0f0; border-radius: 5px;'><strong>عدد زوار الصفحة:</strong> **{count}**</div>", unsafe_allow_html=True)

# --- بيانات المستحقات ---
months = [
    "Nov-21", "Dec-21",
    "Jan-22", "Feb-22", "Mar-22", "Apr-22", "May-22", "Jun-22", "Jul-22", "Aug-22", "Sep-22", "Oct-22", "Nov-22", "Dec-22",
    "Jan-23", "Feb-23", "Mar-23", "Apr-23", "May-23", "Jun-23", "Jul-23", "Aug-23", "Sep-23", "Oct-23", "Nov-23", "Dec-23",
    "Jan-24", "Feb-24", "Mar-24", "Apr-24", "May-24", "Jun-24", "Jul-24", "Aug-24", "Sep-24", "Oct-24", "Nov-24", "Dec-24",
    "Jan-25", "Feb-25", "Mar-25", "Apr-25"
]

cumulative_percentages = [
    25.00, 45.00,
    65.00, 71.40, 91.40, 89.12, 103.66, 103.88, 111.49, 115.71, 122.14, 133.61, 145.93, 157.63,
    172.63, 183.00, 183.00, 203.00, 218.00, 233.00, 248.00, 258.00, 268.00, 318.00, 303.58, 343.58,
    378.58, 408.58, 458.58, 508.58, 548.58, 578.58, 608.58, 638.58, 668.58, 698.58, 728.58, 758.58,
    788.58, 818.58, 848.58, 948.58
]

df = pd.DataFrame({
    "month": months,
    "cumulative_percentage": cumulative_percentages
})
df["monthly_percentage"] = df["cumulative_percentage"].diff().fillna(df["cumulative_percentage"])
df["year"] = df["month"].str[-2:].apply(lambda x: int("20" + x) if x != "21" else 2021)

st.title("حساب المستحقات حسب الراتب السنوي")

years = sorted(df["year"].unique())
salaries = {}

# إدخال الراتب لكل سنة
for year in years:
    with st.container():
        salaries[year] = st.number_input(f"أدخل الراتب لسنة {year}", min_value=0, step=100, value=4500 if year != 2021 else 4450)

df["salary"] = df["year"].map(salaries)
df["monthly_amount"] = df["monthly_percentage"] / 100 * df["salary"]

summary = df.groupby("year")["monthly_amount"].sum().round().astype(int).reset_index()
total = summary["monthly_amount"].sum()

st.subheader("المستحقات حسب كل سنة")
for _, row in summary.iterrows():
    st.markdown(f"<div style='padding: 10px; background-color: #e1e1e1; border-radius: 5px;'>سنة {row['year']}: {row['monthly_amount']:,} شيكل</div>", unsafe_allow_html=True)

st.markdown("---")
st.subheader(f"المجموع الكلي للمستحقات: {total:,} شيكل")
st.markdown(f"<div style='padding: 15px; background-color: #c1e1c1; border-radius: 10px;'><strong>المجموع الكلي للمستحقات: {total:,} شيكل</strong></div>", unsafe_allow_html=True)