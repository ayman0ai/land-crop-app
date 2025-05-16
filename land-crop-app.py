import streamlit as st
import pandas as pd

# إعداد الصفحة
st.set_page_config(page_title="تقييم الأرض الزراعية", page_icon="🌾", layout="centered")

# تنسيق CSS مخصص
st.markdown("""
<style>
h1, h2, h3 {
    text-align: right;
}
div.stSlider > label {
    text-align: right !important;
    display: block;
}
.stSlider div[data-baseweb="slider"] {
    direction: ltr;
}
.stSlider > div:first-child {
    direction: rtl;
    margin-bottom: 1em;
}
.stSlider span[data-baseweb="slider-value"] {
    left: auto !important;
    right: 0 !important;
}
.css-1aumxhk {
    text-align: right !important;
}
.arabic-text {
    direction: rtl;
    text-align: right;
    unicode-bidi: bidi-override; /* قد يساعد في فرض الاتجاه */
}
</style>
""", unsafe_allow_html=True)

# تنسيق CSS لمحاذاة النصوص العربية لليمين (تأكد من وجوده)
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        direction: RTL;
        text-align: right;
    }
    </style>
""", unsafe_allow_html=True)


# عرض العنوان والمقدمة
st.title("🌾 نظام ذكي لتقييم الأرض الزراعية وترشيح المحاصيل")
st.markdown(f"""
<p class="arabic-text">
مرحبًا بك في أداة تقييم الأرض الزراعية
يتيح لك هذا التطبيق تحديد مدى ملاءمة قطعة أرض لزراعة محاصيل مختلفة بناءً على خصائص التربة والمناخ .</p>
""", unsafe_allow_html=True)
st.markdown("---")

# قاعدة بيانات المحاصيل مع متوسط الإنتاجية ومتطلبات الملوحة
crops = pd.DataFrame({
    'Crop': ['قمح', 'شعير', 'ذرة', 'زيتون', 'نخيل', 'زعتر', 'ريحان', 'لافندر', 'بصل', 'ثوم'],
    'Soil': ['طينية جيدة الصرف', 'جيدة الصرف', 'رملية طينية عميقة', 'طينية خفيفة/رملية طينية جيدة الصرف', 'رملية طينية جيدة الصرف',
             'رملية/كلسية جيدة الصرف', 'طينية رملية غنية جيدة الصرف', 'رملية/حصوية كلسية جيدة الصرف',
             'طينية رملية خصبة جيدة الصرف', 'طينية رملية خصبة جيدة الصرف'],
    'pH_min': [6.5, 6.5, 6.0, 7.0, 6.5, 6.0, 6.0, 7.0, 6.0, 6.0],
    'pH_max': [7.8, 7.8, 7.5, 8.5, 8.0, 8.5, 7.5, 8.5, 7.5, 7.5],
    'Rain_min': [200, 150, 300, 200, 0, 150, 300, 200, 250, 250],
    'Rain_max': [600, 500, 700, 600, 100, 400, 900, 500, 600, 600],
    'Temp_min': [10, 10, 15, 10, 18, 15, 15, 10, 10, 10],
    'Temp_max': [30, 30, 35, 35, 45, 35, 35, 35, 30, 30],
    'Salinity_min': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    'Salinity_max': [6.0, 5.0, 3.0, 4.0, 8.0, 3.0, 3.0, 3.0, 2.5, 2.5],
    'Average_Yield': [3.5, 3.0, 5.0, 2.5, 2.0, 1.1, 1.5, 1.0, 6.0, 5.0] # متوسط الإنتاجية (طن/فدان)
})

# مدخلات المستخدم
st.header("📋 بيانات التربة والمناخ:")
soil = st.selectbox("🌍 نوع التربة", ['طينية', 'رملية', 'طينية ثقيلة', 'رملية-طينية', 'جيدة الصرف', 'طينية خفيفة', 'رملية طينية', 'رملية/حصوية', 'كلسية'])
ph = st.slider("⚗️ pH التربة", 4.0, 9.0, 7.0)
rain = st.slider("🌧️ معدل الأمطار السنوي (مم)", 0, 2000, 150)
temp = st.slider("🌡️ درجة الحرارة المتوسطة (°C)", 0, 50, 28)
salinity = st.slider("🧂 ملوحة التربة (dS/m)", 0.0, 10.0, 2.0)

# دالة حساب التوافق
def calculate_suitability(row):
    score = 0
    user_soil_simplified = soil.lower()
    crop_soil_simplified = row['Soil'].lower()
    if user_soil_simplified in crop_soil_simplified or crop_soil_simplified in user_soil_simplified:
        score += 20
    if row['pH_min'] <= ph <= row['pH_max']:
        score += 20
    if row['Rain_min'] <= rain <= row['Rain_max']:
        score += 20
    if row['Temp_min'] <= temp <= row['Temp_max']:
        score += 20
    if row['Salinity_min'] <= salinity <= row['Salinity_max']:
        score += 20
    return score

# الحسابات
crops['Suitability (%)'] = crops.apply(calculate_suitability, axis=1)
crops['Expected Yield (طن/فدان)'] = (crops['Average_Yield'] * crops['Suitability (%)']) / 100

# تقريب القيم
crops['Suitability (%)'] = crops['Suitability (%)'].round(1)
crops['Expected Yield (طن/فدان)'] = crops['Expected Yield (طن/فدان)'].round(2)

# ترشيح النتائج
recommended = crops[crops['Suitability (%)'] >= 50].sort_values(by='Suitability (%)', ascending=False)

# عرض النتائج
st.markdown("---")
st.header("📊 نتائج التقييم:")
max_score = crops['Suitability (%)'].max()
if max_score >= 90:
    overall = "🌟 ممتازة جدًا للزراعة"
elif max_score >= 70:
    overall = "✅ مناسبة للزراعة"
elif max_score >= 50:
    overall = "⚠️ مقبولة ولكن بها بعض التحديات"
else:
    overall = "❌ غير مناسبة حاليًا للزراعة"

st.success(f"**{overall}** (أقصى توافق: {max_score:.1f}%)")

if not recommended.empty:
    st.subheader("🌱 المحاصيل المقترحة حسب التوافق:")
    recommended_display = recommended[['Crop', 'Suitability (%)', 'Expected Yield (طن/فدان)']].copy()
    recommended_display.rename(columns={'Suitability (%)': 'نسبة التوافق (%)',
                                        'Expected Yield (طن/فدان)': 'الإنتاجية المتوقعة (طن/فدان)'}, inplace=True)
    st.table(recommended_display)
else:
    st.warning("⚠️ لا توجد محاصيل مناسبة حاليًا بناءً على المعايير المدخلة.")

st.markdown("---")
st.markdown("📌 **ملاحظة**: النتائج تقديرية وتفترض وجود مصدر ري مناسب، ولا تشمل خصائص مثل ملوحة المياه أو نوع السماد أو الآفات.")