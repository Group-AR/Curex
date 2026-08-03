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
# الهوية البصرية الطبية النظيفة والحديثة (Light Medical Theme)
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');
    @import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css');

    .stApp {
        background: linear-gradient(rgba(240, 249, 255, 0.92), rgba(248, 250, 252, 0.95)), 
                    url('https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?q=80&w=1920&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
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

    /* شعار CureX المطور (دمج السهم مع نبض القلب في حرف X) */
    .curex-logo {
        font-size: 28px;
        font-weight: 900;
        color: #0F172A;
        letter-spacing: -0.5px;
    }
    .curex-logo span {
        color: #0D9488;
        position: relative;
    }
    /* محاكاة نبض القلب والسهم داخل الـ X */
    .curex-x {
        color: #2563EB;
        display: inline-block;
        position: relative;
    }
    .curex-x::after {
        content: "⚡🩺";
        font-size: 14px;
        vertical-align: super;
    }

    /* واجهة الـ Hero الاحترافية بتأثير Glass خفيف */
    .hero-section {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(13, 148, 136, 0.2);
        border-radius: 24px;
        padding: 45px;
        margin-bottom: 35px;
        box-shadow: 0 15px 35px rgba(15, 23, 42, 0.08), inset 0 1px 0 rgba(255, 255, 255, 0.8);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    /* الشريط العلوي الزجاجي */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(12px);
        border-bottom: 2px solid rgba(13, 148, 136, 0.2);
        padding: 15px 30px;
        border-radius: 16px;
        margin-bottom: 30px;
        box-shadow: 0 8px 25px rgba(15, 23, 42, 0.05);
    }

    /* الشريط الجانبي */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.95) !important;
        border-left: 1px solid rgba(13, 148, 136, 0.15);
        direction: rtl;
    }

    /* بطاقات المؤشرات (KPI Cards) الكبيرة */
    .kpi-card-medical {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(13, 148, 136, 0.08);
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-right: 6px solid #0D9488;
        transition: all 0.3s ease;
        margin-bottom: 20px;
    }

    .kpi-card-medical:hover {
        transform: translateY(-6px);
        border-color: #0D9488;
        box-shadow: 0 20px 40px rgba(13, 148, 136, 0.15);
    }

    .kpi-title-large {
        font-size: 18px !important;
        font-weight: 700 !important;
        color: #475569 !important;
        margin-bottom: 10px;
    }

    .kpi-number-large {
        font-size: 40px !important;
        font-weight: 900 !important;
        color: #0D9488 !important;
    }

    /* بطاقات المنتجات الحديثة */
    .product-medical-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(226, 232, 240, 0.9);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
        box-shadow: 0 8px 25px rgba(15, 23, 42, 0.04);
    }

    .product-medical-card:hover {
        transform: translateY(-5px);
        border-color: #0D9488;
        box-shadow: 0 15px 35px rgba(13, 148, 136, 0.12);
    }

    .product-icon-box {
        font-size: 34px;
        color: #0D9488;
        background: rgba(13, 148, 136, 0.1);
        width: 70px;
        height: 70px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 15px auto;
        border: 1px solid rgba(13, 148, 136, 0.2);
    }

    /* حقول الإدخال بتصميم حديث وتأثير Focus */
    .stTextInput input, .stNumberInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border-radius: 12px !important;
        border: 1px solid #CBD5E1 !important;
        font-weight: 600 !important;
    }

    .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox div[data-baseweb="select"]:focus {
        border-color: #0D9488 !important;
        box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.15) !important;
    }

    /* الأزرار بـ Gradient بسيط و Shadow */
    .stButton>button {
        background: linear-gradient(135deg, #2563EB 0%, #0D9488 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        font-size: 15px !important;
        padding: 0.75rem 1.5rem !important;
        border: none !important;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.2) !important;
        width: 100% !important;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(13, 148, 136, 0.35) !important;
    }

    /* تحسين الجداول (Sticky Header, Zebra Rows, Rounded Corners) */
    [data-testid="stDataFrame"] {
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid #E2E8F0;
        background: #FFFFFF;
        box-shadow: 0 4px 20px rgba(15, 23, 42, 0.03);
    }
    </style>
