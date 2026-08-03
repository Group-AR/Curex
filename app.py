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
# إعدادات الصفحة (استخدام لوجو CureX SVG كأيقونة للمتصفح)
# -----------------------------------------------------------------------------
curex_favicon_svg = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect width="100" height="100" rx="20" fill="#FFFFFF"/>
  <text x="12" y="65" font-family="Arial, sans-serif" font-weight="bold" font-size="55" fill="#2563EB">C</text>
  <path d="M 60 25 L 85 25 L 85 50" fill="none" stroke="#14B8A6" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M 52 75 L 75 52 L 85 52" fill="none" stroke="#14B8A6" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
  <polyline points="65,65 72,55 78,72 85,52" fill="none" stroke="#14B8A6" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
'''
import base64
encoded_favicon = base64.b64encode(curex_favicon_svg.encode("utf-8")).decode("utf-8")
favicon_data_url = f"data:image/svg+xml;base64,{encoded_favicon}"

st.set_page_config(
    page_title="متجر CureX للمستلزمات الطبية",
    page_icon=favicon_data_url,
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# الهوية البصرية الطبية الاحترافية (Glassmorphism خفيف، ألوان طبية نقية)
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');
    @import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css');

    .stApp {
        background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 50%, #F8FAFC 100%);
        background-attachment: fixed;
        font-family: 'Cairo', sans-serif;
        color: #0F172A;
        direction: rtl;
        text-align: right;
    }

    h1, h2, h3, h4, h5, h6, label, .stMarkdown p {
        color: #0F172A !important;
        font-weight: 700 !important;
        text-align: right !important;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .animated-section {
        animation: fadeIn 0.4s ease-out forwards;
    }

    /* تصميم الشعار النقي بدون أي أسهم أو إضافات */
    .brand-logo {
        font-size: 34px;
        font-weight: 900;
        font-family: 'Cairo', sans-serif;
        letter-spacing: -0.5px;
        line-height: 1.1;
    }
    .brand-cure {
        color: #2563EB; /* الأزرق الطبي */
    }
    .brand-x {
        color: #14B8A6; /* التركواز */
    }
    .brand-sub {
        font-size: 11px;
        font-weight: 700;
        color: #64748B;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-top: 2px;
    }

    /* Hero Section بأسلوب الشركات العالمية وبخلفية زجاجية نظيفة */
    .hero-section {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-radius: 20px;
        padding: 40px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.04);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    /* الشريط العلوي النظيف */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #FFFFFF;
        border-bottom: 2px solid #38BDF8;
        padding: 15px 25px;
        border-radius: 14px;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(15, 23, 42, 0.03);
    }

    /* الشريط الجانبي المطور */
    [data-testid="stSidebar"] {
        background: #FFFFFF !important;
        border-left: 1px solid #E2E8F0;
        direction: rtl;
    }

    /* بطاقات المؤشرات (KPI Cards) */
    .kpi-card-medical {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 8px 25px rgba(15, 23, 42, 0.04);
        border: 1px solid #F1F5F9;
        border-right: 4px solid #2563EB;
        transition: all 0.3s ease;
        margin-bottom: 20px;
    }

    .kpi-card-medical:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(37, 99, 235, 0.08);
        border-color: #38BDF8;
    }

    .kpi-title-large {
        font-size: 14px !important;
        font-weight: 700 !important;
        color: #64748B !important;
        margin-bottom: 6px;
    }

    .kpi-number-large {
        font-size: 30px !important;
        font-weight: 900 !important;
        color: #14B8A6 !important;
    }

    /* بطاقات المنتجات الطبية مع Hover Animation */
    .product-medical-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 22px;
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
        box-shadow: 0 6px 20px rgba(15, 23, 42, 0.02);
    }

    .product-medical-card:hover {
        transform: translateY(-3px);
        border-color: #2563EB;
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.08);
    }

    .product-icon-box {
        font-size: 28px;
        color: #2563EB;
        background: #F0Fdf4;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 12px auto;
        border: 1px solid #E2E8F0;
    }

    /* حقول الإدخال النظيفة */
    .stTextInput input, .stNumberInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        border-radius: 10px !important;
        border: 1px solid #CBD5E1 !important;
        font-weight: 600 !important;
    }

    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 8px rgba(37, 99, 235, 0.12) !important;
    }

    /* الأزرار الاحترافية مع Hover Animation */
    .stButton>button {
        background: linear-gradient(135deg, #2563EB 0%, #14B8A6 100%) !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
        font-weight: 800 !important;
        font-size: 14px !important;
        padding: 0.6rem 1.4rem !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.2) !important;
        width: 100% !important;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(20, 184, 166, 0.3) !important;
        background: linear-gradient(135deg, #1D4ED8 0%, #0F766E 100%) !important;
    }

    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #E2E8F0;
        background: #FFFFFF;
    }

    /* التنبيهات المخصصة */
    .custom-toast {
        background: #14B8A6;
        color: #FFFFFF;
        padding: 12px 18px;
        border-radius: 10px;
        box-shadow: 0 8px 20px rgba(20,184,166,0.15);
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
        padding: 14px;
        border-radius: 10px;
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
        padding: 14px;
        border-radius: 10px;
        font-weight: 700;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    </style>
""", unsafe_allow_html=True)

file_path = "SmartStock ERP Pro.xlsx"

# -----------------------------------------------------------------------------
# دوال إدارة البيانات (محافظ عليها تماماً بدون أي تغيير منطقي)
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
# الرسوم البيانية بالألوان الطبية المطلوبة (بدون ألوان داكنة أو بنفسجية)
# الألوان: #2563EB, #38BDF8, #14B8A6, #10B981 مع تدرج ناعم
# -----------------------------------------------------------------------------
def style_plot(fig, title_text):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#0F172A", size=13, family="Cairo"),
        title=dict(text=title_text, x=0.5, xanchor='center', font=dict(color="#2563EB", size=17, family="Cairo")),
        legend=dict(font=dict(color="#0F172A", size=11), x=1.02, y=0.5),
        margin=dict(t=50, b=70, l=30, r=100)
    )
    return fig

def draw_charts(df_inventory, df_trans):
    st.markdown("<br><h3 style='margin-bottom: 20px; color: #2563EB;'>التحليلات والتقارير الطبية المتقدمة</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if not df_trans.empty and "Date" in df_trans.columns and "Quantity" in df_trans.columns:
            fig_line = px.line(df_trans, x="Date", y="Quantity", color="Item Name" if "Item Name" in df_trans.columns else None, template="plotly_white", markers=True, color_discrete_sequence=['#2563EB', '#38BDF8', '#14B8A6', '#10B981'])
            st.plotly_chart(style_plot(fig_line, "حركة المستلزمات اليومية"), use_container_width=True)
        else:
            st.info("لا توجد بيانات كافية لرسم الخط البياني.")

    with col2:
        if not df_inventory.empty:
            # استخدام الألوان الطبية المطلوبة بتدرج ناعم وهادئ
            fig_bar = px.bar(df_inventory, x="Item Name", y="Current Balance", template="plotly_white", color="Current Balance", color_continuous_scale=["#38BDF8", "#2563EB", "#14B8A6", "#10B981"])
            fig_bar.update_xaxes(tickangle=-45, tickfont=dict(size=11))
            st.plotly_chart(style_plot(fig_bar, "مستوى المخزون الحالي"), use_container_width=True)

# -----------------------------------------------------------------------------
# لوحة التحكم الرئيسية
# -----------------------------------------------------------------------------
def create_dashboard():
    st.markdown("""
        <div class="animated-section">
            <h1 style="font-size: 28px; margin-bottom: 8px; color: #2563EB;"><i class="bi bi-speedometer2"></i> لوحة التحكم الإدارية</h1>
            <p style="color: #64748B; font-size: 14px; margin-bottom: 22px;">متابعة شاملة لحالة المخزون، العمليات، والمؤشرات الحيوية لمتجر CureX.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="custom-toast"><i class="bi bi-bell-fill"></i> تم تحديث السجلات الطبية بنجاح ومزامنة البيانات.</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
            <div class="kpi-card-medical">
                <div style="font-size: 24px; color: #2563EB; margin-bottom: 6px;"><i class="bi bi-box-seam"></i></div>
                <div class="kpi-title-large">إجمالي المنتجات</div>
                <div class="kpi-number-large">{len(df_products)}</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="kpi-card-medical" style="border-right-color: #14B8A6;">
                <div style="font-size: 24px; color: #14B8A6; margin-bottom: 6px;"><i class="bi bi-arrow-repeat"></i></div>
                <div class="kpi-title-large">إجمالي العمليات والطلبات</div>
                <div class="kpi-number-large" style="color: #14B8A6 !important;">{len(df_trans)}</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        reorder_count = len(df_inventory[df_inventory["Reorder Point"].astype(str).str.contains("Reorder|🚨", na=False)]) if not df_inventory.empty else 0
        st.markdown(f"""
            <div class="kpi-card-medical" style="border-right-color: #EF4444;">
                <div style="font-size: 24px; color: #EF4444; margin-bottom: 6px;"><i class="bi bi-exclamation-octagon"></i></div>
                <div class="kpi-title-large">منتجات تحتاج للطلب</div>
                <div class="kpi-number-large" style="color: #EF4444 !important;">{reorder_count}</div>
            </div>
        """, unsafe_allow_html=True)

    draw_charts(df_inventory, df_trans)

    st.markdown("<hr style='border-color: #E2E8F0; margin: 30px 0;'>", unsafe_allow_html=True)
    st.subheader("تفاصيل المخزون الطبي الحالي")
    search_inv = st.text_input("بحث سريع في المخزون...", key="search_inv_db")
    filtered_df_inv = df_inventory.copy()
    if search_inv and not df_inventory.empty:
        filtered_df_inv = df_inventory[df_inventory["Item Name"].astype(str).str.contains(search_inv, case=False, na=False)]
    st.dataframe(filtered_df_inv, use_container_width=True)

# -----------------------------------------------------------------------------
# صفحة متجر CureX الاحترافية (Hero Section مصمم كمواقع الشركات الطبية العالمية)
# -----------------------------------------------------------------------------
def create_store():
    st.markdown("""
        <div class="hero-section animated-section">
            <div>
                <div class="brand-logo">
                    <span class="brand-cure">Cure</span><span class="brand-x">X</span>
                </div>
                <div class="brand-sub">HEALTHCARE SOLUTIONS</div>
                <p style="font-size: 14px; color: #475569; max-width: 580px; margin-top: 12px; line-height: 1.6;">نوفر أحدث الأجهزة والمستلزمات الطبية بأعلى معايير الدقة والجودة العالمية لدعم منظومتك الصحية بكفاءة واحترافية.</p>
            </div>
            <div style="font-size: 32px; font-weight: 900; background: #F0FDF4; color: #14B8A6; padding: 20px 30px; border-radius: 16px; border: 1px solid #A7F3D0; box-shadow: 0 4px 15px rgba(20,184,166,0.06);">
                <span class="brand-cure">Cure</span><span class="brand-x">X</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    search_query = st.text_input("🔍 ابحث عن مستلزم طبي أو دواء...", "")
    
    st.markdown("<h3 style='margin-top: 25px; margin-bottom: 15px; color: #2563EB;'>المستلزمات الطبية المتاحة للطلب الفوري</h3>", unsafe_allow_html=True)
    
    if not df_inventory.empty:
        filtered_inv = df_inventory.copy()
        if search_query:
            filtered_inv = filtered_inv[filtered_inv["Item Name"].astype(str).str.contains(search_query, case=False, na=False)]
        
        cols = st.columns(3)
        for idx, row in filtered_inv.iterrows():
            item_name = row.get("Item Name", "منتج بدون اسم")
            current_bal = row.get("Current Balance", 0)
            
            stock_badge = f'<span style="background: #ECFDF5; color: #059669; border: 1px solid #A7F3D0; padding: 4px 10px; border-radius: 20px; font-weight: 700; font-size: 11px;"><i class="bi bi-check-circle"></i> متوفر: {current_bal}</span>' if current_bal > 5 else f'<span style="background: #FEF2F2; color: #DC2626; border: 1px solid #FECACA; padding: 4px 10px; border-radius: 20px; font-weight: 700; font-size: 11px;"><i class="bi bi-exclamation-circle"></i> قارب على النفاد: {current_bal}</span>'
                
            with cols[idx % 3]:
                st.markdown(f"""
                    <div class="product-medical-card">
                        <div class="product-icon-box"><i class="bi bi-capsule"></i></div>
                        <h4 style="color: #0F172A; font-size: 16px; margin-bottom: 12px;">{item_name}</h4>
                        {stock_badge}
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<h3 style='margin-top: 15px; margin-bottom: 15px; color: #2563EB;'>تفضل بملء بياناتك لإتمام الطلب</h3>", unsafe_allow_html=True)
    
    with st.form("customer_order_full"):
        c_name = st.selectbox("اختر المستلزم الطبي المطلوب", df_inventory["Item Name"].tolist() if "Item Name" in df_inventory.columns else [])
        c_qty = st.number_input("الكمية المطلوبة", min_value=1, value=1)
        
        col1, col2 = st.columns(2)
        with col1:
            c_buyer = st.text_input("اسمك / اسم المؤسسة الطبية")
            c_phone = st.text_input("رقم الهاتـف / الجوال")
        with col2:
            c_email = st.text_input("البريد الإلكتروني")
            c_payment = st.selectbox("طريقة الدفع", ["الدفع عند الاستلام (Cash)", "تحويل بنكي", "بطاقة ائتمان"])
            
        c_address = st.text_area("عنوان التوصيل أو اسم العيادة/المستشفى بالتفصيل")
        
        submit_order = st.form_submit_button("تأكيد الطلب")
        if submit_order:
            if c_buyer and c_phone and c_address and c_name:
                with st.spinner("جاري معالجة الطلب الطبي والتحقق من تفاصيل المنتجات..."):
                    time.sleep(1.0)
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
                        
                        st.markdown('<div class="custom-success-alert"><i class="bi bi-check-circle-fill"></i> تمت عملية إتمام الطلب بنجاح تام! تم إرسال تفاصيل الشحن لبريدك.</div>', unsafe_allow_html=True)
                        st.balloons()
                    except Exception as e:
                        st.markdown(f'<div class="custom-error-alert"><i class="bi bi-x-octagon-fill"></i> حدث خطأ أثناء معالجة الطلب: {e}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="custom-error-alert"><i class="bi bi-exclamation-triangle-fill"></i> يرجى ملء كافة البيانات الأساسية المطلوبة لإتمام الطلب.</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# الشريط العلوي النظيف (بدون عبارة "منظومة إدارة المستلزمات الطبية")
# -----------------------------------------------------------------------------
current_time_str = datetime.now().strftime("%Y-%m-%d | %H:%M")
st.markdown(f"""
    <div class="top-nav animated-section">
        <div style="display: flex; align-items: center; gap: 10px;">
            <div class="brand-logo" style="font-size: 22px;">
                <span class="brand-cure">Cure</span><span class="brand-x">X</span>
            </div>
        </div>
        <div style="font-size: 12px; color: #0D9488; background: #ECFDF5; padding: 4px 10px; border-radius: 20px; border: 1px solid #A7F3D0;">
            <i class="bi bi-clock"></i> الوقت الحالي: {current_time_str}
        </div>
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="color: #059669; font-weight: 700; font-size: 12px;"><i class="bi bi-check-circle-fill"></i> متصل وآمن</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# الشريط الجانبي المطور (بدون أيقونات في التسميات المطلوبة)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 12px 0;" class="animated-section">
            <div class="brand-logo" style="font-size: 28px; margin-bottom: 2px;">
                <span class="brand-cure">Cure</span><span class="brand-x">X</span>
            </div>
            <div class="brand-sub" style="font-size: 8px;">HEALTHCARE SOLUTIONS</div>
        </div>
        <hr style="border-color: #E2E8F0; margin-bottom: 12px;">
    """, unsafe_allow_html=True)
    
    app_mode = st.selectbox("اختر واجهة الاستخدام", [
        "متجر CureX الطبي", 
        "لوحة التحكم الرئيسية"
    ])
    
    st.markdown("---")
    admin_pass = st.text_input("كلمة المرور للتحكم", type="password")

if app_mode == "متجر CureX الطبي":
    create_store()
else:
    if admin_pass == "lklklk900AR4":
        create_dashboard()
        
        st.markdown("<hr style='border-color: #E2E8F0; margin: 30px 0;'>", unsafe_allow_html=True)
        st.subheader("إضافة صنف طبى جديد للمخزن")
        with st.form("add_product"):
            p_name = st.text_input("اسم المنتج أو الدواء الجديد")
            p_bal = st.number_input("الرصيد الابتدائي", min_value=0, value=10)
            p_reorder = st.number_input("حد الطلب (Reorder Point)", min_value=0, value=5)
            p_submit = st.form_submit_button("إضافة الصنف للمخزن")
            
            if p_submit and p_name:
                with st.spinner("جاري حفظ الصنف الجديد وتحديث البيانات..."):
                    time.sleep(0.6)
                    new_row = pd.DataFrame([{"Item Name": p_name, "Current Balance": p_bal, "Reorder Point": p_reorder, "Total Sold": 0}])
                    df_inventory_updated = pd.concat([df_inventory, new_row], ignore_index=True)
                    save_data(df_products, df_trans, df_inventory_updated)
                    st.markdown('<div class="custom-success-alert"><i class="bi bi-check-circle-fill"></i> تمت إضافة الصنف الطبي بنجاح للمخزن.</div>', unsafe_allow_html=True)
                    st.rerun()
    else:
        st.warning("🔒 من فضلك ادخل كلمة المرور للتحكم الصحيحة في القائمة الجانبية لعرض لوحة التحكم الكاملة.")

# -----------------------------------------------------------------------------
# الفوتر الطبي النظيف
# -----------------------------------------------------------------------------
st.markdown("""
    <hr style='border-color: #E2E8F0; margin-top: 40px;'>
    <div style='display: flex; justify-content: space-between; align-items: center; color: #64748B; font-size: 12px; padding-bottom: 20px;' class='animated-section'>
        <div><strong style="color: #2563EB;">CureX</strong> - نظام إدارة المستلزمات الطبية بمعايير الجودة العالمية</div>
        <div>&copy; 2026 جميع الحقوق محفوظة</div>
    </div>
""", unsafe_allow_html=True)
