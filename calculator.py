import streamlit as st
import pandas as pd
from config import MONTHS, CUMULATIVE_PERCENTAGES

def calculate_benefits():
    st.title("حاسبة المستحقات حسب راتب كل سنة (بالشيكل)")

    # إعداد الداتا فريم
    df = pd.DataFrame({
        "الشهر": MONTHS,
        "النسبة_التراكمية": CUMULATIVE_PERCENTAGES
    })
    df["النسبة_الشهرية"] = df["النسبة_التراكمية"].diff().fillna(df["النسبة_التراكمية"])

    # تحديد السنة لكل شهر
    df["السنة"] = df["الشهر"].str[-2:].apply(lambda x: int("20" + x) if x != "21" else 2021)

    # إدخال الرواتب لكل سنة
    st.subheader("أدخل الراتب لكل سنة:")
    salaries = {}
    for year in sorted(df["السنة"].unique()):
        salaries[year] = st.number_input(f"الراتب في سنة {year} (شيكل):", min_value=0.0, step=100.0, value=None)

    # حساب المستحقات حسب الراتب لكل سنة
    df["الراتب_السنة"] = df["السنة"].map(salaries)
    df["المستحق_هذا_الشهر"] = df["النسبة_الشهرية"] / 100 * df["الراتب_السنة"]

    # حساب المجموع لكل سنة
    summary = df.groupby("السنة")["المستحق_هذا_الشهر"].sum().reset_index()
    summary.columns = ["السنة", "مجموع_المستحقات"]

    # عرض النتائج
    st.subheader("تفاصيل المستحقات الشهرية:")
    st.dataframe(df[["الشهر", "السنة", "النسبة_الشهرية", "الراتب_السنة", "المستحق_هذا_الشهر"]])

    st.subheader("مجموع المستحقات لكل سنة:")
    st.dataframe(summary)

    total = summary["مجموع_المستحقات"].sum()
    st.success(f"المجموع الكلي لجميع المستحقات: {total:,.2f} شيكل") 