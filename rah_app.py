import streamlit as st
import pandas as pd
import os

# =============================================================================
# 1. GÖRSEL TASARIM (CSS - DR. SAİT SEVİNÇ ÖZEL TEMA)
# =============================================================================
def local_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    /* --- ANA GÖVDE (ZORUNLU BEYAZ MOD) --- */
    [data-testid="stAppViewContainer"] {
        background-color: #ffffff !important;
        font-family: 'Inter', sans-serif;
        color: #333333 !important;
    }
    
    /* Tüm başlık ve yazıları koyu renk yap */
    h1, h2, h3, h4, h5, h6, p, div, span, label, li, button {
        color: #2c3e50; 
    }

    /* --- SIDEBAR (SOL MENÜ) --- */
    [data-testid="stSidebar"] {
        background-color: #f4f6f8 !important;
        border-right: 1px solid #e0e0e0;
    }
    [data-testid="stSidebar"] * {
        color: #2c3e50 !important;
    }
    /* Radyo butonları */
    .stRadio label {
        color: #2c3e50 !important;
        font-weight: 600;
    }

    /* --- DOĞRUDAN KODLAR İÇİN METRİK DÜZELTMESİ --- */
    /* Kodların rengi (Görünür olması için) */
    div[data-testid="stMetricValue"] {
        color: #d35400 !important; /* Canlı kiremit rengi */
        font-size: 1.6rem !important;
        font-weight: 800 !important;
    }
    /* Kod etiketi (Kod 1, Kod 2 yazısı) */
    div[data-testid="stMetricLabel"] {
        color: #7f8c8d !important; 
        font-size: 0.85rem !important;
        font-weight: 600 !important;
    }
    div[data-testid="metric-container"] {
        background-color: #fff;
        border: 1px solid #eee;
        padding: 10px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }

    /* --- GİRİŞ KUTULARI VE MENÜLER --- */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 2px solid #dce1e6 !important;
        color: #333 !important;
    }
    div[data-baseweb="select"] span {
        color: #333 !important;
    }
    ul[data-baseweb="menu"] {
        background-color: #ffffff !important;
    }
    li[role="option"] {
        color: #333 !important;
        background-color: #ffffff !important;
    }
    li[role="option"]:hover {
        background-color: #fff3e0 !important;
        font-weight: bold;
    }
    
    /* --- SEKMELER (TABS) --- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: #f1f2f6 !important;
        color: #57606f !important;
        border-radius: 6px 6px 0 0;
        font-weight: 600;
        border: 1px solid #e0e0e0;
        border-bottom: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #e67e22 !important; /* Dr. Sait Turuncusu */
        border-top: 3px solid #e67e22 !important;
    }

    /* --- HEADER VE KARTLAR --- */
    .header-container {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        margin-bottom: 30px;
        border-bottom: 5px solid #e67e22;
        text-align: center;
    }
    .header-container h1 { color: white !important; margin: 0; }
    .header-container p { color: #bdc3c7 !important; }

    .disease-card {
        background: white;
        border: 1px solid #eee;
        border-left: 6px solid #e67e22;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }
    
    .ulrich-card {
        background: #fff9db;
        border: 1px solid #f1c40f;
        padding: 15px;
        border-radius: 8px;
        color: #5d4037 !important;
    }

    /* --- TIMELINE ADIMLARI --- */
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
        border-color: #e67e22;
        transform: translateX(3px);
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .code-pill {
        background: #2c3e50;
        color: #fff !important;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        padding: 5px 12px;
        border-radius: 5px;
        min-width: 80px;
        text-align: center;
        margin-right: 15px;
        font-size: 1.1rem;
    }
    
    /* Etiketler */
    .tag { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: bold; color: white !important; margin-left: auto; }
    .bg-blue { background-color: #3498db; }
    .bg-green { background-color: #27ae60; }
    .bg-purple { background-color: #9b59b6; }
    .bg-red { background-color: #e74c3c; }

    /* Gizleme */
    .stDeployButton, footer, header {visibility: hidden;}
    .custom-footer {margin-top: 50px; text-align: center; color: #95a5a6 !important; font-size: 0.8rem; border-top: 1px solid #eee; padding-top: 20px;}
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# 2. VERİTABANI (TAM KAPSAM - RAH + ULRICH)
# =============================================================================
def get_rah_database():
    db = {
        # --- BAĞIŞIKLIK & ENFEKSİYON ---
        "Alerji (Genel)": {"source": "RAH Syf 121 & Ulrich M4", "desc": "Alerjik reaksiyonlar ve histamin dengesi.", "direct": ["35.20", "64.27"], "compact": ["00.00", "01.00", "02.00", "31.10", "34.00", "35.10", "35.20", "36.00", "64.27", "31.50", "01.00"], "ulrich": [{"code": "90.38", "name": "Alerji Tedavisi"}, {"code": "90.39", "name": "Alerji Acil Durum"}]},
        "Grip (Influenza)": {"source": "RAH Syf 82 & Ulrich M4", "desc": "Viral enfeksiyonlar ve grip.", "direct": ["70.46", "43.11"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.46", "36.00", "42.10", "43.11", "31.50", "01.00"], "ulrich": [{"code": "90.48", "name": "Grip / Enfeksiyon"}]},
        "Covid-19 / Long-Covid": {"source": "RAH Syf 137", "desc": "Koronavirüs sonrası destek.", "direct": ["43.52"], "compact": ["00.00", "01.00", "02.00", "31.11", "35.10", "22.93", "70.17", "42.70", "43.10", "43.30", "43.50", "43.52", "31.50", "01.00"], "ulrich": [{"code": "90.48", "name": "Enfeksiyon Desteği"}]},
        "Bağışıklık Güçlendirme": {"source": "RAH Syf 121 & Ulrich M4", "desc": "Genel savunma sistemi.", "direct": ["35.10"], "compact": ["00.00", "01.00", "02.00", "31.10", "34.00", "35.10", "35.11", "36.50", "31.50", "01.00"], "ulrich": [{"code": "90.56", "name": "Bağışıklık Sistemi"}]},

        # --- SİNİR SİSTEMİ & PSİKOLOJİ ---
        "Migren": {"source": "RAH Syf 175 & Ulrich M4", "desc": "Şiddetli baş ağrısı tedavisi.", "direct": ["55.60", "55.55"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.45", "38.10", "39.10", "39.40", "54.10", "54.25", "55.55", "55.60", "64.00", "31.50", "01.00"], "ulrich": [{"code": "90.40", "name": "Migren / Baş Ağrısı"}]},
        "Baş Ağrısı": {"source": "RAH Syf 174", "desc": "Genel baş ağrıları.", "direct": ["55.55"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.45", "54.10", "55.55", "72.05", "31.50", "01.00"], "ulrich": [{"code": "4.40", "name": "Baş Ağrısı (Genel)"}]},
        "Depresyon": {"source": "RAH Syf 167 & Ulrich M4", "desc": "Ruhsal denge ve vitalite.", "direct": ["72.10", "72.00"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "48.10", "64.10", "64.28", "64.29", "72.10", "75.10", "31.50", "01.00"], "ulrich": [{"code": "90.58", "name": "Depresyon / Ruhsal Denge"}, {"code": "90.52", "name": "Vitalizasyon"}]},
        "Uyku Bozukluğu": {"source": "RAH Syf 168 & Ulrich M4", "desc": "Uykuya dalma sorunları.", "direct": ["55.10", "55.20"], "compact": ["00.00", "01.00", "02.21", "31.10", "35.10", "70.10", "54.00", "55.10", "64.11", "65.30", "72.00", "75.10", "31.50", "01.00"], "ulrich": [{"code": "90.59", "name": "Stres / Gevşeme (Uyku Öncesi)"}]},
        "Stres Azaltma": {"source": "RAH Syf 207 & Ulrich M4", "desc": "Sinirsel gerginlik ve rahatlama.", "direct": ["75.10", "72.05"], "compact": ["00.00", "01.00", "02.00", "31.10", "48.10", "50.00", "64.05", "64.10", "72.05", "75.10", "31.50", "01.00"], "ulrich": [{"code": "90.57", "name": "Vejetatif Dystoni"}]},
        "DEHB (Dikkat Eksikliği)": {"source": "RAH Syf 172", "desc": "Dikkat eksikliği ve hiperaktivite.", "direct": ["55.45"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "35.20", "70.10", "54.00", "54.10", "55.45", "64.27", "83.80", "72.00", "31.50", "01.00"], "ulrich": [{"code": "4.04", "name": "Öğrenme Programı"}]},
        "Alzheimer": {"source": "RAH Syf 170", "desc": "Bellek kaybı.", "direct": ["55.30"], "compact": ["00.00", "01.00", "02.00", "31.34", "31.35", "35.10", "70.10", "38.10", "39.10", "50.10", "54.00", "55.30", "55.42", "72.00", "75.10", "31.50", "01.00"]},
        "Parkinson": {"source": "Source 2, Syf 170", "desc": "Titreme ve hareket bozukluğu.", "direct": ["55.31"], "compact": ["00.00", "01.00", "02.00", "31.34", "31.35", "35.10", "70.68", "38.10", "54.00", "55.31", "64.28", "72.00", "75.10", "31.50", "01.00"]},
        "Multipl Skleroz (MS)": {"source": "RAH Syf 172", "desc": "Merkezi sinir sistemi hastalığı.", "direct": ["55.43"], "compact": ["00.00", "01.00", "02.00", "31.34", "31.35", "35.10", "70.10", "54.00", "55.42", "55.43", "72.00", "75.10", "31.50", "01.00"]},

        # --- KAS & İSKELET SİSTEMİ ---
        "Romatizma / Artrit": {"source": "RAH Syf 160 & Ulrich M4", "desc": "Eklem iltihabı ve ağrıları.", "direct": ["53.52", "53.53"], "compact": ["00.00", "01.00", "02.00", "31.40", "31.41", "35.10", "70.28", "52.00", "53.52", "53.53", "53.54", "31.50", "01.00"], "ulrich": [{"code": "90.62", "name": "Romatizma"}]},
        "Sırt ve Bel Ağrısı": {"source": "RAH Syf 163 & Ulrich M4", "desc": "Omurga kaynaklı ağrılar, lumbago.", "direct": ["53.70", "53.73"], "compact": ["00.00", "01.00", "02.00", "31.40", "35.10", "71.11", "71.50", "52.00", "53.70", "53.73", "72.05", "31.50", "01.00"], "ulrich": [{"code": "90.64", "name": "Sırt Ağrısı / Omurga"}]},
        "Osteoporoz": {"source": "RAH Syf 165 & Ulrich", "desc": "Kemik erimesi.", "direct": ["53.80"], "compact": ["00.00", "01.00", "02.00", "31.41", "35.10", "50.00", "52.00", "52.05", "53.80", "64.00", "64.81", "31.50", "01.00"], "ulrich": [{"code": "90.63", "name": "Kemik Metabolizması"}]},
        "Spor Yaralanmaları": {"source": "RAH Syf 156 & Ulrich M4", "desc": "Burkulma, ezilme, kas yırtılması.", "direct": ["53.21", "53.24"], "compact": ["00.00", "01.00", "02.00", "31.39", "31.40", "35.10", "53.21", "53.22", "53.24", "31.50", "01.00"], "ulrich": [{"code": "90.66", "name": "Spor Yaralanmaları"}]},
        "Kemik Kırığı": {"source": "RAH Syf 155", "desc": "Kırık iyileşmesi.", "direct": ["53.11"], "compact": ["00.00", "01.00", "02.00", "31.39", "31.41", "35.10", "70.51", "52.00", "53.11", "31.50", "01.00"]},
        "Fibromiyalji": {"source": "RAH Syf 166", "desc": "Yumuşak doku romatizması.", "direct": ["53.84"], "compact": ["00.00", "01.00", "02.00", "31.38", "31.40", "35.10", "70.26", "70.27", "36.00", "52.00", "53.23", "53.25", "53.28", "53.62", "53.84", "62.10", "64.00", "31.50", "01.00"]},

        # --- KALP & DOLAŞIM ---
        "Yüksek Tansiyon": {"source": "RAH Syf 127 & Ulrich M4", "desc": "Kan basıncı regülasyonu.", "direct": ["39.60", "70.47"], "compact": ["00.00", "01.00", "02.00", "31.39", "35.10", "70.47", "38.00", "39.10", "39.40", "39.50", "39.60", "64.00", "31.50", "01.00"], "ulrich": [{"code": "90.22", "name": "Hipertansiyon"}]},
        "Dolaşım Bozukluğu": {"source": "RAH Syf 125 & Ulrich M4", "desc": "Genel dolaşım sorunları.", "direct": ["39.10"], "compact": ["00.00", "01.00", "02.00", "31.39", "35.10", "38.00", "38.10", "39.10", "31.50", "01.00"], "ulrich": [{"code": "90.20", "name": "Dolaşım / Kalp"}]},
        "Varis": {"source": "RAH Syf 126", "desc": "Toplardamar genişlemesi.", "direct": ["39.20"], "compact": ["00.00", "01.00", "02.00", "31.39", "31.87", "35.10", "36.00", "38.00", "38.50", "39.20", "39.40", "31.50", "01.00"], "ulrich": [{"code": "90.24", "name": "Venöz Dolaşım / Varis"}]},
        "Kalp Yetersizliği": {"source": "RAH Syf 129", "desc": "Kalp yetmezliği desteği.", "direct": ["41.20"], "compact": ["00.00", "01.00", "02.00", "31.15", "31.39", "31.87", "35.10", "70.18", "38.00", "39.60", "40.00", "41.20", "41.30", "42.70", "31.50", "01.00"], "ulrich": [{"code": "4.18", "name": "Kalp Programı"}]},

        # --- SİNDİRİM SİSTEMİ ---
        "Gastrit": {"source": "RAH Syf 143 & Ulrich M4", "desc": "Mide iltihabı ve yanması.", "direct": ["47.20", "47.10"], "compact": ["00.00", "01.00", "02.00", "31.13", "35.10", "70.19", "46.30", "47.20", "47.10", "31.50", "01.00"], "ulrich": [{"code": "90.30", "name": "Mide / Bağırsak"}]},
        "Karaciğer Detoks": {"source": "RAH Syf 149 & Ulrich M4", "desc": "Karaciğer fonksiyonu ve temizlik.", "direct": ["48.10", "31.60"], "compact": ["00.00", "01.00", "02.00", "31.29", "35.10", "70.20", "48.10", "49.10", "31.60", "31.50", "01.00"], "ulrich": [{"code": "90.32", "name": "Karaciğer / Safra"}]},
        "Kabızlık": {"source": "RAH Syf 148", "desc": "Obstipasyon.", "direct": ["47.86"], "compact": ["00.00", "01.00", "02.00", "31.12", "31.16", "35.10", "70.19", "46.00", "47.86", "31.50", "01.00"], "ulrich": [{"code": "90.30", "name": "Mide / Bağırsak"}]},
        "Diyabet (Şeker)": {"source": "RAH Syf 154 & Ulrich", "desc": "Şeker hastalığı.", "direct": ["51.40"], "compact": ["00.00", "01.00", "02.00", "31.14", "35.10", "70.20", "48.35", "50.20", "51.20", "51.40", "64.70", "31.50", "01.00"], "ulrich": [{"code": "90.54", "name": "Metabolizma / Diyabet"}]},

        # --- DİĞER ---
        "Cilt Sorunları (Akne)": {"source": "RAH Syf 181 & Ulrich M4", "desc": "Cilt problemleri.", "direct": ["63.10", "63.20"], "compact": ["00.00", "01.00", "02.00", "31.38", "30.65", "35.10", "70.24", "62.10", "63.10", "63.20", "31.50", "01.00"], "ulrich": [{"code": "90.36", "name": "Cilt / Saç / Tırnak"}]},
        "Hormonal Denge (Kadın)": {"source": "RAH Syf 186 & Ulrich M4", "desc": "Menstruasyon ve menopoz.", "direct": ["65.10", "65.60"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.22", "64.00", "65.10", "65.60", "31.50", "01.00"], "ulrich": [{"code": "90.42", "name": "Hormonal Düzenleme (Kadın)"}]},
        "Prostat Sorunları": {"source": "RAH Syf 200 & Ulrich", "desc": "Prostatit ve büyüme.", "direct": ["69.30", "69.10"], "compact": ["00.00", "01.00", "02.00", "31.18", "35.10", "70.23", "68.26", "69.10", "69.30", "31.50", "01.00"], "ulrich": [{"code": "90.43", "name": "Hormonal Düzenleme (Erkek)"}]},
        "Bağımlılık Bırakma": {"source": "RAH Syf 207", "desc": "Sigara, alkol vb.", "direct": ["75.17"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "48.10", "50.00", "54.10", "64.28", "64.29", "72.05", "75.10", "75.17", "31.50", "01.00"]},
        "Kilo Verme": {"source": "RAH Syf 152", "desc": "Metabolizma hızlandırma.", "direct": ["75.15"], "compact": ["00.00", "01.00", "02.00", "09.00", "31.10", "36.00", "38.00", "44.00", "46.40", "48.10", "50.00", "64.00", "75.10", "75.15", "31.50", "01.00"]},
        "Kulak Çınlaması (Tinnitus)": {"source": "RAH Syf 179 & Ulrich", "desc": "Kulak çınlaması.", "direct": ["59.10"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.15", "38.10", "39.10", "58.30", "58.40", "59.10", "59.40", "72.00", "75.00", "31.50", "01.00"], "ulrich": [{"code": "4.12", "name": "Tinnitus Programı"}]}
    }
    return db

def get_program_name(code):
    names = {
        "00.00": "Analiz Hazırlığı", "01.00": "Vitalizasyon Komple", "01.10": "Enerji Yükleme", "01.30": "Ön Kontrol", "01.40": "Çakralar Komple",
        "02.00": "Akupunktur Meridyenleri",
        "31.10": "ATP Üretimi Komple", "31.50": "Temel Detoksifikasyon", "31.51": "Detoks Kan", "31.52": "Detoks Lenf", "31.60": "Detoks Karaciğer", "31.81": "Yara İzi Tedavisi",
        "35.10": "Bağışıklık Artırma",
        "34.00": "Bağışıklık Sis. Fizyolojisi", "36.00": "Lenfatik Sistem Fizyolojisi", "38.00": "Dolaşım Sis. Fizyolojisi", "40.00": "Kalp Fizyolojisi", "42.00": "Solunum Sis. Fizyolojisi", 
        "44.00": "Böbrek Fizyolojisi", "46.00": "Sindirim Sis. Fizyolojisi", "48.00": "Karaciğer/Safra/Pankreas", "50.00": "Metabolizma Fizyolojisi", "52.00": "Kas-İskelet Sis. Fizyolojisi", 
        "54.00": "Sinir Sistemi Fizyolojisi", "56.00": "Göz Fizyolojisi", "58.00": "İşitme Fizyolojisi", "62.00": "Cilt Fizyolojisi", "64.00": "Hormonal Sistem", "66.00": "Kadın Cinsel Org.", "68.00": "Erkek Cinsel Org."
    }
    if code in names: return names[code]
    if code.startswith("70."): return "Sistem Tedavisi (Kombine)"
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
# 3. ANA UYGULAMA (UI)
# =============================================================================
def main():
    st.set_page_config(page_title="RAH Asistanı | Dr. Sait Sevinç", page_icon="🧬", layout="wide")
    local_css()

    # --- SIDEBAR ---
    with st.sidebar:
        try:
            if os.path.exists("drsaitlogo.jpeg"):
                st.image("drsaitlogo.jpeg", width=120)
            else:
                st.markdown("### 🩺 Dr. Sait Sevinç")
        except:
            st.markdown("### 🩺 Dr. Sait Sevinç")

        st.markdown("### Biyorezonans Asistanı")
        st.markdown("---")
        
        st.markdown("#### ⚙️ Cihaz Seçimi")
        device = st.radio("Cihazınızı Seçin:", ["Rayocomp PS 10", "Rayocomp PS 1000"], label_visibility="collapsed")
        
        if device == "Rayocomp PS 10":
            st.info("**PS 10 Modu:** Kodları manuel girin veya Green Card kullanın.")
        else:
            st.success("**PS 1000 Modu:** Menüden otomatik yükleyin.")

    # --- MAIN CONTENT ---
    st.markdown("""
    <div class="header-container">
        <h1>🧬 RAH Biyorezonans Asistanı</h1>
        <p>Dr. Sait Sevinç Kliniği İçin Özel Geliştirilmiştir<br>RAH Kompendium & Dr. Elmar Ulrich Protokolleri</p>
    </div>
    """, unsafe_allow_html=True)
    
    db = get_rah_database()
    
    # Arama Kutusu
    st.markdown('<h3 style="color:#2c3e50; margin-bottom:10px;">🔎 Rahatsızlık Seçimi</h3>', unsafe_allow_html=True)
    disease_list = sorted(db.keys())
    selected_disease = st.selectbox("Listeden seçim yapınız:", [""] + disease_list)

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
        tab1, tab2, tab3 = st.tabs(["🚀 Kompakt Protokol", "⚡ Doğrudan Kodlar", "🧬 Ulrich Protokolü"])

        # --- TAB 1: RAH KOMPAKT ---
        with tab1:
            st.info("**Önerilen Yöntem:** Hazırlık > Enerji > Tedavi > Detoks sıralamasıdır.")
            
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
                    <div style="flex-grow: 1; font-weight: 600; color: #34495e;">
                        {prog_name}
                    </div>
                    <span class="tag {cat_class}">{cat_name}</span>
                    <div style="margin-left: 15px; font-size: 0.85rem; color: #7f8c8d; font-weight: bold;">⏱️ {duration}</div>
                </div>
                """, unsafe_allow_html=True)
                try: total_minutes += int(duration.split()[0])
                except: pass
            
            st.success(f"⏱️ **Toplam Süre:** {total_minutes} Dakika")

        # --- TAB 2: DOĞRUDAN KODLAR ---
        with tab2:
            st.warning("**Dikkat:** Bu kodlar sadece spesifik hastalık frekanslarıdır. Tam tedavi için 'Kompakt Protokol' önerilir.")
            cols = st.columns(4)
            for i, code in enumerate(data["direct"]):
                with cols[i % 4]:
                    st.metric(label=f"Kod {i+1}", value=code)

        # --- TAB 3: ULRICH PROTOKOLÜ ---
        with tab3:
            if "ulrich" in data:
                st.markdown(f"""
                <div class="ulrich-card">
                    <b>ℹ️ Dr. Elmar Ulrich Modülü (M4):</b> Bu programlar özel sistem kartları veya 90.00 serisi içindedir.
                </div><br>
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
                st.info("Bu rahatsızlık için özel bir Ulrich protokolü tanımlanmamış.")

    else:
        st.markdown('<div class="custom-footer">Developed for Dr. Sait Sevinç © 2025</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
