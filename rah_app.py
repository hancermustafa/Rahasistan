import streamlit as st
import pandas as pd
from PIL import Image
import os

# =============================================================================
# 1. GÖRSEL TASARIM (PREMIUM CSS - Dr. Sait Sevinç Özel Tema)
# =============================================================================
def local_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        color: #333;
    }
    
    /* --- HEADER --- */
    .header-container {
        background: linear-gradient(135deg, #2980b9 0%, #2c3e50 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        margin-bottom: 25px;
        border-bottom: 5px solid #e67e22;
    }
    .header-title {
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 5px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .header-subtitle {
        font-size: 1rem;
        font-weight: 400;
        opacity: 0.9;
    }

    /* --- KARTLAR --- */
    .disease-card {
        background: white;
        border: 1px solid #eee;
        border-left: 6px solid #e67e22;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    
    .ulrich-card {
        background: #fdfcf0; /* Hafif sarımsı, eski kağıt havası */
        border: 2px solid #f1c40f;
        padding: 15px;
        border-radius: 10px;
        margin-top: 10px;
    }

    /* --- TIMELINE ADIMLARI --- */
    .step-row {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        background: white;
        border: 1px solid #f0f0f0;
        margin-bottom: 8px;
        padding: 12px;
        border-radius: 8px;
        transition: transform 0.2s;
    }
    .step-row:hover {
        border-color: #3498db;
        transform: translateX(5px);
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .code-pill {
        background: #2c3e50;
        color: #fff;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        padding: 5px 12px;
        border-radius: 5px;
        min-width: 80px;
        text-align: center;
        margin-right: 15px;
    }
    
    /* --- SEKME TASARIMI --- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f8f9fa;
        border-radius: 5px 5px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #fff;
        border-top: 3px solid #e67e22;
    }

    /* Sidebar ve Footer */
    section[data-testid="stSidebar"] {
        background-color: #f4f6f7;
    }
    .footer {
        margin-top: 50px;
        text-align: center;
        color: #95a5a6;
        font-size: 0.8rem;
        border-top: 1px solid #eee;
        padding-top: 20px;
    }
    
    /* Etiketler */
    .tag { padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: bold; color: white; margin-left: auto; }
    .bg-blue { background-color: #3498db; }
    .bg-green { background-color: #27ae60; }
    .bg-purple { background-color: #8e44ad; }
    .bg-red { background-color: #e74c3c; }
    .bg-gold { background-color: #f39c12; color: #fff; }

    /* Deploy Butonu Gizle */
    .stDeployButton {display:none;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# 2. VERİTABANI (RAH + ULRICH ENTEGRASYONU)
# =============================================================================
def get_rah_database():
    # db yapısı:
    # 'source': Kaynak bilgisi
    # 'desc': Açıklama
    # 'direct': Doğrudan RAH kodları
    # 'compact': Kompakt RAH Protokolü (Sıralı)
    # 'ulrich': Dr. Elmar Ulrich Modülü Kodları (YENİ!)

    db = {
        # --- BAĞIŞIKLIK & ENFEKSİYON ---
        "Alerji (Genel)": {
            "source": "Source 2 (Syf 121) & Ulrich M4",
            "desc": "Alerjik reaksiyonlar, histamin dengesi ve bağışıklık modülasyonu.",
            "direct": ["35.20", "64.27"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "34.00", "35.10", "35.20", "36.00", "64.27", "31.50", "01.00"],
            "ulrich": [{"code": "90.38", "name": "Alerji Tedavisi"}, {"code": "90.39", "name": "Alerji Acil Durum"}]
        },
        "Grip (Influenza)": {
            "source": "Source 2 (Syf 82) & Ulrich M4",
            "desc": "Viral enfeksiyonlar, ateş ve grip semptomları.",
            "direct": ["70.46", "43.11"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.46", "36.00", "42.10", "43.11", "31.50", "01.00"],
            "ulrich": [{"code": "90.48", "name": "Grip / Enfeksiyon"}]
        },
        "Bağışıklık Güçlendirme": {
            "source": "Source 2 (Syf 121) & Ulrich M4",
            "desc": "Genel savunma sistemini artırma.",
            "direct": ["35.10"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "34.00", "35.10", "35.11", "36.50", "31.50", "01.00"],
            "ulrich": [{"code": "90.56", "name": "Bağışıklık Sistemi (Savunma)"}]
        },

        # --- SİNİR SİSTEMİ & PSİKOLOJİ ---
        "Migren": {
            "source": "Source 2 (Syf 175) & Ulrich M4",
            "desc": "Şiddetli baş ağrısı, damar ve sinir sistemi regülasyonu.",
            "direct": ["55.60", "55.55"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.45", "38.10", "39.10", "39.40", "54.10", "54.25", "55.55", "55.60", "64.00", "31.50", "01.00"],
            "ulrich": [{"code": "90.40", "name": "Migren / Baş Ağrısı"}]
        },
        "Depresyon": {
            "source": "Source 2 (Syf 167) & Ulrich M4",
            "desc": "Ruhsal denge, nörotransmitterler ve vitalite.",
            "direct": ["72.10", "72.00"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "48.10", "64.10", "64.28", "64.29", "72.10", "75.10", "31.50", "01.00"],
            "ulrich": [{"code": "90.58", "name": "Depresyon / Ruhsal Denge"}, {"code": "90.52", "name": "Vitalizasyon (Enerji)"}]
        },
        "Stres / Tükenmişlik": {
            "source": "Source 2 (Syf 207) & Ulrich M4",
            "desc": "Aşırı stres, burnout ve sinirsel gerginlik.",
            "direct": ["75.10", "72.05"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "48.10", "50.00", "64.05", "64.10", "72.05", "75.10", "31.50", "01.00"],
            "ulrich": [{"code": "90.59", "name": "Stres / Gevşeme"}, {"code": "90.57", "name": "Vejetatif Dystoni (Sinirsel Denge)"}]
        },
        "Uyku Bozukluğu": {
            "source": "Source 2 (Syf 168) & Ulrich M4",
            "desc": "Uykuya dalma ve uykuyu sürdürme sorunları.",
            "direct": ["55.10", "55.20"],
            "compact": ["00.00", "01.00", "02.21", "31.10", "35.10", "70.10", "54.00", "55.10", "64.11", "65.30", "72.00", "75.10", "31.50", "01.00"],
            "ulrich": [{"code": "90.59", "name": "Stres / Gevşeme (Uyku Öncesi)"}]
        },

        # --- KAS & İSKELET SİSTEMİ ---
        "Romatizma / Artrit": {
            "source": "Source 2 (Syf 160) & Ulrich M4",
            "desc": "Eklem iltihabı ve ağrıları.",
            "direct": ["53.52", "53.53"],
            "compact": ["00.00", "01.00", "02.00", "31.40", "31.41", "35.10", "70.28", "52.00", "53.52", "53.53", "53.54", "31.50", "01.00"],
            "ulrich": [{"code": "90.62", "name": "Romatizma / Eklem Ağrıları"}]
        },
        "Sırt ve Bel Ağrısı": {
            "source": "Source 2 (Syf 163) & Ulrich M4",
            "desc": "Omurga kaynaklı ağrılar, lumbago.",
            "direct": ["53.70", "53.73"],
            "compact": ["00.00", "01.00", "02.00", "31.40", "35.10", "71.11", "71.50", "52.00", "53.70", "53.73", "72.05", "31.50", "01.00"],
            "ulrich": [{"code": "90.64", "name": "Sırt Ağrısı / Omurga"}]
        },
        "Spor Yaralanmaları": {
            "source": "Source 2 (Syf 156) & Ulrich M4",
            "desc": "Burkulma, ezilme, kas yırtılması.",
            "direct": ["53.21", "53.24"],
            "compact": ["00.00", "01.00", "02.00", "31.39", "31.40", "35.10", "53.21", "53.22", "53.24", "31.50", "01.00"],
            "ulrich": [{"code": "90.66", "name": "Spor Yaralanmaları / Travma"}]
        },

        # --- KALP & DOLAŞIM ---
        "Yüksek Tansiyon": {
            "source": "Source 2 (Syf 127) & Ulrich M4",
            "desc": "Kan basıncı regülasyonu.",
            "direct": ["39.60", "70.47"],
            "compact": ["00.00", "01.00", "02.00", "31.39", "35.10", "70.47", "38.00", "39.10", "39.50", "39.60", "64.00", "31.50", "01.00"],
            "ulrich": [{"code": "90.22", "name": "Hipertansiyon (Yüksek Tansiyon)"}]
        },
        "Dolaşım Bozukluğu": {
            "source": "Source 2 (Syf 125) & Ulrich M4",
            "desc": "Soğuk eller/ayaklar, genel dolaşım.",
            "direct": ["39.10"],
            "compact": ["00.00", "01.00", "02.00", "31.39", "35.10", "38.00", "38.10", "39.10", "31.50", "01.00"],
            "ulrich": [{"code": "90.20", "name": "Dolaşım / Kalp"}]
        },

        # --- SİNDİRİM SİSTEMİ ---
        "Gastrit / Mide Yanması": {
            "source": "Source 2 (Syf 143) & Ulrich M4",
            "desc": "Mide mukozası iltihabı, reflü.",
            "direct": ["47.20", "47.10"],
            "compact": ["00.00", "01.00", "02.00", "31.13", "35.10", "70.19", "46.30", "47.20", "47.10", "31.50", "01.00"],
            "ulrich": [{"code": "90.30", "name": "Mide / Bağırsak / Sindirim"}]
        },
        "Karaciğer / Detoks": {
            "source": "Source 2 (Syf 149) & Ulrich M4",
            "desc": "Karaciğer fonksiyonu ve genel temizlik.",
            "direct": ["48.10", "31.60"],
            "compact": ["00.00", "01.00", "02.00", "31.29", "35.10", "70.20", "48.10", "49.10", "31.60", "31.50", "01.00"],
            "ulrich": [{"code": "90.32", "name": "Karaciğer / Safra / Detoks"}]
        },
        
        # --- DİĞER ÖZEL DURUMLAR ---
        "Cilt Sorunları (Akne/Egzama)": {
            "source": "Source 2 (Syf 181) & Ulrich M4",
            "desc": "Cilt iltihapları ve alerjik reaksiyonlar.",
            "direct": ["63.10", "63.20"],
            "compact": ["00.00", "01.00", "02.00", "31.38", "30.65", "35.10", "70.24", "62.10", "63.10", "63.20", "31.50", "01.00"],
            "ulrich": [{"code": "90.36", "name": "Cilt / Saç / Tırnak"}]
        },
        "Hormonal Denge (Kadın)": {
            "source": "Source 2 (Syf 186) & Ulrich M4",
            "desc": "Menstruasyon, menopoz ve genel denge.",
            "direct": ["65.10", "65.60"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.22", "64.00", "65.10", "65.60", "31.50", "01.00"],
            "ulrich": [{"code": "90.42", "name": "Hormonal Düzenleme (Kadın)"}]
        }
    }
    return db

def get_program_name(code):
    # Standart RAH isimleri
    names = {
        "00.00": "Analiz Hazırlığı", "01.00": "Vitalizasyon Komple", "02.00": "Akupunktur Meridyenleri",
        "31.10": "ATP Üretimi Komple", "31.50": "Temel Detoksifikasyon", "35.10": "Bağışıklık Artırma",
        "70.xx": "Sistem Tedavisi"
    }
    if code in names: return names[code]
    if code.startswith("70."): return "Sistem Programı (Kombine)"
    return f"RAH Programı {code}"

def get_duration(code):
    if code.startswith("70."): return "10 dk"
    if code == "02.00": return "5 dk"
    return "5 dk"

def get_category_class(code):
    if code.startswith("01.") or code.startswith("02."): return "bg-blue"
    if code.startswith("31.5") or code.startswith("31.6"): return "bg-green"
    if code.startswith("70."): return "bg-purple"
    return "bg-red"

def get_category_name(code):
    if code.startswith("01.") or code.startswith("02."): return "Enerji"
    if code.startswith("31.5") or code.startswith("31.6"): return "Detoks"
    if code.startswith("70."): return "Sistem"
    return "Tedavi"

# =============================================================================
# 3. ANA UYGULAMA
# =============================================================================
def main():
    st.set_page_config(page_title="RAH Asistanı | Dr. Sait Sevinç", page_icon="🧬", layout="wide")
    local_css()

    # --- SIDEBAR ---
    with st.sidebar:
        # Logo Kontrolü
        try:
            if os.path.exists("drsaitlogo.jpeg"):
                st.image("drsaitlogo.jpeg", width=120)
            else:
                st.markdown("### Dr. Sait Sevinç")
        except:
            st.markdown("### Dr. Sait Sevinç")

        st.markdown("### Profesyonel Biyorezonans Asistanı")
        st.caption("v5.0 - Ulrich Modülü Entegre")
        st.markdown("---")
        
        st.subheader("⚙️ Cihaz Ayarı")
        device = st.radio("Cihazınızı Seçin:", ["Rayocomp PS 10", "Rayocomp PS 1000 polar"])
        
        if device == "Rayocomp PS 10":
            st.info("⚠️ **PS 10:** Kodları manuel girin veya Green Card kullanın.")
        else:
            st.success("✅ **PS 1000:** Menüden otomatik yükleyin.")

    # --- MAIN CONTENT ---
    st.markdown("""
    <div class="header-container">
        <div class="header-title">
            <span>🧬</span> RAH Biyorezonans Asistanı
        </div>
        <div class="header-subtitle">
            Dr. Sait Sevinç Kliniği İçin Özel Geliştirilmiştir<br>
            <span style="font-size: 0.8rem; opacity: 0.8;">RAH Kompendium & Dr. Elmar Ulrich Protokolleri</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    db = get_rah_database()
    
    # Arama
    st.markdown('<div class="search-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="search-label"><span>🔎</span> Rahatsızlık veya Semptom Seçimi</div>', unsafe_allow_html=True)
    disease_list = sorted(db.keys())
    selected_disease = st.selectbox("Listeden seçim yapınız:", [""] + disease_list, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    if selected_disease:
        data = db[selected_disease]
        
        # Bilgi Kartı
        st.markdown(f"""
        <div class="disease-card">
            <h2 style="color: #2c3e50; margin-bottom: 10px;">📌 {selected_disease}</h2>
            <p style="font-size: 1.1rem; color: #555;">{data['desc']}</p>
            <div style="margin-top: 15px; font-size: 0.85rem; color: #888;">
                📚 <b>Referans:</b> {data['source']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 3 SEKME
        tab1, tab2, tab3 = st.tabs(["🚀 Kompakt Protokol (RAH)", "⚡ Doğrudan Kodlar", "🧬 Ulrich Protokolü"])

        # --- TAB 1: RAH KOMPAKT ---
        with tab1:
            st.markdown("##### 📋 Standart RAH Tedavi Sıralaması")
            st.info("**Önerilen:** Hazırlık > Enerji > Tedavi > Detoks")
            
            total_minutes = 0
            for step_code in data["compact"]:
                duration = get_duration(step_code)
                cat_class = get_category_class(step_code)
                cat_name = get_category_name(step_code)
                prog_name = get_program_name(step_code)
                if step_code == "00.00": prog_name = "Analiz Hazırlığı"
                
                st.markdown(f"""
                <div class="step-row">
                    <div class="code-pill">{step_code}</div>
                    <div style="flex-grow: 1; margin-left: 15px; font-weight: 500; color: #34495e;">
                        {prog_name}
                    </div>
                    <span class="badge {cat_class}">{cat_name}</span>
                    <div style="margin-left: 15px; color: #7f8c8d; font-size: 0.9rem; font-weight: 600;">⏱️ {duration}</div>
                </div>
                """, unsafe_allow_html=True)
                try: total_minutes += int(duration.split()[0])
                except: pass
            
            st.success(f"⏱️ **Toplam RAH Süresi:** {total_minutes} Dakika")

        # --- TAB 2: DOĞRUDAN KODLAR ---
        with tab2:
            st.warning("**Not:** Bu kodlar sadece spesifik hastalık frekanslarıdır.")
            cols = st.columns(4)
            for i, code in enumerate(data["direct"]):
                with cols[i % 4]:
                    st.metric(label=f"Kod {i+1}", value=code)

        # --- TAB 3: ULRICH PROTOKOLÜ (YENİ!) ---
        with tab3:
            if "ulrich" in data:
                st.markdown(f"##### 🧬 Dr. Elmar Ulrich Özel Modülü")
                st.markdown("""
                <div class="ulrich-card">
                    <b>ℹ️ Bilgi:</b> Dr. Ulrich protokolleri, belirli hastalık grupları için optimize edilmiş özel sistem programlarıdır.
                    Genellikle 90.00 serisi (M4 Modülü) içinde yer alırlar.
                </div>
                <br>
                """, unsafe_allow_html=True)
                
                for u_prog in data["ulrich"]:
                    st.markdown(f"""
                    <div class="step-row" style="border-left: 5px solid #f1c40f;">
                        <div class="code-pill" style="background-color: #f39c12;">{u_prog['code']}</div>
                        <div style="flex-grow: 1; margin-left: 15px; font-weight: 700; color: #d35400;">
                            {u_prog['name']}
                        </div>
                        <div style="color: #7f8c8d; font-weight: 600;">⏱️ 10-20 dk</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Bu rahatsızlık için tanımlanmış özel bir Ulrich Protokolü (M4) bulunamadı.")

    else:
        st.markdown('<div class="footer">Developed for Dr. Sait Sevinç © 2025</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()