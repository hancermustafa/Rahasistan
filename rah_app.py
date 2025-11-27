import streamlit as st
import pandas as pd
import os

# =============================================================================
# 1. GÖRSEL TASARIM (ULTIMATE UI FIX)
# =============================================================================
def local_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    /* --- TEMEL SAYFA YAPISI (ZORUNLU AYDINLIK MOD) --- */
    [data-testid="stAppViewContainer"] {
        background-color: #ffffff !important;
        font-family: 'Inter', sans-serif;
        color: #333333 !important;
    }
    
    /* --- SORUNLU BİLEŞENLERİN TAMİRİ --- */
    
    /* 1. SEÇİM KUTUSU (Selectbox) - Siyah ekran sorununu çözer */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 2px solid #e0e0e0 !important;
        color: #333333 !important;
        border-radius: 8px;
    }
    /* Seçili metin rengi */
    div[data-baseweb="select"] div {
        color: #333333 !important;
    }
    /* Açılan Liste (Dropdown) */
    ul[data-baseweb="menu"] {
        background-color: #ffffff !important;
        border: 1px solid #e0e0e0 !important;
    }
    li[role="option"] {
        color: #333333 !important;
        background-color: #ffffff !important;
    }
    /* Liste üzerine gelince */
    li[role="option"]:hover, li[aria-selected="true"] {
        background-color: #fff3e0 !important; /* Hafif turuncu */
        color: #e67e22 !important;
        font-weight: bold;
    }
    /* Ok işareti */
    svg {
        fill: #666666 !important;
    }

    /* 2. SEKMELER (Tabs) - Görünmez yazı sorununu çözer */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #f8f9fa !important;
        color: #555555 !important; /* Normalde koyu gri */
        border: 1px solid #e0e0e0;
        border-radius: 8px 8px 0 0;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #e67e22 !important; /* Seçilince Turuncu */
        border-top: 3px solid #e67e22 !important;
        border-bottom: none;
        box-shadow: 0 -2px 5px rgba(0,0,0,0.05);
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #e67e22 !important;
        background-color: #fff !important;
    }

    /* --- HEADER (BAŞLIK) --- */
    .header-container {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin-bottom: 30px;
        border-bottom: 5px solid #e67e22;
        text-align: center;
    }
    .header-title {
        font-size: 2rem;
        font-weight: 800;
        margin: 0;
        color: white !important;
        letter-spacing: -0.5px;
    }
    .header-subtitle {
        font-size: 0.95rem;
        opacity: 0.8;
        margin-top: 8px;
        color: #ecf0f1 !important;
    }

    /* --- KARTLAR --- */
    .disease-card {
        background: white;
        border: 1px solid #eee;
        border-left: 6px solid #e67e22;
        padding: 25px;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }
    
    /* --- TIMELINE ADIMLARI --- */
    .step-row {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        background: #fff;
        border: 1px solid #f0f2f5;
        margin-bottom: 10px;
        padding: 12px 15px;
        border-radius: 8px;
        transition: transform 0.2s;
    }
    .step-row:hover {
        border-color: #e67e22;
        transform: translateX(5px);
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .code-pill {
        background: #2c3e50;
        color: #fff !important;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        padding: 4px 12px;
        border-radius: 6px;
        min-width: 80px;
        text-align: center;
        margin-right: 15px;
        font-size: 1.1rem;
    }

    /* --- SIDEBAR --- */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa !important;
        border-right: 1px solid #e0e0e0;
    }
    [data-testid="stSidebar"] * {
        color: #2c3e50 !important;
    }
    
    /* --- ETIKETLER --- */
    .tag { padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: bold; color: white !important; margin-left: auto; }
    .bg-blue { background-color: #3498db; }
    .bg-green { background-color: #27ae60; }
    .bg-purple { background-color: #9b59b6; }
    .bg-red { background-color: #e74c3c; }

    /* Gizleme */
    .stDeployButton, footer, header {visibility: hidden;}
    .custom-footer {
        margin-top: 50px; text-align: center; color: #95a5a6 !important; font-size: 0.8rem; border-top: 1px solid #eee; padding-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# 2. VERİTABANI (RAH COMPACT + DR. ULRICH MODÜLÜ)
# =============================================================================
def get_rah_database():
    # RAH Compact (Source 2, Ch 18) + Dr. Ulrich (M4/PDF)
    db = {
        # --- 18.3 BAĞIŞIKLIK ---
        "Alerji (Genel)": {
            "source": "RAH Abstract (Syf 121) + Dr. Ulrich (4.01)",
            "desc": "Alerjik reaksiyonlar, histamin intoleransı ve genel bağışıklık dengesi.",
            "direct": ["35.20", "64.27"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "34.00", "35.10", "35.20", "36.00", "64.27", "31.50", "01.00"],
            "ulrich": [{"code": "4.01", "name": "Alerji Programı"}, {"code": "4.14", "name": "Temizleme Programı"}]
        },
        "Fruktoz İntoleransı": {
            "source": "RAH Abstract (Syf 121)",
            "desc": "Fruktoz sindirim sorunu ve bağırsak desteği.",
            "direct": ["35.30"],
            "compact": ["00.00", "01.00", "02.00", "09.34", "31.10", "34.00", "35.10", "35.30", "46.40", "46.50", "47.70", "31.50", "01.00"],
            "ulrich": [{"code": "4.07", "name": "Asidoz Programı"}]
        },
        
        # --- 18.4 LENFATİK ---
        "Lenfatik Ödem": {
            "source": "RAH Abstract (Syf 124)",
            "desc": "Lenf sıvısı birikimi ve drenaj bozukluğu.",
            "direct": ["37.15"],
            "compact": ["00.00", "01.00", "02.00", "31.25", "35.10", "36.00", "37.13", "37.15", "31.50", "01.00"]
        },
        "Tonsillit (Akut)": {
            "source": "RAH Abstract (Syf 123)",
            "desc": "Akut bademcik enfeksiyonu.",
            "direct": ["37.14"],
            "compact": ["00.00", "01.00", "02.00", "31.25", "35.10", "70.16", "36.00", "37.12", "37.13", "37.14", "43.17", "31.50", "01.00"]
        },

        # --- 18.5 DOLAŞIM ---
        "Yüksek Tansiyon": {
            "source": "RAH Abstract (Syf 127) + Dr. Ulrich (90.22)",
            "desc": "Kan basıncı regülasyonu ve damar sağlığı.",
            "direct": ["39.60", "70.47"],
            "compact": ["00.00", "01.00", "02.00", "31.39", "35.10", "70.47", "38.00", "39.10", "39.40", "39.50", "39.60", "64.00", "31.50", "01.00"],
            "ulrich": [{"code": "4.18", "name": "Kalp Programı"}, {"code": "4.02", "name": "Stres Programı"}]
        },
        "Varis (Venöz Bozukluk)": {
            "source": "RAH Abstract (Syf 126)",
            "desc": "Toplardamar genişlemesi ve bacak ödemi.",
            "direct": ["39.20"],
            "compact": ["00.00", "01.00", "02.00", "31.39", "31.87", "35.10", "36.00", "38.00", "38.50", "39.20", "39.40", "31.50", "01.00"]
        },
        "Dolaşım Bozukluğu": {
            "source": "RAH Abstract (Syf 125)",
            "desc": "Soğuk el/ayak ve genel dolaşım yetersizliği.",
            "direct": ["39.10"],
            "compact": ["00.00", "01.00", "02.00", "31.39", "35.10", "38.00", "38.10", "39.10", "31.50", "01.00"]
        },

        # --- 18.6 KALP ---
        "Kalp Yetmezliği (Sol)": {
            "source": "RAH Abstract (Syf 129)",
            "desc": "Sol ventrikül yetersizliği.",
            "direct": ["41.20"],
            "compact": ["00.00", "01.00", "02.00", "31.15", "31.39", "31.87", "35.10", "70.18", "38.00", "39.60", "40.00", "41.20", "41.30", "42.70", "31.50", "01.00"],
            "ulrich": [{"code": "4.18", "name": "Kalp Programı"}]
        },

        # --- 18.7 SOLUNUM ---
        "Bronşiyal Astım": {
            "source": "RAH Abstract (Syf 135) + Dr. Ulrich (4.20)",
            "desc": "Astım ve solunum zorluğu.",
            "direct": ["43.20"],
            "compact": ["00.00", "01.00", "02.00", "31.11", "34.00", "35.10", "35.20", "70.16", "36.00", "42.60", "42.70", "43.10", "43.20", "43.30", "31.50", "01.00"],
            "ulrich": [{"code": "4.20", "name": "Astım Programı"}]
        },
        "Bronşit (Akut)": {
            "source": "RAH Abstract (Syf 132)",
            "desc": "Akut bronş iltihabı ve öksürük.",
            "direct": ["43.13"],
            "compact": ["00.00", "01.00", "02.00", "31.11", "35.10", "70.17", "36.00", "42.60", "43.13", "43.30", "31.50", "01.00"]
        },
        "Grip / Nezle": {
            "source": "RAH Abstract (Syf 132)",
            "desc": "Soğuk algınlığı (Rinit).",
            "direct": ["43.11"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.16", "36.00", "42.10", "43.11", "31.50", "01.00"]
        },
        "Sinüzit (Akut)": {
            "source": "RAH Abstract (Syf 133)",
            "desc": "Sinüs iltihabı.",
            "direct": ["43.15"],
            "compact": ["00.00", "01.00", "02.00", "31.25", "35.10", "70.16", "36.00", "42.10", "42.20", "43.11", "43.15", "31.50", "01.00"]
        },
        "Covid-19 / Long-Covid": {
            "source": "RAH Abstract (Syf 137)",
            "desc": "Viral enfeksiyon sonrası destek.",
            "direct": ["43.52"],
            "compact": ["00.00", "01.00", "02.00", "31.11", "35.10", "22.93", "70.17", "42.70", "43.10", "43.30", "43.50", "43.52", "31.50", "01.00"]
        },

        # --- 18.8 BÖBREK ---
        "Böbrek Taşı": {
            "source": "RAH Abstract (Syf 140)",
            "desc": "Nefrolityaz.",
            "direct": ["45.25"],
            "compact": ["00.00", "01.00", "02.00", "31.23", "35.10", "44.00", "44.21", "39.65", "45.25", "31.50", "01.00"]
        },
        "Sistit (Mesane İltihabı)": {
            "source": "RAH Abstract (Syf 141)",
            "desc": "İdrar yolu enfeksiyonu.",
            "direct": ["45.35"],
            "compact": ["00.00", "01.00", "02.00", "31.17", "31.23", "35.10", "70.21", "44.10", "44.20", "45.35", "45.40", "31.50", "01.00"]
        },
        "Ödem Atma": {
            "source": "RAH Abstract (Syf 142)",
            "desc": "Vücuttan su atılımı.",
            "direct": ["45.80"],
            "compact": ["00.00", "01.00", "02.00", "09.00", "31.10", "31.87", "35.10", "36.00", "38.80", "39.50", "44.10", "44.20", "45.80", "64.10", "64.20", "64.60", "31.50", "01.00"]
        },

        # --- 18.9 SİNDİRİM ---
        "Gastrit (Akut/Kronik)": {
            "source": "RAH Abstract (Syf 143)",
            "desc": "Mide mukozası iltihabı.",
            "direct": ["47.20", "47.30"],
            "compact": ["00.00", "01.00", "02.00", "31.13", "35.10", "70.19", "46.30", "46.40", "47.30", "31.50", "01.00"],
            "ulrich": [{"code": "4.07", "name": "Asidoz Programı"}]
        },
        "Mide Ülseri": {
            "source": "RAH Abstract (Syf 145)",
            "desc": "Mide dokusu yarası.",
            "direct": ["47.40"],
            "compact": ["00.00", "01.00", "02.00", "31.13", "31.70", "35.10", "70.19", "70.41", "46.30", "46.40", "47.40", "31.50", "01.00"]
        },
        "İrritabl Bağırsak (IBS)": {
            "source": "RAH Abstract (Syf 147)",
            "desc": "Huzursuz bağırsak sendromu.",
            "direct": ["47.70"],
            "compact": ["00.00", "01.00", "02.00", "31.12", "31.16", "35.10", "70.19", "46.00", "47.70", "75.10", "31.50", "01.00"]
        },
        "Kabızlık": {
            "source": "RAH Abstract (Syf 148)",
            "desc": "Obstipasyon.",
            "direct": ["47.86"],
            "compact": ["00.00", "01.00", "02.00", "31.12", "31.16", "35.10", "70.19", "46.00", "47.86", "31.50", "01.00"]
        },

        # --- 18.10 KARACİĞER ---
        "Karaciğer Detoks/Yağlanma": {
            "source": "RAH Abstract (Syf 149)",
            "desc": "Karaciğer dejenerasyonu ve temizlik.",
            "direct": ["49.15"],
            "compact": ["00.00", "01.00", "02.00", "31.29", "35.10", "31.70", "70.20", "48.10", "49.15", "31.50", "01.00"]
        },
        "Safra Taşı": {
            "source": "RAH Abstract (Syf 151)",
            "desc": "Kolelityaz.",
            "direct": ["49.38"],
            "compact": ["00.00", "01.00", "02.00", "31.27", "31.28", "31.29", "35.10", "70.20", "48.20", "49.34", "49.37", "49.38", "50.00", "31.50", "01.00"]
        },

        # --- 18.11 METABOLİZMA ---
        "Diyabet (Şeker Hastalığı)": {
            "source": "RAH Abstract (Syf 154) + Dr. Ulrich (4.19)",
            "desc": "Tip 1 ve 2 diyabet desteği.",
            "direct": ["51.40"],
            "compact": ["00.00", "01.00", "02.00", "31.14", "35.10", "70.20", "48.35", "50.20", "51.20", "51.40", "64.70", "31.50", "01.00"],
            "ulrich": [{"code": "4.19", "name": "Diyabet Programı"}]
        },
        "Kilo Verme": {
            "source": "RAH Abstract (Syf 152)",
            "desc": "Metabolizma hızlandırma.",
            "direct": ["75.15"],
            "compact": ["00.00", "01.00", "02.00", "09.00", "31.10", "36.00", "38.00", "44.00", "46.40", "48.10", "50.00", "64.00", "75.10", "75.15", "31.50", "01.00"]
        },
        "Gut Hastalığı": {
            "source": "RAH Abstract (Syf 154)",
            "desc": "Ürik asit birikimi.",
            "direct": ["51.50"],
            "compact": ["00.00", "01.00", "02.00", "30.70", "31.10", "35.10", "50.00", "51.10", "51.50", "52.60", "71.11", "71.50", "31.50", "01.00"]
        },

        # --- 18.12 KAS & İSKELET ---
        "Sırt Ağrısı Komple": {
            "source": "RAH Abstract (Syf 163)",
            "desc": "Genel sırt ve omurga ağrıları.",
            "direct": ["53.70"],
            "compact": ["00.00", "01.00", "02.00", "31.40", "35.10", "71.11", "71.50", "52.00", "52.20", "53.23", "53.25", "53.41", "53.70", "72.05", "75.10", "31.50", "01.00"],
            "ulrich": [{"code": "4.02", "name": "Stres Programı"}]
        },
        "Bel Ağrısı (Lumbago)": {
            "source": "RAH Abstract (Syf 166)",
            "desc": "Bel tutulması.",
            "direct": ["53.83"],
            "compact": ["00.00", "01.00", "02.00", "31.40", "35.10", "52.25", "53.23", "53.41", "53.73", "53.83", "31.50", "01.00"]
        },
        "Boyun Ağrısı (Servikal)": {
            "source": "RAH Abstract (Syf 163)",
            "desc": "Boyun omurgası sorunları.",
            "direct": ["53.71"],
            "compact": ["00.00", "01.00", "02.00", "31.40", "35.10", "71.11", "71.50", "52.00", "52.20", "53.23", "53.25", "53.41", "53.71", "72.05", "75.10", "31.50", "01.00"]
        },
        "Romatizma / Artrit": {
            "source": "RAH Abstract (Syf 160)",
            "desc": "Eklem iltihabı.",
            "direct": ["53.52"],
            "compact": ["00.00", "01.00", "02.00", "31.40", "31.41", "35.10", "70.28", "52.00", "53.52", "53.53", "53.54", "31.50", "01.00"]
        },
        "Artroz (Kireçlenme)": {
            "source": "RAH Abstract (Syf 160)",
            "desc": "Eklem dejenerasyonu.",
            "direct": ["53.53"],
            "compact": ["00.00", "01.00", "02.00", "31.40", "31.41", "35.10", "70.28", "52.00", "52.61", "52.62", "53.53", "53.54", "31.50", "01.00"]
        },
        "Fibromiyalji": {
            "source": "RAH Abstract (Syf 166)",
            "desc": "Yumuşak doku romatizması.",
            "direct": ["53.84"],
            "compact": ["00.00", "01.00", "02.00", "31.38", "31.40", "35.10", "70.26", "70.27", "36.00", "52.00", "53.23", "53.25", "53.28", "53.62", "53.84", "62.10", "64.00", "31.50", "01.00"]
        },
        "Osteoporoz": {
            "source": "RAH Abstract (Syf 165)",
            "desc": "Kemik erimesi.",
            "direct": ["53.80"],
            "compact": ["00.00", "01.00", "02.00", "31.41", "35.10", "50.00", "52.00", "52.05", "53.80", "64.00", "64.81", "31.50", "01.00"]
        },
        "Kemik Kırığı": {
            "source": "RAH Abstract (Syf 155)",
            "desc": "Kırık iyileşmesi.",
            "direct": ["53.11"],
            "compact": ["00.00", "01.00", "02.00", "31.39", "31.41", "35.10", "70.51", "52.00", "53.11", "31.50", "01.00"]
        },

        # --- 18.13 SİNİR SİSTEMİ ---
        "Baş Ağrısı": {
            "source": "RAH Abstract (Syf 174)",
            "desc": "Genel baş ağrıları.",
            "direct": ["55.55"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.45", "54.10", "55.55", "72.05", "31.50", "01.00"],
            "ulrich": [{"code": "4.40", "name": "Baş Ağrısı (Migren)"}]
        },
        "Migren": {
            "source": "RAH Abstract (Syf 175)",
            "desc": "Şiddetli baş ağrısı.",
            "direct": ["55.60"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.45", "38.10", "39.10", "39.40", "54.10", "54.25", "55.55", "55.60", "64.00", "72.05", "31.50", "01.00"]
        },
        "Uyku Bozukluğu": {
            "source": "RAH Abstract (Syf 168)",
            "desc": "Uykuya dalma ve sürdürme sorunu.",
            "direct": ["55.10", "55.20"],
            "compact": ["00.00", "01.00", "02.21", "31.10", "35.10", "70.10", "54.00", "55.10", "64.11", "65.30", "72.00", "75.10", "31.50", "01.00"]
        },
        "Depresyon": {
            "source": "RAH Abstract (Syf 167)",
            "desc": "Ruhsal çöküntü.",
            "direct": ["72.10"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "48.10", "64.10", "64.28", "64.29", "72.10", "75.10", "31.50", "01.00"]
        },
        "Stres Azaltma": {
            "source": "RAH Abstract (Syf 207) + Dr. Ulrich (4.02)",
            "desc": "Sinirsel gerginlik.",
            "direct": ["75.10"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "48.10", "50.00", "64.05", "64.10", "64.20", "64.28", "64.29", "64.30", "64.35", "64.40", "64.50", "72.05", "75.10", "31.50", "01.00"],
            "ulrich": [{"code": "4.02", "name": "Stres Programı"}]
        },
        "Bağımlılık Bırakma": {
            "source": "RAH Abstract (Syf 207)",
            "desc": "Sigara, alkol vb.",
            "direct": ["75.17"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "48.10", "50.00", "54.10", "64.28", "64.29", "72.05", "75.10", "75.17", "31.50", "01.00"]
        },
        "Alzheimer": {
            "source": "RAH Abstract (Syf 170)",
            "desc": "Bellek kaybı.",
            "direct": ["55.30"],
            "compact": ["00.00", "01.00", "02.00", "31.34", "31.35", "35.10", "70.10", "38.10", "39.10", "50.10", "54.00", "55.30", "55.42", "72.00", "75.10", "31.50", "01.00"]
        },
        "Parkinson": {
            "source": "Source 2, Syf. 170", 
            "desc": "Titreme ve hareket bozukluğu.", 
            "direct": ["55.31"], 
            "compact": ["00.00", "01.00", "02.00", "31.34", "31.35", "35.10", "70.68", "38.10", "54.00", "55.31", "64.28", "72.00", "75.10", "31.50", "01.00"]
        },
        "MS (Multipl Skleroz)": {
            "source": "RAH Abstract (Syf 172)",
            "desc": "Merkezi sinir sistemi hastalığı.",
            "direct": ["55.43"],
            "compact": ["00.00", "01.00", "02.00", "31.34", "31.35", "35.10", "70.10", "54.00", "55.42", "55.43", "72.00", "75.10", "31.50", "01.00"]
        },
        "DEHB (Dikkat Eksikliği)": {
            "source": "RAH Abstract (Syf 172) + Dr. Ulrich (4.04)",
            "desc": "Konsantrasyon bozukluğu.",
            "direct": ["55.45"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "35.20", "70.10", "54.00", "54.10", "55.45", "64.27", "83.80", "72.00", "31.50", "01.00"],
            "ulrich": [{"code": "4.04", "name": "Öğrenme Programı"}]
        },

        # --- 18.14 GÖZ ---
        "Katarakt": {
            "source": "RAH Abstract (Syf 176)",
            "desc": "Göz merceği bulanıklığı.",
            "direct": ["57.20"],
            "compact": ["00.00", "01.00", "02.00", "31.31", "35.10", "70.12", "56.00", "56.40", "57.20", "31.50", "01.00"]
        },
        "Glokom": {
            "source": "RAH Abstract (Syf 176)",
            "desc": "Göz tansiyonu.",
            "direct": ["57.30"],
            "compact": ["00.00", "01.00", "02.00", "31.31", "35.10", "70.12", "56.00", "56.60", "57.10", "57.30", "31.50", "01.00"]
        },
        "Sarı Nokta (Makula)": {
            "source": "RAH Abstract (Syf 177)",
            "desc": "Görme merkezi dejenerasyonu.",
            "direct": ["57.40"],
            "compact": ["00.00", "01.00", "02.00", "31.31", "31.81", "31.87", "35.10", "70.12", "38.10", "39.10", "54.22", "56.34", "56.61", "56.62", "57.40", "31.50", "01.00"]
        },
        "Konjonktivit": {
            "source": "RAH Abstract (Syf 178)",
            "desc": "Göz iltihabı.",
            "direct": ["57.52"],
            "compact": ["00.00", "01.00", "02.00", "31.31", "35.10", "70.12", "56.00", "57.52", "31.50", "01.00"]
        },

        # --- 18.15 KULAK ---
        "Tinnitus (Çınlama)": {
            "source": "RAH Abstract (Syf 179) + Dr. Ulrich (4.12)",
            "desc": "Kulak çınlaması.",
            "direct": ["59.10"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.15", "38.10", "39.10", "58.30", "58.40", "59.10", "59.40", "72.00", "75.00", "31.50", "01.00"],
            "ulrich": [{"code": "4.12", "name": "Tinnitus Programı"}]
        },
        "Ani İşitme Kaybı": {
            "source": "RAH Abstract (Syf 180)",
            "desc": "",
            "direct": ["59.40"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.15", "38.10", "39.10", "58.30", "58.40", "59.10", "59.30", "59.40", "75.00", "31.50", "01.00"]
        },

        # --- 18.16 CİLT ---
        "Sedef (Psoriasis)": {
            "source": "RAH Abstract (Syf 181)",
            "desc": "Ciltte pullanma.",
            "direct": ["63.10"],
            "compact": ["00.00", "01.00", "02.00", "31.38", "30.65", "35.10", "70.24", "62.10", "62.20", "62.60", "63.10", "72.00", "75.00", "31.50", "01.00"]
        },
        "Nörodermatit": {
            "source": "RAH Abstract (Syf 181)",
            "desc": "Atopik egzama.",
            "direct": ["63.20"],
            "compact": ["00.00", "01.00", "02.00", "30.65", "31.38", "35.10", "70.24", "54.20", "54.50", "62.10", "62.20", "63.20", "72.00", "75.00", "31.50", "01.00"]
        },
        "Cilt Mantarı": {
            "source": "RAH Abstract (Syf 183) + Dr. Ulrich (4.05)",
            "desc": "Mikoz.",
            "direct": ["63.50"],
            "compact": ["00.00", "01.00", "02.00", "30.65", "31.38", "35.10", "70.24", "62.10", "63.50", "31.50", "01.00"],
            "ulrich": [{"code": "4.05", "name": "Mantar Programı"}]
        },
        "Saç Dökülmesi": {
            "source": "RAH Abstract (Syf 185)",
            "desc": "Androgenetik alopesi.",
            "direct": ["63.90"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "48.10", "50.00", "54.00", "63.90", "64.00", "65.10", "70.11", "75.10", "31.50", "01.00"]
        },

        # --- 18.17 HORMONAL ---
        "Hormonal Denge (Kadın)": {
            "source": "RAH Abstract (Syf 186) + Dr. Ulrich (4.08)",
            "desc": "Genel denge.",
            "direct": ["65.10"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.22", "64.00", "65.10", "31.50", "01.00"],
            "ulrich": [{"code": "4.08", "name": "Kadın Hormon Programı"}]
        },
        "Hormonal Denge (Erkek)": {
            "source": "RAH Abstract (Syf 186) + Dr. Ulrich (4.09)",
            "desc": "Genel denge.",
            "direct": ["65.20"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.23", "64.00", "65.20", "31.50", "01.00"],
            "ulrich": [{"code": "4.09", "name": "Erkek Hormon Programı"}]
        },
        "Menopoz": {
            "source": "RAH Abstract (Syf 195)",
            "desc": "Klimakterik şikayetler.",
            "direct": ["65.60"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.22", "64.10", "64.20", "65.10", "65.60", "66.00", "72.00", "75.00", "31.50", "01.00"]
        },
        "Tiroid (Hipertiroidi)": {
            "source": "RAH Abstract (Syf 188)",
            "desc": "Çok çalışma.",
            "direct": ["65.33"],
            "compact": ["00.00", "01.00", "02.00", "31.33", "35.10", "70.54", "64.10", "64.20", "64.30", "65.33", "31.50", "01.00"]
        },
        "Tiroid (Hipotiroidi)": {
            "source": "RAH Abstract (Syf 189)",
            "desc": "Az çalışma.",
            "direct": ["65.34"],
            "compact": ["00.00", "01.00", "02.00", "31.33", "35.10", "70.54", "64.10", "64.20", "64.30", "65.34", "31.50", "01.00"]
        },

        # --- 18.18 CİNSEL ORGANLAR ---
        "Prostatit": {
            "source": "RAH Abstract (Syf 200)",
            "desc": "Prostat iltihabı.",
            "direct": ["69.30"],
            "compact": ["00.00", "01.00", "02.00", "31.18", "35.10", "70.23", "68.26", "69.30", "31.50", "01.00"]
        },
        "Endometriozis": {
            "source": "RAH Abstract (Syf 199)",
            "desc": "Rahim içi doku.",
            "direct": ["67.30"],
            "compact": ["00.00", "01.00", "02.00", "31.20", "31.22", "31.81", "35.10", "70.22", "36.10", "64.80", "65.10", "65.30", "65.31", "65.50", "66.00", "67.30", "72.00", "75.00", "31.50", "01.00"]
        },

        # --- 18.19 KAN ---
        "Demir Eksikliği": {
            "source": "RAH Abstract (Syf 202)",
            "desc": "Anemi.",
            "direct": ["33.24"],
            "compact": ["00.00", "01.00", "02.00", "07.21", "31.39", "35.10", "32.06", "32.10", "33.24", "33.60", "31.50", "01.00"]
        },
        
        # --- EKSTRA ---
        "Asidoz (Asitlenme)": {
            "source": "Dr. Ulrich (4.07)",
            "desc": "Vücut asit dengesinin bozulması.",
            "direct": ["31.53"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "31.53", "06.00", "31.50", "01.00"],
            "ulrich": [{"code": "4.07", "name": "Asidoz Programı"}]
        },
        "Operasyon Sonrası Bakım": {
            "source": "Dr. Ulrich (4.10)",
            "desc": "Cerrahi sonrası iyileşme.",
            "direct": ["70.63"],
            "compact": ["00.00", "01.00", "31.80", "31.81", "31.82", "70.63", "35.10", "31.50", "01.00"],
            "ulrich": [{"code": "4.10", "name": "Op. Sonrası Bakım"}]
        }
    }
    return db

def get_program_name(code):
    # Temel programların isimleri
    names = {
        "00.00": "Analiz Hazırlığı", "01.00": "Vitalizasyon Komple", "01.10": "Enerji Yükleme", "01.30": "Ön Kontrol", "01.40": "Çakralar Komple",
        "02.00": "Akupunktur Meridyenleri",
        "31.10": "ATP Üretimi Komple", "31.50": "Temel Detoksifikasyon", "31.51": "Detoks Kan", "31.52": "Detoks Lenf", "31.60": "Detoks Karaciğer", "31.81": "Yara İzi Tedavisi",
        "35.10": "Bağışıklık Artırma",
        "34.00": "Bağışıklık Sis. Fizyolojisi", "36.00": "Lenfatik Sistem Fizyolojisi", "38.00": "Dolaşım Sis. Fizyolojisi", "40.00": "Kalp Fizyolojisi", "42.00": "Solunum Sis. Fizyolojisi", 
        "44.00": "Böbrek Fizyolojisi", "46.00": "Sindirim Sis. Fizyolojisi", "48.00": "Karaciğer/Safra/Pankreas", "50.00": "Metabolizma Fizyolojisi", "52.00": "Kas-İskelet Sis. Fizyolojisi", 
        "54.00": "Sinir Sistemi Fizyolojisi", "56.00": "Göz Fizyolojisi", "58.00": "İşitme Fizyolojisi", "62.00": "Cilt Fizyolojisi", "64.00": "Hormonal Sistem", "66.00": "Kadın Cinsel Org.", "68.00": "Erkek Cinsel Org."
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
# 3. ANA UYGULAMA (STREAMLIT)
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

        st.markdown("### Profesyonel Biyorezonans Asistanı")
        st.caption("v8.0 - Grand Master Edition")
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
    
    # Arama Kutusu
    st.markdown('<h3 style="color:#2c3e50;">🔎 Rahatsızlık Seçimi</h3>', unsafe_allow_html=True)
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
        tab1, tab2, tab3 = st.tabs(["🚀 Kompakt Protokol (RAH)", "⚡ Doğrudan Kodlar", "🧬 Ulrich Protokolü"])

        # --- TAB 1: RAH KOMPAKT ---
        with tab1:
            st.info("**Önerilen Yöntem:** Bu sıralama; **Hazırlık > Enerji > Tedavi > Detoks** mantığıyla hazırlanmıştır.")
            
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
                    <span class="tag {cat_class}">{cat_name}</span>
                    <div style="margin-left: 15px; color: #7f8c8d; font-size: 0.9rem; font-weight: 600;">⏱️ {duration}</div>
                </div>
                """, unsafe_allow_html=True)
                try: total_minutes += int(duration.split()[0])
                except: pass
            
            st.success(f"⏱️ **Toplam RAH Süresi:** {total_minutes} Dakika")

        # --- TAB 2: DOĞRUDAN KODLAR ---
        with tab2:
            st.warning("**Dikkat:** Bu kodlar sadece spesifik hastalık frekanslarıdır. Enerji dengelemesi ve detoks içermez.")
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
                    özel sistem programlarıdır (4.00 Serisi). Genellikle <b>10-20 dakika</b> uygulanır.
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
