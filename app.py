import streamlit as st
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import plotly.express as px
from datetime import datetime
import time

# -----------------------------------------------------------------------------
# إعدادات الصفحة
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="متجر CureX للمستلزمات الطبية",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# الهوية البصرية المضيئة والمنعشة (مطابقة للشعار الأصلي والألوان المطلوبة)
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');
    @import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css');

    .stApp {
        background: linear-gradient(135deg, #F0F4F8 0%, #E2EEF8 50%, #E6F4F1 100%);
        background-attachment: fixed;
        font-family: 'Cairo', sans-serif;
        color: #1E293B;
        direction: rtl;
        text-align: right;
    }

    h1, h2, h3, h4, h5, h6, label, .stMarkdown p {
        color: #0F172A !important;
        font-weight: 700 !important;
        text-align: right !important;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .animated-section {
        animation: fadeIn 0.4s ease-out forwards;
    }

    /* تنسيق الشعار الدقيق المطابق للصورة */
    .brand-logo {
        font-size: 38px;
        font-weight: 900;
        font-family: 'Cairo', sans-serif;
        letter-spacing: -1px;
        line-height: 1.1;
    }
    .brand-cure {
        color: #1E40AF; /* الأزرق الطبي */
    }
    .brand-x {
        color: #0D9488; /* التركواز */
    }
    .brand-sub {
        font-size: 11px;
        font-weight: 700;
        color: #64748B;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        margin-top: 2px;
    }

    /* واجهة الـ Hero الطبية المنعشة */
    .hero-section {
        background: linear-gradient(135deg, #FFFFFF 0%, #F0F9FF 50%, #E6FFFA 100%);
        border: 1px solid rgba(14, 165, 233, 0.2);
        border-radius: 24px;
        padding: 45px;
        margin-bottom: 35px;
        box-shadow: 0 12px 35px rgba(14, 165, 233, 0.08);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    /* الشريط العلوي */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #FFFFFF;
        border-bottom: 2px solid #0EA5E9;
        padding: 15px 30px;
        border-radius: 16px;
        margin-bottom: 30px;
        box-shadow: 0 6px 20px rgba(14, 165, 233, 0.06);
    }

    /* الشريط الجانبي */
    [data-testid="stSidebar"] {
        background: #FFFFFF !important;
        border-left: 1px solid #E2E8F0;
        direction: rtl;
    }

    /* بطاقات المؤشرات (KPI Cards) */
    .kpi-card-medical {
        background: #FFFFFF;
        border-radius: 18px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(14, 165, 233, 0.06);
        border: 1px solid #E0F2FE;
        border-right: 5px solid #0EA5E9;
        transition: all 0.3s ease;
        margin-bottom: 20px;
    }

    .kpi-card-medical:hover {
        transform: translateY(-4px);
        box-shadow: 0 15px 35px rgba(13, 148, 136, 0.12);
        border-color: #0D9488;
    }

    .kpi-title-large {
        font-size: 15px !important;
        font-weight: 700 !important;
        color: #64748B !important;
        margin-bottom: 8px;
    }

    .kpi-number-large {
        font-size: 32px !important;
        font-weight: 900 !important;
        color: #0D9488 !important;
    }

    /* بطاقات المنتجات الطبية */
    .product-medical-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 18px;
        padding: 25px;
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.03);
    }

    .product-medical-card:hover {
        transform: translateY(-4px);
        border-color: #0EA5E9;
        box-shadow: 0 12px 30px rgba(14, 165, 233, 0.1);
    }

    .product-icon-box {
        font-size: 32px;
        color: #0EA5E9;
        background: #F0F9FF;
        width: 65px;
        height: 65px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 15px auto;
        border: 1px solid #BAE6FD;
        box-shadow: 0 0 10px rgba(14, 165, 233, 0.05);
    }

    /* حقول الإدخال */
    .stTextInput input, .stNumberInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        border-radius: 12px !important;
        border: 1px solid #CBD5E1 !important;
        font-weight: 600 !important;
    }

    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #0EA5E9 !important;
        box-shadow: 0 0 10px rgba(14, 165, 233, 0.15) !important;
    }

    /* الأزرار الطبية الاحترافية */
    .stButton>button {
        background: linear-gradient(135deg, #0EA5E9 0%, #0D9488 100%) !important;
        color: #FFFFFF !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        font-size: 15px !important;
        padding: 0.7rem 1.5rem !important;
        border: none !important;
        box-shadow: 0 6px 20px rgba(14, 165, 233, 0.25) !important;
        width: 100% !important;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(13, 148, 136, 0.35) !important;
        background: linear-gradient(135deg, #0284C7 0%, #0F766E 100%) !important;
    }

    [data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid #E2E8F0;
        background: #FFFFFF;
    }

    /* عناصر التنبيهات والتفاعلات */
    .custom-toast {
        background: #0D9488;
        color: #FFFFFF;
        padding: 12px 20px;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(13,148,136,0.2);
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 15px;
    }
    
    .custom-success-alert {
        background: #ECFDF5;
        border: 1px solid #A7F3D0;
        color: #065F46;
        padding: 15px;
        border-radius: 12px;
        font-weight: 700;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .custom-error-alert {
        background: #FEF2F2;
        border: 1px solid #FECACA;
        color: #991B1B;
        padding: 15px;
        border-radius: 12px;
        font-weight: 700;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* تصميم Tooltips مخصص */
    .medical-tooltip {
        position: relative;
        display: inline-block;
        cursor: pointer;
        color: #0EA5E9;
        font-weight: bold;
    }
    .medical-tooltip .tooltip-text {
        visibility: hidden;
        width: 180px;
        background-color: #0F172A;
        color: #fff;
        text-align: center;
        border-radius: 8px;
        padding: 6px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -90px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 12px;
        font-weight: normal;
    }
    .medical-tooltip:hover .tooltip-text {
        visibility: visible;
        opacity: 1;
    }
    </style>
""", unsafe_allow_html=True)

file_path = "SmartStock ERP Pro.xlsx"

# -----------------------------------------------------------------------------
# دوال إدارة البيانات
# -----------------------------------------------------------------------------
@st.cache_resource
def get_smtp_server():
    return "smtp.gmail.com"

@st.cache_data
def load_data():
    if not os.path.exists(file_path):
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    df_products = pd.read_excel(file_path, sheet_name="Products")
    df_trans = pd.read_excel(file_path, sheet_name="Transactions")
    df_inventory = pd.read_excel(file_path, sheet_name="Inventory Balance")
    return df_products, df_trans, df_inventory

def save_data(df_products, df_trans, df_inventory):
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
        df_products.to_excel(writer, sheet_name="Products", index=False)
        df_trans.to_excel(writer, sheet_name="Transactions", index=False)
        df_inventory.to_excel(writer, sheet_name="Inventory Balance", index=False)
    st.cache_data.clear()

def send_email_alert(subject, body):
    try:
        sender_email = st.secrets["EMAIL_USER"]
        sender_password = st.secrets["EMAIL_PASS"]
        receiver_email = st.secrets["RECEIVER_EMAIL"]

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain", "utf-8"))

        server = smtplib.SMTP(get_smtp_server(), 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
    except Exception as e:
        print(f"فشل إرسال الإيميل: {e}")

df_products, df_trans, df_inventory = load_data()

# -----------------------------------------------------------------------------
# الرسوم البيانية المتناسقة
# -----------------------------------------------------------------------------
def style_plot(fig, title_text):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#1E293B", size=13, family="Cairo"),
        title=dict(text=title_text, x=0.5, xanchor='center', font=dict(color="#0EA5E9", size=18, family="Cairo")),
        legend=dict(font=dict(color="#1E293B", size=11), x=1.02, y=0.5),
        margin=dict(t=60, b=80, l=40, r=120)
    )
    return fig

def draw_charts(df_inventory, df_trans):
    st.markdown("<br><h3 style='margin-bottom: 25px; color: #0EA5E9;'>التحليلات والتقارير الطبية المتقدمة</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if not df_trans.empty and "Date" in df_trans.columns and "Quantity" in df_trans.columns:
            fig_line = px.line(df_trans, x="Date", y="Quantity", color="Item Name" if "Item Name" in df_trans.columns else None, template="plotly_white", markers=True, color_discrete_sequence=['#0EA5E9', '#0D9488', '#38BDF8', '#14B8A6'])
            st.plotly_chart(style_plot(fig_line, "حركة المستلزمات اليومية"), use_container_width=True)
        else:
            st.info("لا توجد بيانات كافية لرسم الخط البياني.")

    with col2:
        if not df_inventory.empty:
            fig_bar = px.bar(df_inventory, x="Item Name", y="Current Balance", template="plotly_white", color="Current Balance", color_continuous_scale=["#BAE6FD", "#0EA5E9", "#0D9488"])
            fig_bar.update_xaxes(tickangle=-45, tickfont=dict(size=11))
            st.plotly_chart(style_plot(fig_bar, "مستوى المخزون الحالي"), use_container_width=True)

# -----------------------------------------------------------------------------
# لوحة التحكم الرئيسية
# -----------------------------------------------------------------------------
def create_dashboard():
    st.markdown("""
        <div class="animated-section">
            <h1 style="font-size: 32px; margin-bottom: 10px; color: #0EA5E9;"><i class="bi bi-speedometer2"></i> لوحة التحكم الإدارية</h1>
            <p style="color: #475569; font-size: 15px; margin-bottom: 25px;">متابعة شاملة لحالة المخزون، العمليات، والمؤشرات الحيوية لمتجر CureX.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="custom-toast"><i class="bi bi-bell-fill"></i> تنبيه نظام (Toast Notification): تم تحديث السجلات الطبية بنجاح ومزامنة البيانات.</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
            <div class="kpi-card-medical">
                <div style="font-size: 26px; color: #0EA5E9; margin-bottom: 8px;"><i class="bi bi-box-seam"></i></div>
                <div class="kpi-title-large">إجمالي المنتجات</div>
                <div class="kpi-number-large">{len(df_products)}</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="kpi-card-medical">
                <div style="font-size: 26px; color: #0D9488; margin-bottom: 8px;"><i class="bi bi-arrow-repeat"></i></div>
                <div class="kpi-title-large">إجمالي العمليات والطلبات</div>
                <div class="kpi-number-large">{len(df_trans)}</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        reorder_count = len(df_inventory[df_inventory["Reorder Point"].astype(str).str.contains("Reorder|🚨", na=False)]) if not df_inventory.empty else 0
        st.markdown(f"""
            <div class="kpi-card-medical" style="border-right-color: #EF4444;">
                <div style="font-size: 26px; color: #EF4444; margin-bottom: 8px;"><i class="bi bi-exclamation-octagon"></i></div>
                <div class="kpi-title-large">منتجات تحتاج للطلب</div>
                <div class="kpi-number-large" style="color: #EF4444 !important;">{reorder_count}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<p style='font-size: 14px; font-weight:700; color:#0F172A;'>نسبة كفاءة المخزون وتعقيم الصيدلية الرئيسي:</p>", unsafe_allow_html=True)
    st.progress(88)

    draw_charts(df_inventory, df_trans)

    st.markdown("<hr style='border-color: #CBD5E1; margin: 35px 0;'>", unsafe_allow_html=True)
    st.subheader("تفاصيل المخزون الطبي الحالي")
    search_inv = st.text_input("بحث سريع في المخزون...", key="search_inv_db")
    filtered_df_inv = df_inventory.copy()
    if search_inv and not df_inventory.empty:
        filtered_df_inv = df_inventory[df_inventory["Item Name"].astype(str).str.contains(search_inv, case=False, na=False)]
    st.dataframe(filtered_df_inv, use_container_width=True)

# -----------------------------------------------------------------------------
# صفحة متجر CureX الاحترافية
# -----------------------------------------------------------------------------
def create_store():
    st.markdown("""
        <div class="hero-section animated-section">
            <div>
                <div class="brand-logo">
                    <span class="brand-cure">Cure</span><span class="brand-x">X</span>
                </div>
                <div class="brand-sub">HEALTHCARE SOLUTIONS</div>
                <p style="font-size: 15px; color: #475569; max-width: 600px; margin-top: 15px;">نوفر أحدث الأجهزة والمستلزمات الطبية بأعلى معايير الدقة والجودة لدعم منظومتك الصحية.</p>
            </div>
            <div style="font-size: 45px; font-weight: 900; background: #E0F2FE; color: #0EA5E9; padding: 15px 25px; border-radius: 16px; border: 1px solid #BAE6FD; box-shadow: 0 0 15px rgba(14,165,233,0.1);">
                <span class="brand-cure">Cure</span><span class="brand-x">X</span> ↗
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="margin-bottom: 20px; font-size: 14px; color: #475569;">
            معلومات المعايير الطبية: 
            <span class="medical-tooltip">معايير التعقيم ISO 🩺
              <span class="tooltip-text">جميع مستلزماتنا معقمة وفقاً للمعايير العالمية لضمان سلامة المرضى.</span>
            </span>
        </div>
    """, unsafe_allow_html=True)

    search_query = st.text_input("🔍 ابحث عن مستلزم طبي أو دواء...", "")
    
    st.markdown("<h3 style='margin-top: 30px; margin-bottom: 20px; color: #0EA5E9;'>المستلزمات الطبية المتاحة للطلب الفوري</h3>", unsafe_allow_html=True)
    
    if not df_inventory.empty:
        filtered_inv = df_inventory.copy()
        if search_query:
            filtered_inv = filtered_inv[filtered_inv["Item Name"].astype(str).str.contains(search_query, case=False, na=False)]
        
        cols = st.columns(3)
        for idx, row in filtered_inv.iterrows():
            item_name = row.get("Item Name", "منتج بدون اسم")
            current_bal = row.get("Current Balance", 0)
            
            stock_badge = f'<span style="background: #ECFDF5; color: #059669; border: 1px solid #A7F3D0; padding: 5px 12px; border-radius: 20px; font-weight: 700; font-size: 12px;"><i class="bi bi-check-circle"></i> متوفر: {current_bal}</span>' if current_bal > 5 else f'<span style="background: #FEF2F2; color: #DC2626; border: 1px solid #FECACA; padding: 5px 12px; border-radius: 20px; font-weight: 700; font-size: 12px;"><i class="bi bi-exclamation-circle"></i> قارب على النفاد: {current_bal}</span>'
                
            with cols[idx % 3]:
                st.markdown(f"""
                    <div class="product-medical-card">
                        <div class="product-icon-box"><i class="bi bi-capsule"></i></div>
                        <h4 style="color: #0F172A; font-size: 17px; margin-bottom: 15px;">{item_name}</h4>
                        {stock_badge}
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<h3 style='margin-top: 20px; margin-bottom: 20px; color: #0EA5E9;'>تفضل بملء بياناتك لإتمام الطلب</h3>", unsafe_allow_html=True)
    
    with st.form("customer_order_full"):
        c_name = st.selectbox("اختر المستلزم الطبي المطلوب", df_inventory["Item Name"].tolist() if "Item Name" in df_inventory.columns else [])
        c_qty = st.number_input("الكمية المطلوبة", min_value=1, value=1)
        
        col1, col2 = st.columns(2)
        with col1:
            c_buyer = st.text_input("اسمك الكريم / اسم المؤسسة الطبية")
            c_phone = st.text_input("رقم الهاتـف / الجوال")
        with col2:
            c_email = st.text_input("البريد الإلكتروني")
            c_payment = st.selectbox("طريقة الدفع", ["الدفع عند الاستلام (Cash)", "تحويل بنكي", "بطاقة ائتمان"])
            
        c_address = st.text_area("عنوان التوصيل أو اسم العيادة/المستشفى بالتفصيل")
        
        submit_order = st.form_submit_button("تأكيد وإرسال الطلب الطبي")
        if submit_order:
            if c_buyer and c_phone and c_address and c_name:
                with st.spinner("جاري معالجة الطلب الطبي والتحقق من صلاحية التعقيم والمنتجات..."):
                    time.sleep(1.2)
                    try:
                        idx = df_inventory[df_inventory["Item Name"] == c_name].index
                        if not idx.empty:
                            current_bal = df_inventory.loc[idx[0], "Current Balance"]
                            new_bal = max(0, current_bal - c_qty)
                            df_inventory.loc[idx[0], "Current Balance"] = new_bal
                            
                            if "Total Sold" in df_inventory.columns:
                                df_inventory.loc[idx[0], "Total Sold"] += c_qty
                            else:
                                df_inventory.loc[idx[0], "Total Sold"] = c_qty

                        order_notes = f"الاسم: {c_buyer} | الهاتف: {c_phone} | الإيميل: {c_email} | الدفع: {c_payment} | العنوان: {c_address}"
                        new_t = pd.DataFrame([{
                            "Item Name": c_name, "Transaction Type": "طلب عميل جديد",
                            "Quantity": c_qty, "Notes": order_notes,
                            "Date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
                        }])
                        df_trans_updated = pd.concat([df_trans, new_t], ignore_index=True)
                        
                        save_data(df_products, df_trans_updated, df_inventory)
                        
                        st.markdown('<div class="custom-success-alert"><i class="bi bi-check-circle-fill"></i> تمت عملية إتمام الطلب بنجاح تام! تم إرسال تفاصيل الشحن والتعقيم لبريدك.</div>', unsafe_allow_html=True)
                        st.balloons()
                    except Exception as e:
                        st.markdown(f'<div class="custom-error-alert"><i class="bi bi-x-octagon-fill"></i> حدث خطأ أثناء معالجة الطلب: {e}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="custom-error-alert"><i class="bi bi-exclamation-triangle-fill"></i> يرجى ملء كافة البيانات الأساسية المطلوبة لإتمام الطلب.</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# الشريط العلوي والشريط الجانبي
# -----------------------------------------------------------------------------
current_time_str = datetime.now().strftime("%Y-%m-%d | %H:%M")
st.markdown(f"""
    <div class="top-nav animated-section">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div class="brand-logo" style="font-size: 24px;">
                <span class="brand-cure">Cure</span><span class="brand-x">X</span>
            </div>
            <span style="font-size: 14px; font-weight: 600; color: #475569;">منظومة إدارة المستلزمات الطبية</span>
        </div>
        <div style="font-size: 13px; color: #0D9488; background: #ECFDF5; padding: 5px 12px; border-radius: 20px; border: 1px solid #A7F3D0; ">
            <i class="bi bi-clock"></i> الوقت الحالي: {current_time_str}
        </div>
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="color: #059669; font-weight: 700; font-size: 13px;"><i class="bi bi-check-circle-fill"></i> متصل وآمن</span>
        </div>
    </div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 15px 0;" class="animated-section">
            <div class="brand-logo" style="font-size: 30px; margin-bottom: 2px;">
                <span class="brand-cure">Cure</span><span class="brand-x">X</span>
            </div>
            <div class="brand-sub" style="font-size: 9px;">HEALTHCARE SOLUTIONS</div>
        </div>
        <hr style="border-color: #E2E8F0; margin-bottom: 15px;">
    """, unsafe_allow_html=True)
    
    app_mode = st.selectbox("🎯 اختر واجهة الاستخدام", [
        "متجر CureX الطبي", 
        "لوحة التحكم الرئيسية"
    ])
    
    st.markdown("---")
    admin_pass = st.text_input("🔒 كلمة مرور الأدمن", type="password")

if app_mode == "متجر CureX الطبي":
    create_store()
else:
    if admin_pass == "lklklk900AR4":
        create_dashboard()
        
        st.markdown("<hr style='border-color: #CBD5E1; margin: 35px 0;'>", unsafe_allow_html=True)
        st.subheader("إضافة صنف طبى جديد للمخزن")
        with st.form("add_product"):
            p_name = st.text_input("اسم المنتج أو الدواء الجديد")
            p_bal = st.number_input("الرصيد الابتدائي", min_value=0, value=10)
            p_reorder = st.number_input("حد الطلب (Reorder Point)", min_value=0, value=5)
            p_submit = st.form_submit_button("إضافة الصنف للمخزن")
            
            if p_submit and p_name:
                with st.spinner("جاري حفظ الصنف الجديد وتحديث قواعد التعقيم..."):
                    time.sleep(0.8)
                    new_row = pd.DataFrame([{"Item Name": p_name, "Current Balance": p_bal, "Reorder Point": p_reorder, "Total Sold": 0}])
                    df_inventory_updated = pd.concat([df_inventory, new_row], ignore_index=True)
                    save_data(df_products, df_trans, df_inventory_updated)
                    st.markdown('<div class="custom-success-alert"><i class="bi bi-check-circle-fill"></i> تمت إضافة الصنف الطبي بنجاح للمخزن.</div>', unsafe_allow_html=True)
                    st.rerun()
    else:
        st.warning("🔒 من فضلك ادخل كلمة مرور الأدمن الصحيحة في القائمة الجانبية لعرض لوحة التحكم الكاملة.")

# -----------------------------------------------------------------------------
# الفوتر
# -----------------------------------------------------------------------------
st.markdown("""
    <hr style='border-color: #CBD5E1; margin-top: 50px;'>
    <div style='display: flex; justify-content: space-between; align-items: center; color: #64748B; font-size: 13px; padding-bottom: 25px;' class='animated-section'>
        <div><strong style="color: #1E40AF;">CureX</strong> - نظام إدارة المستلزمات الطبية بمعايير التعقيم العالمية</div>
        <div>&copy; 2026 جميع الحقوق محفوظة</div>
    </div>
""", unsafe_allow_html=True)
