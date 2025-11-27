import streamlit as st
import pandas as pd
import os

# =============================================================================
# 1. GÖRSEL TASARIM (TAMİR EDİLMİŞ CSS)
# =============================================================================
def local_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    /* --- 1. ANA GÖVDE ZORUNLU AYDINLIK MOD --- */
    [data-testid="stAppViewContainer"] {
        background-color: #ffffff !important;
        color: #333333 !important;
    }
    
    /* --- 2. SIDEBAR (SOL MENÜ) --- */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa !important;
        border-right: 1px solid #e0e0e0;
    }
    [data-testid="stSidebar"] * {
        color: #2c3e50 !important;
    }
    
    /* --- 3. INPUT KUTULARI VE SELECTBOX DÜZELTMESİ (KRİTİK NOKTA) --- */
    /* Seçim kutusunun kendisi */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #ced4da !important;
    }
    /* Seçim kutusunun içindeki yazı */
    div[data-baseweb="select"] span {
        color: #000000 !important;
    }
    /* Açılan Listenin (Dropdown) Arka Planı ve Yazısı */
    div[data-baseweb="popover"] {
        background-color: #ffffff !important;
    }
    div[data-baseweb="menu"] {
        background-color: #ffffff !important;
    }
    div[data-baseweb="menu"] li {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    /* Liste üzerine gelince (Hover) */
    div[data-baseweb="menu"] li:hover {
        background-color: #f0f2f6 !important;
    }
    /* Input üzerindeki etiketler (Label) */
    label[data-testid="stWidgetLabel"] p {
        color: #2c3e50 !important;
        font-weight: 600 !important;
    }
    
    /* --- 4. HEADER TASARIMI --- */
    .header-container {
        background: linear-gradient(135deg, #2980b9 0%, #2c3e50 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border-bottom: 4px solid #e67e22;
    }
    .header-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.8rem;
        font-weight: 800;
        color: white !important;
        margin: 0;
    }
    .header-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        font-weight: 400;
        color: #ecf0f1 !important;
        opacity: 0.9;
    }

    /* --- 5. KARTLAR --- */
    .disease-card {
        background: white;
        border: 1px solid #eee;
        border-left: 5px solid #e67e22;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .disease-card h2 { color: #2c3e50 !important; margin-top:0; }
    .disease-card p { color: #555 !important; }
    
    .ulrich-card {
        background: #fff9db;
        border: 1px solid #f1c40f;
        padding: 15px;
        border-radius: 8px;
        color: #333 !important;
        margin-bottom: 15px;
    }

    /* --- 6. TIMELINE --- */
    .step-row {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        background: white;
        border: 1px solid #f0f0f0;
        margin-bottom: 8px;
        padding: 10px 15px;
        border-radius: 8px;
        transition: transform 0.2s;
    }
    .step-row:hover {
        border-color: #3498db;
        transform: translateX(3px);
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .code-pill {
        background: #2c3e50;
        color: #fff !important;
        font-family: monospace;
        font-weight: bold;
        padding: 4px 10px;
        border-radius: 5px;
        min-width: 70px;
        text-align: center;
        margin-right: 12px;
    }
    
    /* --- 7. DİĞER --- */
    .tag { padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: bold; color: white !important; margin-left: auto; }
    .bg-blue { background-color: #3498db; }
    .bg-green { background-color: #27ae60; }
    .bg-purple { background-color: #8e44ad; }
    .bg-red { background-color: #e74c3c; }
    .bg-gold { background-color: #f39c12; }

    .stDeployButton {display:none;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .custom-footer {
        margin-top: 40px;
        text-align: center;
        color: #999 !important;
        font-size: 0.8rem;
        border-top: 1px solid #eee;
        padding-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# 2. VERİTABANI (RAH + ULRICH ENTEGRASYONU - TAM LİSTE)
# =============================================================================
def get_rah_database():
    # Source 2: Syf 104-207 + Ulrich Modülü
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
        "Covid-19 / Long-Covid": {
            "source": "Source 2, Syf. 137",
            "desc": "Koronavirüs sonrası destek.",
            "direct": ["43.52"],
            "compact": ["00.00", "01.00", "02.00", "31.11", "35.10", "22.93", "70.17", "42.70", "43.10", "43.30", "43.50", "43.52", "31.50", "01.00"],
            "ulrich": [{"code": "90.48", "name": "Enfeksiyon Desteği"}]
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
        "Parkinson Hastalığı": {
            "source": "Source 2, Syf. 170", 
            "desc": "Dopamin dengesi ve motor kontrol sistemi.", 
            "direct": ["55.31", "64.28"], 
            "compact": ["00.00", "01.00", "02.00", "31.34", "31.35", "35.10", "70.68", "38.10", "54.00", "55.31", "64.28", "72.00", "75.10", "31.50", "01.00"],
            "ulrich": [{"code": "90.53", "name": "Sinir Sistemi Dejenerasyonu"}]
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
        "Osteoporoz": {
            "source": "Source 2, Syf. 165", 
            "desc": "Kemik erimesi.", 
            "direct": ["53.80"], 
            "compact": ["00.00", "01.00", "02.00", "31.41", "35.10", "50.00", "52.00", "52.05", "53.80", "64.00", "64.81", "31.50", "01.00"],
            "ulrich": [{"code": "90.63", "name": "Kemik Metabolizması"}]
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
        "Varis": {
            "source": "Source 2, Syf. 126", 
            "desc": "Toplardamar genişlemesi.", 
            "direct": ["39.20"], 
            "compact": ["00.00", "01.00", "02.00", "31.39", "31.87", "35.10", "36.00", "38.00", "38.50", "39.20", "39.40", "31.50", "01.00"],
            "ulrich": [{"code": "90.24", "name": "Venöz Dolaşım / Varis"}]
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
        "Kabızlık": {
            "source": "Source 2, Syf. 148", 
            "desc": "Obstipasyon.", 
            "direct": ["47.86"], 
            "compact": ["00.00", "01.00", "02.00", "31.12", "31.16", "35.10", "70.19", "46.00", "47.86", "31.50", "01.00"],
            "ulrich": [{"code": "90.30", "name": "Mide / Bağırsak"}]
        },
        "Diyabet (Şeker Hastalığı)": {
            "source": "Source 2, Syf. 154", 
            "desc": "Tip 1 ve Tip 2 Diyabet desteği.", 
            "direct": ["51.40"], 
            "compact": ["00.00", "01.00", "02.00", "31.14", "35.10", "70.20", "48.35", "50.20", "51.20", "51.40", "64.70", "31.50", "01.00"],
            "ulrich": [{"code": "90.54", "name": "Metabolizma / Diyabet"}]
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
        },
        "Prostat Sorunları": {
            "source": "Source 2, Syf. 200 & Ulrich M4",
            "desc": "Prostatit ve iyi huylu büyüme.",
            "direct": ["69.30", "69.10"],
            "compact": ["00.00", "01.00", "02.00", "31.18", "35.10", "70.23", "68.26", "69.10", "69.30", "31.50", "01.00"],
            "ulrich": [{"code": "90.43", "name": "Hormonal Düzenleme (Erkek)"}]
        }
    }
    return db

def get_program_name(code):
    # Standart RAH isimleri
    names = {
        "00.00": "Analiz Hazırlığı", "01.00": "Vitalizasyon Komple", "01.10": "Enerji Yükleme", "01.30": "Ön Kontrol (Pre-control)", "01.40": "Çakralar Komple",
        "02.00": "Akupunktur Meridyenleri",
        "31.10": "ATP Üretimi Komple", "31.50": "Temel Detoksifikasyon", "31.51": "Detoks Kan Sistemi", "31.52": "Detoks Lenfatik Sistem", "31.60": "Detoks Karaciğer", "31.81": "Yara İzi Tedavisi",
        "35.10": "Bağışıklık Artırma",
        "34.00": "Bağışıklık Sis. Fizyolojisi", "36.00": "Lenfatik Sistem Fizyolojisi", "38.00": "Dolaşım Sistemi Fizyolojisi", "40.00": "Kalp Fizyolojisi", "42.00": "Solunum Sis. Fizyolojisi", "44.00": "Böbrek Fizyolojisi", "46.00": "Sindirim Sis. Fizyolojisi", "48.00": "Karaciğer/Safra/Pankreas Fizyolojisi", "50.00": "Metabolizma Fizyolojisi", "52.00": "Kas-İskelet Sis. Fizyolojisi", "54.00": "Sinir Sistemi Fizyolojisi", "56.00": "Göz Fizyolojisi", "58.00": "İşitme Organı Fizyolojisi", "62.00": "Cilt/Saç Fizyolojisi", "64.00": "Hormonal Sistem Fizyolojisi", "66.00": "Kadın Cinsel Org. Fizyolojisi", "68.00": "Erkek Cinsel Org. Fizyolojisi"
    }
    
    if code in names:
        return names[code]
    
    # Sistem programları
    if code.startswith("70."):
        return "Sistem Tedavisi (Kombine)"
    
    # Diğerleri için genel isim
    return f"RAH Programı {code}"

def get_duration(code):
    if code.startswith("70."): return "10 dk"
    if code == "02.00": return "5 dk"
    return "5 dk"

def get_category_class(code):
    # CSS sınıfı döndürür
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
        st.caption("v6.5 - Ultimate Clean Edition")
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
    
    # Arama (Label ile düzeltilmiş)
    st.markdown("### 🔎 Rahatsızlık veya Semptom Seçimi")
    disease_list = sorted(db.keys())
    selected_disease = st.selectbox("Hastalık listesinden seçim yapınız:", [""] + disease_list)

    if selected_disease:
        data = db[selected_disease]
        
        # Bilgi Kartı
        st.markdown(f"""
        <div class="disease-card">
            <h2>📌 {selected_disease}</h2>
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

        # --- TAB 3: ULRICH PROTOKOLÜ ---
        with tab3:
            if "ulrich" in data:
                st.markdown(f"##### 🧬 Dr. Elmar Ulrich Özel Modülü (M4)")
                st.markdown("""
                <div class="ulrich-card">
                    <b>ℹ️ Bilgi:</b> Dr. Ulrich protokolleri, belirli hastalık grupları için optimize edilmiş 
                    özel sistem programlarıdır (90.00 Serisi). Genellikle <b>10-20 dakika</b> uygulanır.
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
        st.markdown('<div class="custom-footer">Developed for Dr. Sait Sevinç © 2025</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