""", unsafe_allow_html=True)

file_path = "SmartStock ERP Pro.xlsx"

# -----------------------------------------------------------------------------
# دوال إدارة البيانات (مع استخدام التخزين المؤقت للتحسين)
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
# دالة تحديد الأيقونة المناسبة لكل منتج طبي
# -----------------------------------------------------------------------------
def get_medical_icon(item_name):
    name = str(item_name).lower()
    if "كمامة" in name or "mask" in name:
        return "bi-lungs"
    elif "قفاز" in name or "gloves" in name:
        return "bi-hand-index-thumb"
    elif "ترمومتر" in name or "حرارة" in name:
        return "bi-thermometer-half"
    elif "ضغط" in name or "bp" in name:
        return "bi-activity"
    elif "سماعة" in name or "stethoscope" in name:
        return "bi-earbuds"
    elif "كرسي" in name or "wheelchair" in name:
        return "bi-person-wheelchair"
    elif "حقنة" in name or "سرنجة" in name or "syringe" in name:
        return "bi-syringe"
    elif "محاليل" in name or "IV" in name:
        return "bi-droplet"
    else:
        return "bi-capsule"

# -----------------------------------------------------------------------------
# الرسوم البيانية الطبية المتناسقة
# -----------------------------------------------------------------------------
def style_plot(fig, title_text):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#0F172A", size=13, family="Cairo"),
        title=dict(text=title_text, x=0.5, xanchor='center', font=dict(color="#0D9488", size=18, family="Cairo")),
        legend=dict(font=dict(color="#0F172A", size=11), x=1.02, y=0.5),
        margin=dict(t=60, b=80, l=40, r=120)
    )
    return fig

def draw_charts(df_inventory, df_trans):
    st.markdown("<br><h3 style='margin-bottom: 25px; color: #0D9488;'>📊 التحليلات والتقارير الطبية المتقدمة</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if not df_trans.empty and "Date" in df_trans.columns and "Quantity" in df_trans.columns:
            fig_line = px.line(df_trans, x="Date", y="Quantity", color="Item Name" if "Item Name" in df_trans.columns else None, template="plotly_white", markers=True, color_discrete_sequence=['#2563EB', '#0D9488', '#38BDF8', '#14B8A6'])
            st.plotly_chart(style_plot(fig_line, "حركة المستلزمات اليومية (Line Chart)"), use_container_width=True)
        else:
            st.info("لا توجد بيانات كافية لرسم الخط البياني.")

    with col2:
        if not df_inventory.empty:
            fig_bar = px.bar(df_inventory, x="Item Name", y="Current Balance", template="plotly_white", color="Current Balance", color_continuous_scale=["#38BDF8", "#0D9488", "#2563EB"])
            fig_bar.update_xaxes(tickangle=-45, tickfont=dict(size=11))
            st.plotly_chart(style_plot(fig_bar, "مستوى المخزون الحالي (Bar Chart)"), use_container_width=True)

    # رسوم بيانية إضافية (Pie & Donut)
    col3, col4 = st.columns(2)
    with col3:
        if not df_inventory.empty and "Total Sold" in df_inventory.columns:
            fig_pie = px.pie(df_inventory, names="Item Name", values="Total Sold", template="plotly_white", hole=0.4, color_discrete_sequence=px.colors.sequential.Teal)
            st.plotly_chart(style_plot(fig_pie, "أكثر المنتجات مبيعاً (Donut Chart)"), use_container_width=True)
    with col4:
        if not df_inventory.empty:
            df_low = df_inventory.sort_values(by="Current Balance", ascending=True).head(5)
            fig_donut = px.bar(df_low, x="Item Name", y="Current Balance", template="plotly_white", color_discrete_sequence=["#EF4444"])
            st.plotly_chart(style_plot(fig_donut, "أقل المنتجات بالمخزون حرجة"), use_container_width=True)

# -----------------------------------------------------------------------------
# لوحة التحكم الرئيسية (Dashboard)
# -----------------------------------------------------------------------------
def create_dashboard():
    st.markdown("""
        <div class="animated-section">
            <h1 style="font-size: 32px; margin-bottom: 10px; color: #0D9488;"><i class="bi bi-speedometer2"></i> لوحة التحكم الإدارية</h1>
            <p style="color: #475569; font-size: 15px; margin-bottom: 25px;">متابعة شاملة لحالة المخزون، العمليات، والمؤشرات الحيوية لمتجر CureX.</p>
        </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
            <div class="kpi-card-medical">
                <div style="font-size: 30px; color: #2563EB; margin-bottom: 8px;"><i class="bi bi-box-seam"></i></div>
                <div class="kpi-title-large">📦 إجمالي المنتجات</div>
                <div class="kpi-number-large">{len(df_products)}</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="kpi-card-medical">
                <div style="font-size: 30px; color: #0D9488; margin-bottom: 8px;"><i class="bi bi-arrow-repeat"></i></div>
                <div class="kpi-title-large">🔄 إجمالي العمليات والطلبات</div>
                <div class="kpi-number-large">{len(df_trans)}</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        reorder_count = len(df_inventory[df_inventory["Reorder Point"].astype(str).str.contains("Reorder|🚨", na=False)]) if not df_inventory.empty else 0
        st.markdown(f"""
            <div class="kpi-card-medical" style="border-right-color: #EF4444;">
                <div style="font-size: 30px; color: #EF4444; margin-bottom: 8px;"><i class="bi bi-exclamation-octagon"></i></div>
                <div class="kpi-title-large">🚨 منتجات تحتاج للطلب</div>
                <div class="kpi-number-large" style="color: #EF4444 !important;">{reorder_count}</div>
            </div>
        """, unsafe_allow_html=True)

    draw_charts(df_inventory, df_trans)

    st.markdown("<hr style='border-color: rgba(226,232,240,0.8); margin: 35px 0;'>", unsafe_allow_html=True)
    st.subheader("تفاصيل المخزون الطبي الحالي")
    search_inv = st.text_input("🔍 بحث سريع في المخزون...", key="search_inv_db")
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
                <h1 style="font-size: 34px; margin-bottom: 10px; color: #0F172A;">
                    مرحباً بكم في متجر <span style="color: #0D9488;">CureX</span> للمستلزمات الطبية
                </h1>
                <p style="font-size: 16px; color: #475569; max-width: 600px;">نوفر أحدث الأجهزة والمستلزمات الطبية بأعلى معايير الدقة والجودة لدعم منظومتك الصحية بكفاءة واحترافية.</p>
            </div>
            <div style="font-size: 40px; font-weight: 900; background: rgba(13, 148, 136, 0.1); padding: 20px 30px; border-radius: 20px; border: 1px solid rgba(13, 148, 136, 0.25); color: #0D9488;">
                Cure<span style="color: #2563EB;">X</span> 🩺
            </div>
        </div>
    """, unsafe_allow_html=True)

    search_query = st.text_input("🔍 ابحث عن مستلزم طبي أو دواء...", "")
    
    st.markdown("<h3 style='margin-top: 30px; margin-bottom: 20px; color: #0D9488;'>المستلزمات الطبية المتاحة للطلب الفوري</h3>", unsafe_allow_html=True)
    
    if not df_inventory.empty:
        filtered_inv = df_inventory.copy()
        if search_query:
            filtered_inv = filtered_inv[filtered_inv["Item Name"].astype(str).str.contains(search_query, case=False, na=False)]
        
        cols = st.columns(3)
        for idx, row in filtered_inv.iterrows():
            item_name = row.get("Item Name", "منتج بدون اسم")
            current_bal = row.get("Current Balance", 0)
            icon_class = get_medical_icon(item_name)
            
            stock_badge = f'<span style="background: rgba(13,148,136,0.12); color: #0D9488; border: 1px solid rgba(13,148,136,0.25); padding: 6px 14px; border-radius: 20px; font-weight: 700; font-size: 12px;"><i class="bi bi-check-circle"></i> متوفر: {current_bal}</span>' if current_bal > 5 else f'<span style="background: rgba(239,68,68,0.1); color: #DC2626; border: 1px solid rgba(239,68,68,0.2); padding: 6px 14px; border-radius: 20px; font-weight: 700; font-size: 12px;"><i class="bi bi-exclamation-circle"></i> قارب على النفاد: {current_bal}</span>'
                
            with cols[idx % 3]:
                st.markdown(f"""
                    <div class="product-medical-card">
                        <div class="product-icon-box"><i class="bi {icon_class}"></i></div>
                        <h4 style="color: #0F172A; font-size: 18px; margin-bottom: 15px;">{item_name}</h4>
                        {stock_badge}
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<h3 style='margin-top: 20px; margin-bottom: 20px; color: #0D9488;'>📝 تفضل بملء بياناتك لإتمام الطلب</h3>", unsafe_allow_html=True)
    
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
        
        submit_order = st.form_submit_button("🛒 تأكيد وإرسال الطلب الطبي")
        if submit_order:
            if c_buyer and c_phone and c_address and c_name:
                with st.spinner("جاري معالجة وإرسال الطلب..."):
                    time.sleep(1)
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
                        st.success("🎉 تم تسجيل طلبك الطبي بنجاح لدى CureX!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"خطأ أثناء تسجيل الطلب: {e}")
            else:
                st.warning("⚠️ يرجى ملء البيانات الأساسية.")

# -----------------------------------------------------------------------------
# الشريط العلوي والشريط الجانبي (Sidebar & Top Nav)
# -----------------------------------------------------------------------------
current_time_str = datetime.now().strftime("%Y-%m-%d | %H:%M")
st.markdown(f"""
    <div class="top-nav animated-section">
        <div style="display: flex; align-items: center; gap: 12px;">
            <span class="curex-logo">Cure<span class="curex-x">X</span></span>
            <span style="font-size: 14px; font-weight: 600; color: #475569;">منظومة إدارة المستلزمات الطبية</span>
        </div>
        <div style="font-size: 13px; color: #0D9488; background: rgba(13,148,136,0.1); padding: 6px 14px; border-radius: 20px; border: 1px solid rgba(13,148,136,0.2);">
            <i class="bi bi-clock"></i> الوقت الحالي: {current_time_str}
        </div>
        <div style="display: flex; align-items: center; gap: 8px; color: #0D9488; font-weight: 700; font-size: 13px;">
            <i class="bi bi-shield-check-fill"></i> النظام آمن ومتصل
        </div>
    </div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 15px 0;" class="animated-section">
            <div class="curex-logo" style="font-size: 32px; margin-bottom: 4px;">Cure<span class="curex-x">X</span></div>
            <p style="font-size: 12px; color: #64748B; margin-top: 2px;">Medical Supplies ERP System</p>
        </div>
        <hr style="border-color: rgba(226,232,240,0.8); margin-bottom: 15px;">
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
        
        st.markdown("<hr style='border-color: rgba(226,232,240,0.8); margin: 35px 0;'>", unsafe_allow_html=True)
        st.subheader("إضافة صنف طبى جديد للمخزن")
        with st.form("add_product"):
            p_name = st.text_input("اسم المنتج أو الدواء الجديد")
            p_bal = st.number_input("الرصيد الابتدائي", min_value=0, value=10)
            p_reorder = st.number_input("حد الطلب (Reorder Point)", min_value=0, value=5)
            p_submit = st.form_submit_button("إضافة الصنف للمخزن")
            
            if p_submit and p_name:
                new_row = pd.DataFrame([{"Item Name": p_name, "Current Balance": p_bal, "Reorder Point": p_reorder, "Total Sold": 0}])
                df_inventory_updated = pd.concat([df_inventory, new_row], ignore_index=True)
                save_data(df_products, df_trans, df_inventory_updated)
                st.success(f"✅ تم إضافة الصنف الطبي '{p_name}' بنجاح!")
                st.rerun()
    else:
        st.warning("🔒 من فضلك ادخل كلمة مرور الأدمن الصحيحة في القائمة الجانبية لعرض لوحة التحكم الكاملة.")

# -----------------------------------------------------------------------------
# الفوتر الاحترافي (Footer)
# -----------------------------------------------------------------------------
st.markdown("""
    <hr style='border-color: rgba(226,232,240,0.8); margin-top: 50px;'>
    <div style='display: flex; justify-content: space-between; align-items: center; color: #475569; font-size: 13px; padding-bottom: 25px;' class='animated-section'>
        <div><strong style="color: #0D9488;">CureX ERP</strong> - نظام إدارة المستلزمات الطبية الحديث (الإصدار 2.6)</div>
        <div>&copy; 2026 جميع الحقوق محفوظة لمتجر CureX الطبي</div>
        <div>📧 support@curex-medical.com | 📞 +20 100 000 0000</div>
    </div>
""", unsafe_allow_html=True)
