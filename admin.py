import streamlit as st
import pandas as pd
from datetime import datetime
from config import MONTHS, CUMULATIVE_PERCENTAGES, MONTH_NAMES
from auth import load_users

def admin_stats():
    st.title("إحصائيات المستخدمين")
    users_data = load_users()
    visitors = users_data["visitors"]
    
    # عرض عدد المستخدمين النشطين
    active_users_count = len(st.session_state.active_users)
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("إجمالي عدد المستخدمين المسجلين:")
        st.info(f"عدد المستخدمين: {len(visitors)}")
    
    with col2:
        st.subheader("المستخدمين النشطين حالياً:")
        st.info(f"عدد المستخدمين النشطين: {active_users_count}")

    st.subheader("إجمالي عدد الزوار:")
    st.info(f"عدد الزوار: {len(visitors)}")
    
    st.subheader("قائمة الزوار:")
    if visitors:
        df_visitors = pd.DataFrame(visitors)
        st.dataframe(df_visitors)
    else:
        st.write("لا يوجد زوار حتى الآن")

    # إضافة نموذج لإدخال شهر جديد
    st.markdown("---")
    st.subheader("إضافة شهر جديد")
    
    # الحصول على آخر شهر وسنة
    last_month = MONTHS[-1]
    last_month_num = int(last_month.split('-')[0].replace('Jan', '1').replace('Feb', '2')
                        .replace('Mar', '3').replace('Apr', '4').replace('May', '5')
                        .replace('Jun', '6').replace('Jul', '7').replace('Aug', '8')
                        .replace('Sep', '9').replace('Oct', '10').replace('Nov', '11')
                        .replace('Dec', '12'))
    last_year = int('20' + last_month.split('-')[1])
    
    # حساب الشهر والسنة التاليين
    next_month_num = last_month_num + 1 if last_month_num < 12 else 1
    next_year = last_year if next_month_num > last_month_num else last_year + 1
    
    # تحويل رقم الشهر إلى اسم
    next_month_name = MONTH_NAMES[next_month_num]
    
    # عرض الشهر التالي للمستخدم
    next_month_str = f"{next_month_name}-{str(next_year)[2:]}"
    st.text(f"الشهر التالي: {next_month_str}")
    
    # إدخال النسبة المئوية للشهر الجديد
    new_percentage = st.number_input("أدخل النسبة المئوية للشهر الجديد:", min_value=0.0, step=0.01)
    
    if st.button("إضافة الشهر"):
        if new_percentage > 0:
            # إضافة الشهر والنسبة الجديدة إلى القوائم
            MONTHS.append(next_month_str)
            CUMULATIVE_PERCENTAGES.append(new_percentage)
            st.success(f"تم إضافة شهر {next_month_str} بنسبة {new_percentage}%")
            st.rerun()
        else:
            st.error("الرجاء إدخال نسبة مئوية صحيحة أكبر من 0") 