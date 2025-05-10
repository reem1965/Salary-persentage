import streamlit as st
from datetime import datetime
from config import ADMIN_USERNAME, ADMIN_PASSWORD

# تهيئة حالة الجلسة
def init_session_state():
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

# قراءة بيانات المستخدمين
def load_users():
    return {
        "admin": {
            "username": ADMIN_USERNAME,
            "password": ADMIN_PASSWORD
        },
        "visitors": []
    }

# حفظ بيانات المستخدمين في الذاكرة المؤقتة
visitors_cache = []
def save_users(users_data):
    global visitors_cache
    visitors_cache = users_data.get('visitors', [])

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
            if st.button("إنشاء اسم مستخدم جديد"):
                if username:
                    if not username.isascii():
                        st.error("الرجاء إدخال اسم المستخدم باللغة الإنجليزية فقط")
                    else:
                        users_data = load_users()
                        if username in [visitor["username"] for visitor in users_data["visitors"]]:
                            st.error("اسم المستخدم موجود مسبقاً، الرجاء اختيار اسم آخر")
                        else:
                            users_data["visitors"].append({
                                "username": username,
                                "last_visit": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            })
                            save_users(users_data)
                            st.success("تم إنشاء اسم المستخدم بنجاح! يمكنك الآن تسجيل الدخول.")
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
                    # تحديث وقت آخر زيارة
                    for visitor in users_data["visitors"]:
                        if visitor["username"] == username:
                            visitor["last_visit"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            break
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
                    # إنشاء مستخدم جديد
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
                    st.success("تم إنشاء اسم المستخدم وتسجيل الدخول بنجاح!")
                    st.rerun()
            else:
                st.error("الرجاء إدخال اسم المستخدم") 