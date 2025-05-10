import streamlit as st
import pandas as pd
import json
from datetime import datetime

# البيانات: الشهور والنسب التراكمية
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

# تهيئة حالة الجلسة
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ''
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
if 'active_users' not in st.session_state:
    st.session_state.active_users = set()
if 'remember_admin' not in st.session_state:
    st.session_state.remember_admin = False
if 'saved_admin_username' not in st.session_state:
    st.session_state.saved_admin_username = ''
if 'saved_admin_password' not in st.session_state:
    st.session_state.saved_admin_password = ''
if 'remember_visitor' not in st.session_state:
    st.session_state.remember_visitor = False
if 'saved_visitor_username' not in st.session_state:
    st.session_state.saved_visitor_username = ''

import os
from dotenv import load_dotenv

# تحميل المتغيرات البيئية
load_dotenv()

# قراءة بيانات المستخدمين
def load_users():
    return {
        "admin": {
            "username": os.getenv('ADMIN_USERNAME', 'admin'),
            "password": os.getenv('ADMIN_PASSWORD', 'admin123')
        },
        "visitors": []
    }

# حفظ بيانات المستخدمين في الذاكرة المؤقتة
visitors_cache = []
def save_users(users_data):
    global visitors_cache
    visitors_cache = users_data.get('visitors', [])

# صفحة تسجيل الدخول
def login_page():
    st.title("تسجيل الدخول")
    login_type = st.radio("نوع الدخول:", ["زائر", "مسؤول"])
    
    if login_type == "زائر":
        col1, col2 = st.columns([3, 1])
        with col1:
            st.warning("الرجاء إدخال اسم المستخدم باللغة الإنجليزية فقط")
            username = st.text_input("اسم المستخدم")
        with col2:
            st.write("")
            st.write("")
            if st.button("التحقق من توفر الاسم"):
                if username:
                    if not username.isascii():
                        st.error("الرجاء إدخال اسم المستخدم باللغة الإنجليزية فقط")
                    else:
                        users_data = load_users()
                        if username in [visitor["username"] for visitor in users_data["visitors"]]:
                            st.error("اسم المستخدم موجود مسبقاً، الرجاء اختيار اسم آخر")
                        else:
                            st.success("اسم المستخدم متاح!")
                else:
                    st.error("الرجاء إدخال اسم المستخدم")
    else:
        st.warning("الرجاء إدخال اسم المستخدم باللغة الإنجليزية فقط")
        username = st.text_input("اسم المستخدم")
        
        # التحقق من أن الاسم باللغة الإنجليزية
        if username and not username.isascii():
            st.error("الرجاء إدخال اسم المستخدم باللغة الإنجليزية فقط")
    
    if login_type == "مسؤول":
        # استرجاع بيانات المسؤول المحفوظة
        if st.session_state.remember_admin:
            username = st.text_input("اسم المستخدم", value=st.session_state.saved_admin_username)
            password = st.text_input("كلمة المرور", type="password", value=st.session_state.saved_admin_password)
        else:
            password = st.text_input("كلمة المرور", type="password")
        
        # مربع اختيار لحفظ بيانات الدخول
        remember = st.checkbox("حفظ بيانات الدخول", value=st.session_state.remember_admin)
        
        if st.button("تسجيل الدخول"):
            users_data = load_users()
            if username == users_data["admin"]["username"] and password == users_data["admin"]["password"]:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.is_admin = True
                st.session_state.active_users.add(username)
                
                # حفظ بيانات المسؤول إذا تم اختيار ذلك
                st.session_state.remember_admin = remember
                if remember:
                    st.session_state.saved_admin_username = username
                    st.session_state.saved_admin_password = password
                else:
                    st.session_state.saved_admin_username = ''
                    st.session_state.saved_admin_password = ''
                
                st.success("تم تسجيل الدخول بنجاح كمسؤول!")
                st.rerun()
            else:
                st.error("خطأ في اسم المستخدم أو كلمة المرور")
    else:
        # استرجاع اسم المستخدم المحفوظ للزائر
        if st.session_state.remember_visitor:
            username = st.text_input("اسم المستخدم", value=st.session_state.saved_visitor_username)
        
        # مربع اختيار لحفظ اسم المستخدم للزائر
        remember_visitor = st.checkbox("حفظ اسم المستخدم", value=st.session_state.remember_visitor)
        
        if st.button("دخول كزائر"):
            users_data = load_users()
            if username:
                # التحقق من وجود اسم المستخدم
                if username in [visitor["username"] for visitor in users_data["visitors"]]:
                    st.error("اسم المستخدم موجود مسبقاً، الرجاء اختيار اسم آخر")
                else:
                    users_data["visitors"].append({
                        "username": username,
                        "last_visit": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    save_users(users_data)
                    
                    # حفظ اسم المستخدم للزائر إذا تم اختيار ذلك
                    st.session_state.remember_visitor = remember_visitor
                    if remember_visitor:
                        st.session_state.saved_visitor_username = username
                    else:
                        st.session_state.saved_visitor_username = ''
                    
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.is_admin = False
                    st.session_state.active_users.add(username)
                    st.success("تم تسجيل الدخول بنجاح!")
                    st.rerun()
            else:
                st.error("الرجاء إدخال اسم المستخدم")

# صفحة الإحصائيات للمسؤول
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
    last_month = months[-1]
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
    month_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                  7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    next_month_name = month_names[next_month_num]
    
    # عرض الشهر التالي للمستخدم
    next_month_str = f"{next_month_name}-{str(next_year)[2:]}"
    st.text(f"الشهر التالي: {next_month_str}")
    
    # إدخال النسبة المئوية للشهر الجديد
    new_percentage = st.number_input("أدخل النسبة المئوية للشهر الجديد:", min_value=0.0, step=0.01)
    
    if st.button("إضافة الشهر"):
        if new_percentage > 0:
            # إضافة الشهر والنسبة الجديدة إلى القوائم
            months.append(next_month_str)
            cumulative_percentages.append(new_percentage)
            st.success(f"تم إضافة شهر {next_month_str} بنسبة {new_percentage}%")
            st.rerun()
        else:
            st.error("الرجاء إدخال نسبة مئوية صحيحة أكبر من 0")

# التطبيق الرئيسي
if not st.session_state.logged_in:
    login_page()
else:
    # زر تسجيل الخروج
    col1, col2 = st.columns([6,1])
    with col2:
        if st.button("تسجيل الخروج"):
            username = st.session_state.username
            st.session_state.active_users.remove(username)
            st.session_state.logged_in = False
            st.session_state.username = ''
            st.session_state.is_admin = False
            st.rerun()
    
    with col1:
        st.write(f"مرحباً {st.session_state.username}!")
    
    if st.session_state.is_admin:
        admin_stats()
        st.markdown("---")
    
    st.title("حاسبة المستحقات حسب راتب كل سنة (بالشيكل)")

    # عرض النتائج

    # إعداد الداتا فريم
    df = pd.DataFrame({
        "الشهر": months,
        "النسبة_التراكمية": cumulative_percentages
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