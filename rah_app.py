import streamlit as st
import pandas as pd
import os

# =============================================================================
# 1. GÖRSEL TASARIM (ULTIMATE CSS - LOGO & MOBİL & DARK MODE)
# =============================================================================
def local_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    /* --- 1. ZORUNLU AYDINLIK MOD --- */
    [data-testid="stAppViewContainer"] {
        background-color: #ffffff !important;
        font-family: 'Inter', sans-serif;
        color: #333333 !important;
    }
    h1, h2, h3, h4, h5, h6, p, div, span, label, li, button { color: #2c3e50; }

    /* --- 2. MOBİL LOGO VE BAŞLIK DÜZENİ --- */
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 15px;
    }
    
    .header-container {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        margin-bottom: 20px;
        border-bottom: 5px solid #e67e22;
        text-align: center;
    }
    .header-title {
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0;
        color: white !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    .header-subtitle {
        font-size: 0.9rem;
        color: #ecf0f1 !important;
        margin-top: 5px;
        opacity: 0.9;
        font-weight: 400;
    }

    /* MOBİL ÖZEL AYARLARI */
    @media only screen and (max-width: 600px) {
        .header-container { padding: 1rem !important; }
        .header-title { font-size: 1.5rem !important; }
        
        /* Seçim listesi mobilde yukarı kaçmasın */
        ul[data-baseweb="menu"] {
            max-height: 250px !important;
            overflow-y: auto !important;
        }
        /* Klavye açılınca içerik yukarı kayabilsin diye boşluk */
        .spacer-div { height: 200px; }
    }

    /* --- 3. CİHAZ SEÇİMİ --- */
    div[role="radiogroup"] {
        display: flex;
        flex-direction: row;
        justify-content: center;
        gap: 10px;
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #eee;
        margin-bottom: 20px;
    }
    div[role="radiogroup"] label {
        background-color: white;
        padding: 8px 20px;
        border-radius: 20px;
        border: 1px solid #ddd;
        cursor: pointer;
        transition: all 0.2s;
    }
    div[role="radiogroup"] label:hover {
        border-color: #e67e22;
        color: #e67e22 !important;
    }

    /* --- 4. GİRİŞ KUTULARI --- */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 2px solid #dce1e6 !important;
        color: #333 !important;
        border-radius: 8px;
    }
    div[data-baseweb="select"] span { color: #333 !important; }
    ul[data-baseweb="menu"] { background-color: #ffffff !important; border: 1px solid #eee !important; }
    li[role="option"] {
        color: #333 !important;
        background-color: #ffffff !important;
        border-bottom: 1px solid #f9f9f9;
        padding: 12px 15px !important;
    }
    li[role="option"]:hover, li[aria-selected="true"] {
        background-color: #fff3e0 !important;
        color: #d35400 !important;
        font-weight: bold;
    }
    
    /* --- 5. SEKMELER --- */
    .stTabs [data-baseweb="tab-list"] { gap: 4px; flex-wrap: wrap; }
    .stTabs [data-baseweb="tab"] {
        height: auto; min-height: 40px;
        background-color: #f1f2f6 !important;
        color: #57606f !important;
        border-radius: 6px 6px 0 0;
        font-weight: 600;
        border: 1px solid #e0e0e0; border-bottom: none;
        padding: 8px 10px;
        flex-grow: 1; text-align: center;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #e67e22 !important;
        border-top: 3px solid #e67e22 !important;
    }

    /* --- 6. KARTLAR VE TIMELINE --- */
    .disease-card { background: white; border: 1px solid #eee; border-left: 6px solid #e67e22; padding: 20px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .ulrich-card { background: #fff9db; border: 1px solid #f1c40f; padding: 15px; border-radius: 8px; color: #5d4037 !important; }
    .step-row { display: flex; flex-wrap: wrap; align-items: center; background: white; border: 1px solid #f0f0f0; margin-bottom: 8px; padding: 10px 15px; border-radius: 8px; }
    .code-pill { background: #2c3e50; color: #fff !important; font-family: monospace; font-weight: bold; padding: 5px 12px; border-radius: 5px; min-width: 80px; text-align: center; margin-right: 15px; }
    div[data-testid="stMetricValue"] { color: #d35400 !important; font-size: 1.6rem !important; }
    .tag { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: bold; color: white !important; margin-left: auto; }
    .bg-blue { background-color: #3498db; } .bg-green { background-color: #27ae60; } .bg-purple { background-color: #9b59b6; } .bg-red { background-color: #e74c3c; }

    /* GİZLEME */
    [data-testid="stSidebar"] { display: none; } 
    .stDeployButton, footer, header { visibility: hidden; }
    .custom-footer { margin-top: 50px; text-align: center; color: #95a5a6 !important; font-size: 0.8rem; border-top: 1px solid #eee; padding-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# 2. VERİTABANI (EKSİKSİZ: KANSER + KAYIP PROTOKOLLER DAHİL)
# =============================================================================
def get_rah_database():
    db = {
        # --- KRİTİK / YENİ EKLENENLER ---
        "Hücresel Dejenerasyon (Tümör Desteği)": {
            "source": "RAH Kompendium (C-Modülü)",
            "desc": "Hücresel bütünlüğü destekleme, bağışıklık aktivasyonu ve tümör eğilimi desteği. (Tıbbi tedaviye destektir).",
            "direct": ["19.00", "19.20", "99.00"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "19.00", "19.20", "99.00", "31.50", "31.60", "01.00"],
            "ulrich": [{"code": "4.14", "name": "Temizleme / Detoks"}, {"code": "4.03", "name": "Ozon / Radyasyon Koruma"}]
        },
        "Kemoterapi / Radyoterapi Yan Etkileri": {
            "source": "RAH + Wellbeing",
            "desc": "Ağır tedavi süreçlerinde vücudu temizleme ve güçlendirme.",
            "direct": ["31.50", "31.60", "22.90"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "31.50", "31.60", "31.61", "22.90", "48.10", "44.10", "35.10", "01.00"],
            "ulrich": [{"code": "4.14", "name": "Temizleme (Clearing)"}]
        },
        "Sigara Bırakma Destek": {
            "source": "RAH Syf 207 + Ulrich 4.14",
            "desc": "Nikotin bağımlılığı, yoksunluk belirtileri ve detoksifikasyon.",
            "direct": ["75.16", "75.17"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "75.16", "75.17", "48.10", "31.50", "01.00"],
            "ulrich": [{"code": "4.14", "name": "Temizleme (Clearing)"}]
        },
        "Anti-Aging (Gençleşme)": {
            "source": "Wellbeing Dosyası + RAH",
            "desc": "Hücresel yenilenme, cilt elastikiyeti ve vitalite artışı.",
            "direct": ["30.65", "31.38"],
            "compact": ["00.00", "01.00", "02.00", "30.65", "31.38", "62.10", "62.50", "64.00", "35.10", "31.50", "01.00"],
            "ulrich": [{"code": "4.06", "name": "Cilt / Saç / Tırnak"}]
        },
        "Selülit Tedavisi": {
            "source": "Wellbeing Dosyası",
            "desc": "Bağ dokusu sıkılaştırma, asidoz giderme ve lenf drenajı.",
            "direct": ["62.50", "36.00"],
            "compact": ["00.00", "01.00", "02.00", "31.52", "36.00", "37.10", "62.50", "50.00", "31.50", "01.00"],
            "ulrich": [{"code": "4.07", "name": "Asidoz"}, {"code": "4.14", "name": "Detoks"}]
        },
        "Otizm Spektrum Desteği": {
            "source": "RAH + Ulrich Kombinasyonu",
            "desc": "Ağır metal temizliği, bağırsak florası ve öğrenme desteği kombinasyonu.",
            "direct": ["31.60", "47.00", "54.00"],
            "compact": ["00.00", "01.00", "02.00", "31.60", "31.50", "47.00", "54.00", "35.10", "31.50", "01.00"],
            "ulrich": [{"code": "4.14", "name": "Temizleme / Detoks"}, {"code": "4.04", "name": "Öğrenme Programı"}]
        },
        "Sınav / İş Performansı": {
            "source": "Wellbeing + Ulrich 4.04",
            "desc": "Odaklanma, hafıza ve zihinsel performans artışı.",
            "direct": ["54.00", "35.20"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "54.00", "54.10", "35.20", "64.27", "83.80", "31.50", "01.00"],
            "ulrich": [{"code": "4.04", "name": "Öğrenme / Konsantrasyon"}]
        },
        "Duygusal Denge / İlişki Stresi": {
            "source": "Ulrich 4.15",
            "desc": "Duygusal yükler ve ilişki kaynaklı stres.",
            "direct": ["72.00"],
            "compact": ["00.00", "01.00", "02.00", "72.00", "72.05", "64.00", "31.10", "31.50", "01.00"],
            "ulrich": [{"code": "4.15", "name": "Partner / İlişki Stresi"}]
        },

        # --- ALFABETİK LİSTE (GERİ GETİRİLENLER DAHİL) ---
        "Adet Sancıları (Dismenore)": {"source": "RAH 65.40", "desc": "Ağrılı adet görme.", "direct": ["65.40"], "compact": ["00.00", "01.00", "02.00", "31.10", "64.00", "65.10", "65.40", "53.83", "31.50", "01.00"], "ulrich": [{"code": "4.08", "name": "Kadın Hormon Programı"}]},
        "Ağır Metal Detoksu": {"source": "RAH + Ulrich 4.14", "desc": "Ağır metal atılımı.", "direct": ["31.60", "31.50"], "compact": ["00.00", "01.00", "02.00", "31.10", "31.50", "31.60", "31.61", "09.34", "44.10", "48.10", "31.50", "01.00"], "ulrich": [{"code": "4.14", "name": "Temizleme"}]},
        "Alerji (Genel)": {"source": "RAH + Ulrich", "desc": "Alerjik reaksiyonlar.", "direct": ["35.20", "64.27"], "compact": ["00.00", "01.00", "02.00", "31.10", "34.00", "35.10", "35.20", "36.00", "64.27", "31.50", "01.00"], "ulrich": [{"code": "4.01", "name": "Alerji Programı"}]},
        "Alzheimer": {"source": "RAH + Ulrich", "desc": "Bellek ve kognitif destek.", "direct": ["55.30"], "compact": ["00.00", "01.00", "02.00", "31.34", "31.35", "35.10", "70.10", "38.10", "39.10", "50.10", "54.00", "55.30", "55.42", "72.00", "75.10", "31.50", "01.00"], "ulrich": [{"code": "4.04", "name": "Öğrenme"}]},
        "Anemi (Demir Eksikliği)": {"source": "RAH Syf 202", "desc": "Kansızlık.", "direct": ["33.24"], "compact": ["00.00", "01.00", "02.00", "07.21", "31.39", "35.10", "32.06", "32.10", "33.24", "33.60", "31.50", "01.00"]},
        "Anjin Pektoris": {"source": "RAH + Ulrich", "desc": "Göğüs ağrısı.", "direct": ["41.40"], "compact": ["00.00", "01.00", "02.00", "31.15", "35.10", "38.00", "40.00", "41.40", "41.50", "31.50", "01.00"], "ulrich": [{"code": "4.18", "name": "Kalp Programı"}]},
        "Artroz / Kireçlenme": {"source": "RAH + Ulrich", "desc": "Eklem dejenerasyonu.", "direct": ["53.53"], "compact": ["00.00", "01.00", "02.00", "31.40", "31.41", "35.10", "70.28", "52.00", "52.61", "52.62", "53.53", "53.54", "31.50", "01.00"], "ulrich": [{"code": "4.13", "name": "Fizik Sabitleri"}]},
        "Asidoz (Asitlenme)": {"source": "Ulrich 4.07", "desc": "Vücut pH dengesizliği.", "direct": ["31.53"], "compact": ["00.00", "01.00", "02.00", "31.10", "31.53", "06.00", "31.50", "01.00"], "ulrich": [{"code": "4.07", "name": "Asidoz Programı"}]},
        "Astım (Bronşiyal)": {"source": "RAH + Ulrich", "desc": "Solunum zorluğu.", "direct": ["43.20"], "compact": ["00.00", "01.00", "02.00", "31.11", "34.00", "35.10", "35.20", "70.16", "36.00", "42.60", "42.70", "43.10", "43.20", "43.30", "31.50", "01.00"], "ulrich": [{"code": "4.20", "name": "Astım Programı"}]},
        "Bağımlılık (Alkol/Madde)": {"source": "RAH + Ulrich", "desc": "Bağımlılık ve detoks.", "direct": ["75.17"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "48.10", "50.00", "54.10", "64.28", "64.29", "72.05", "75.10", "75.17", "31.50", "01.00"], "ulrich": [{"code": "4.14", "name": "Temizleme"}]},
        "Bağışıklık Güçlendirme": {"source": "RAH + Ulrich", "desc": "Genel direnç artırma.", "direct": ["35.10"], "compact": ["00.00", "01.00", "02.00", "31.10", "34.00", "35.10", "35.11", "36.50", "31.50", "01.00"], "ulrich": [{"code": "4.03", "name": "Ozon / Radyasyon"}, {"code": "90.56", "name": "Bağışıklık Sistemi"}]},
        "Baş Ağrısı": {"source": "RAH + Ulrich", "desc": "Genel baş ağrıları.", "direct": ["55.55"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.45", "54.10", "55.55", "72.05", "31.50", "01.00"], "ulrich": [{"code": "4.40", "name": "Baş Ağrısı"}]},
        "Bel Ağrısı (Lumbago)": {"source": "RAH + Ulrich", "desc": "Bel bölgesi ağrıları.", "direct": ["53.83"], "compact": ["00.00", "01.00", "02.00", "31.40", "35.10", "52.25", "53.23", "53.41", "53.73", "53.83", "31.50", "01.00"], "ulrich": [{"code": "4.21", "name": "Sırt Ağrısı"}]},
        "Borreliosis (Lyme)": {"source": "RAH + Ulrich", "desc": "Kene kaynaklı enfeksiyon.", "direct": ["24.10"], "compact": ["00.00", "01.00", "02.00", "24.00", "24.10", "31.10", "35.10", "72.00", "54.00", "53.52", "31.50", "01.00"], "ulrich": [{"code": "4.01", "name": "Alerji / Enfeksiyon"}]},
        "Bronşit (Akut)": {"source": "RAH Syf 132", "desc": "Akut öksürük.", "direct": ["43.13"], "compact": ["00.00", "01.00", "02.00", "31.11", "35.10", "70.17", "36.00", "42.60", "43.13", "43.30", "31.50", "01.00"]},
        "Bronşit (Kronik)": {"source": "RAH Syf 133", "desc": "Uzun süreli öksürük.", "direct": ["43.14"], "compact": ["00.00", "01.00", "02.00", "31.11", "35.10", "70.17", "36.00", "42.60", "43.14", "43.30", "31.50", "01.00"]},
        "Böbrek Taşı": {"source": "RAH Syf 140", "desc": "Nefrolityaz.", "direct": ["45.25"], "compact": ["00.00", "01.00", "02.00", "31.23", "35.10", "44.00", "44.21", "39.65", "45.25", "31.50", "01.00"]},
        "Böbrek Yetmezliği": {"source": "RAH Syf 137", "desc": "Böbrek fonksiyon yetersizliği.", "direct": ["45.05"], "compact": ["00.00", "01.00", "02.00", "31.23", "31.87", "35.10", "44.10", "44.17", "70.21", "45.05", "45.80", "31.50", "01.00"]},
        "Cilt Mantarı": {"source": "RAH + Ulrich", "desc": "Mikoz enfeksiyonları.", "direct": ["63.50"], "compact": ["00.00", "01.00", "02.00", "30.65", "31.38", "35.10", "70.24", "62.10", "63.50", "31.50", "01.00"], "ulrich": [{"code": "4.05", "name": "Mantar Programı"}]},
        "Cilt Sorunları (Akne)": {"source": "RAH + Ulrich", "desc": "Genel cilt problemleri.", "direct": ["63.10"], "compact": ["00.00", "01.00", "02.00", "31.38", "30.65", "35.10", "70.24", "62.10", "63.10", "63.20", "31.50", "01.00"], "ulrich": [{"code": "4.06", "name": "Cilt / Saç"}]},
        "Covid-19 / Long-Covid": {"source": "RAH Syf 137", "desc": "Viral enfeksiyon sonrası.", "direct": ["43.52"], "compact": ["00.00", "01.00", "02.00", "31.11", "35.10", "22.93", "70.17", "42.70", "43.10", "43.30", "43.50", "43.52", "31.50", "01.00"], "ulrich": [{"code": "90.48", "name": "Enfeksiyon Desteği"}]},
        "Crohn Hastalığı": {"source": "RAH Syf 146", "desc": "İnflamatuar bağırsak hastalığı.", "direct": ["47.50"], "compact": ["00.00", "01.00", "02.00", "31.12", "31.16", "31.70", "35.10", "70.19", "46.00", "47.50", "64.55", "72.00", "31.50", "01.00"]},
        "Çakra Dengeleme": {"source": "Ulrich 4.13", "desc": "Enerji merkezleri.", "direct": ["01.40"], "compact": ["00.00", "01.00", "01.40", "01.41", "01.42", "01.43", "01.44", "01.45", "01.46", "01.47", "31.50", "01.00"], "ulrich": [{"code": "4.13", "name": "Fizik Sabitleri / Çakra"}]},
        "DEHB (Dikkat Eksikliği)": {"source": "RAH + Ulrich", "desc": "Konsantrasyon ve öğrenme güçlüğü.", "direct": ["55.45"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "35.20", "70.10", "54.00", "54.10", "55.45", "64.27", "83.80", "72.00", "31.50", "01.00"], "ulrich": [{"code": "4.04", "name": "Öğrenme Programı"}]},
        "Depresyon": {"source": "RAH + Ulrich", "desc": "Ruhsal çöküntü.", "direct": ["72.10"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "48.10", "64.10", "64.28", "64.29", "72.10", "75.10", "31.50", "01.00"], "ulrich": [{"code": "4.16", "name": "Kundalini"}, {"code": "90.58", "name": "Depresyon"}]},
        "Diş Eti İltihabı": {"source": "RAH + Ulrich", "desc": "Diş eti ve çene sorunları.", "direct": ["46.20"], "compact": ["00.00", "01.00", "02.00", "31.39", "46.00", "46.10", "46.20", "35.10", "31.50", "01.00"], "ulrich": [{"code": "4.11", "name": "Diş / Çene"}]},
        "Diyabet (Şeker Hastalığı)": {"source": "RAH + Ulrich", "desc": "Metabolizma desteği.", "direct": ["51.40"], "compact": ["00.00", "01.00", "02.00", "31.14", "35.10", "70.20", "48.35", "50.20", "51.20", "51.40", "64.70", "31.50", "01.00"], "ulrich": [{"code": "4.19", "name": "Diyabet Programı"}]},
        "Dolaşım Bozukluğu": {"source": "RAH + Ulrich", "desc": "Soğuk el/ayak.", "direct": ["39.10"], "compact": ["00.00", "01.00", "02.00", "31.39", "35.10", "38.00", "38.10", "39.10", "31.50", "01.00"], "ulrich": [{"code": "4.18", "name": "Kalp / Dolaşım"}]},
        "Elektrosmog / Radyasyon": {"source": "Ulrich + RAH", "desc": "Elektromanyetik alan yüklemesi.", "direct": ["22.00"], "compact": ["00.00", "01.00", "02.00", "22.00", "22.10", "22.90", "31.10", "31.50", "01.00"], "ulrich": [{"code": "4.03", "name": "Ozon / Radyasyon"}]},
        "Endometriozis": {"source": "RAH Syf 199", "desc": "Rahim içi doku büyümesi.", "direct": ["67.30"], "compact": ["00.00", "01.00", "02.00", "31.20", "31.22", "31.81", "35.10", "70.22", "36.10", "64.80", "65.10", "65.30", "65.31", "65.50", "66.00", "67.30", "72.00", "75.00", "31.50", "01.00"]},
        "Epstein Barr Virüsü (EBV)": {"source": "RAH Syf 95", "desc": "Kronik yorgunluk ve viral yük.", "direct": ["16.20"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "16.00", "16.20", "48.10", "36.00", "31.50", "01.00"]},
        "Fibromiyalji": {"source": "RAH + Ulrich", "desc": "Yaygın kas ağrıları.", "direct": ["53.84"], "compact": ["00.00", "01.00", "02.00", "31.38", "31.40", "35.10", "70.26", "70.27", "36.00", "52.00", "53.23", "53.25", "53.28", "53.62", "53.84", "62.10", "64.00", "31.50", "01.00"], "ulrich": [{"code": "4.13", "name": "Fizik Sabitleri"}]},
        "Fruktoz İntoleransı": {"source": "RAH Syf 121", "desc": "Sindirim bozukluğu.", "direct": ["35.30"], "compact": ["00.00", "01.00", "02.00", "09.34", "31.10", "34.00", "35.10", "35.30", "46.40", "46.50", "47.70", "31.50", "01.00"]},
        "Gastrit / Mide Yanması": {"source": "RAH + Ulrich", "desc": "Mide iltihabı ve reflü.", "direct": ["47.20"], "compact": ["00.00", "01.00", "02.00", "31.13", "35.10", "70.19", "46.30", "47.20", "47.10", "31.50", "01.00"], "ulrich": [{"code": "4.07", "name": "Asidoz / Mide"}]},
        "Glokom": {"source": "RAH Syf 176", "desc": "Göz tansiyonu.", "direct": ["57.30"], "compact": ["00.00", "01.00", "02.00", "31.31", "35.10", "70.12", "56.00", "56.60", "57.10", "57.30", "31.50", "01.00"]},
        "Göz Kuruluğu": {"source": "RAH Syf 178", "desc": "Gözyaşı kanalı sorunları.", "direct": ["57.53"], "compact": ["00.00", "01.00", "02.00", "31.31", "35.10", "70.12", "56.00", "57.53", "31.50", "01.00"]},
        "Grip / Enfeksiyon": {"source": "RAH + Ulrich", "desc": "Viral enfeksiyonlar.", "direct": ["70.46"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.46", "36.00", "42.10", "43.11", "31.50", "01.00"], "ulrich": [{"code": "4.01", "name": "Alerji/Enfeksiyon"}]},
        "Gut Hastalığı": {"source": "RAH + Ulrich", "desc": "Ürik asit birikimi.", "direct": ["51.50"], "compact": ["00.00", "01.00", "02.00", "30.70", "31.10", "35.10", "50.00", "51.10", "51.50", "52.60", "71.11", "71.50", "31.50", "01.00"], "ulrich": [{"code": "4.07", "name": "Asidoz"}]},
        "Herpes (Uçuk)": {"source": "RAH + Ulrich", "desc": "Herpes Simplex.", "direct": ["16.50"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "16.50", "16.51", "63.55", "31.50", "01.00"], "ulrich": [{"code": "4.01", "name": "Enfeksiyon"}]},
        "Hormonal Denge (Kadın)": {"source": "RAH + Ulrich", "desc": "Genel hormon düzenleme.", "direct": ["65.10"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.22", "64.00", "65.10", "31.50", "01.00"], "ulrich": [{"code": "4.08", "name": "Kadın Hormonları"}]},
        "Hormonal Denge (Erkek)": {"source": "RAH + Ulrich", "desc": "Genel hormon düzenleme.", "direct": ["65.20"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.23", "64.00", "65.20", "31.50", "01.00"], "ulrich": [{"code": "4.09", "name": "Erkek Hormon Programı"}]},
        "Kabızlık": {"source": "RAH Syf 148", "desc": "Bağırsak hareketliliği.", "direct": ["47.86"], "compact": ["00.00", "01.00", "02.00", "31.12", "31.16", "35.10", "70.19", "46.00", "47.86", "31.50", "01.00"]},
        "Karaciğer Detoks": {"source": "RAH + Ulrich", "desc": "Karaciğer temizliği.", "direct": ["48.10"], "compact": ["00.00", "01.00", "02.00", "31.29", "35.10", "70.20", "48.10", "49.10", "31.60", "31.50", "01.00"], "ulrich": [{"code": "4.14", "name": "Temizleme / Detoks"}]},
        "Katarakt": {"source": "RAH Syf 176", "desc": "Göz merceği bulanıklığı.", "direct": ["57.20"], "compact": ["00.00", "01.00", "02.00", "31.31", "35.10", "70.12", "56.00", "56.40", "57.20", "31.50", "01.00"]},
        "Kemik Kırığı": {"source": "RAH Syf 155", "desc": "Kırık iyileşmesi.", "direct": ["53.11"], "compact": ["00.00", "01.00", "02.00", "31.39", "31.41", "35.10", "70.51", "52.00", "53.11", "31.50", "01.00"]},
        "Kilo Verme": {"source": "RAH + Ulrich", "desc": "Metabolizma hızlandırma.", "direct": ["75.15"], "compact": ["00.00", "01.00", "02.00", "09.00", "31.10", "36.00", "38.00", "44.00", "46.40", "48.10", "50.00", "64.00", "75.10", "75.15", "31.50", "01.00"], "ulrich": [{"code": "4.19", "name": "Diyabet / Metabolizma"}]},
        "Kronik Yorgunluk (CFS)": {"source": "RAH + Ulrich", "desc": "Sürekli yorgunluk.", "direct": ["16.20"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "16.20", "48.10", "70.10", "31.50", "01.00"], "ulrich": [{"code": "4.16", "name": "Kundalini"}]},
        "Menopoz": {"source": "RAH + Ulrich", "desc": "Klimakterik şikayetler.", "direct": ["65.60"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.22", "64.10", "64.20", "65.10", "65.60", "66.00", "72.00", "75.00", "31.50", "01.00"], "ulrich": [{"code": "4.08", "name": "Kadın Hormonları"}]},
        "Migren": {"source": "RAH + Ulrich", "desc": "Şiddetli baş ağrısı.", "direct": ["55.60"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.45", "38.10", "39.10", "39.40", "54.10", "54.25", "55.55", "55.60", "64.00", "72.05", "31.50", "01.00"], "ulrich": [{"code": "4.40", "name": "Baş Ağrısı/Migren"}]},
        "Operasyon Sonrası Bakım": {"source": "Dr. Ulrich 4.10", "desc": "Cerrahi sonrası iyileşme.", "direct": ["70.63"], "compact": ["00.00", "01.00", "31.80", "31.81", "31.82", "70.63", "35.10", "31.50", "01.00"], "ulrich": [{"code": "4.10", "name": "Op. Sonrası Bakım"}]},
        "Osteoporoz": {"source": "RAH + Ulrich", "desc": "Kemik erimesi.", "direct": ["53.80"], "compact": ["00.00", "01.00", "02.00", "31.41", "35.10", "50.00", "52.00", "52.05", "53.80", "64.00", "64.81", "31.50", "01.00"], "ulrich": [{"code": "4.13", "name": "Fizik Sabitleri"}]},
        "Panik Atak": {"source": "RAH + Ulrich", "desc": "Ani korku nöbetleri.", "direct": ["72.05"], "compact": ["00.00", "01.00", "02.00", "31.10", "72.05", "75.10", "54.00", "64.10", "31.50", "01.00"], "ulrich": [{"code": "4.02", "name": "Stres Programı"}]},
        "Parkinson": {"source": "RAH + Ulrich", "desc": "Titreme ve hareket bozukluğu.", "direct": ["55.31"], "compact": ["00.00", "01.00", "02.00", "31.34", "31.35", "35.10", "70.68", "38.10", "54.00", "55.31", "64.28", "72.00", "75.10", "31.50", "01.00"], "ulrich": [{"code": "4.17", "name": "Parkinson Programı"}]},
        "Prostat Sorunları": {"source": "RAH + Ulrich", "desc": "Prostatit ve büyüme.", "direct": ["69.30"], "compact": ["00.00", "01.00", "02.00", "31.18", "35.10", "70.23", "68.26", "69.10", "69.30", "31.50", "01.00"], "ulrich": [{"code": "4.09", "name": "Erkek Hormonları"}]},
        "Radyasyon / 5G Koruma": {"source": "Ulrich + RAH", "desc": "Elektrosmog detoksu.", "direct": ["22.00"], "compact": ["00.00", "01.00", "02.00", "22.00", "22.10", "22.90", "31.10", "31.50", "01.00"], "ulrich": [{"code": "4.03", "name": "Ozon / Radyasyon Koruma"}]},
        "Romatizma / Artrit": {"source": "RAH + Ulrich", "desc": "Eklem iltihabı ve ağrıları.", "direct": ["53.52"], "compact": ["00.00", "01.00", "02.00", "31.40", "31.41", "35.10", "70.28", "52.00", "53.52", "53.53", "53.54", "31.50", "01.00"], "ulrich": [{"code": "4.13", "name": "Fizik Sabitleri"}]},
        "Sedef (Psoriasis)": {"source": "RAH + Ulrich", "desc": "Cilt pullanması.", "direct": ["63.10"], "compact": ["00.00", "01.00", "02.00", "31.38", "30.65", "35.10", "70.24", "62.10", "62.20", "62.60", "63.10", "72.00", "75.00", "31.50", "01.00"], "ulrich": [{"code": "4.06", "name": "Cilt / Saç"}]},
        "Sırt Ağrısı": {"source": "RAH + Ulrich", "desc": "Omurga kaynaklı ağrılar.", "direct": ["53.70"], "compact": ["00.00", "01.00", "02.00", "31.40", "35.10", "71.11", "71.50", "52.00", "52.20", "53.23", "53.25", "53.41", "53.70", "72.05", "75.10", "31.50", "01.00"], "ulrich": [{"code": "4.21", "name": "Sırt Ağrısı / Omurga"}]},
        "Spor Yaralanmaları": {"source": "RAH + Ulrich", "desc": "Burkulma, ezilme, travma.", "direct": ["53.21"], "compact": ["00.00", "01.00", "02.00", "31.39", "31.40", "35.10", "53.21", "53.22", "53.24", "31.50", "01.00"], "ulrich": [{"code": "4.22", "name": "Skar / Yara İzi"}]},
        "Stres / Tükenmişlik": {"source": "RAH + Ulrich", "desc": "Sinirsel gerginlik ve rahatlama.", "direct": ["75.10"], "compact": ["00.00", "01.00", "02.00", "31.10", "48.10", "50.00", "64.05", "64.10", "64.20", "64.28", "64.29", "64.30", "64.35", "64.40", "64.50", "72.05", "75.10", "31.50", "01.00"], "ulrich": [{"code": "4.02", "name": "Stres Programı"}, {"code": "4.15", "name": "İlişki Stresi"}, {"code": "4.16", "name": "Kundalini Stresi"}]},
        "Tinnitus (Çınlama)": {"source": "RAH + Ulrich", "desc": "Kulak çınlaması.", "direct": ["59.10"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.15", "38.10", "39.10", "58.30", "58.40", "59.10", "59.40", "72.00", "75.00", "31.50", "01.00"], "ulrich": [{"code": "4.12", "name": "Tinnitus Programı"}]},
        "Tiroid (Dengesizlik)": {"source": "RAH + Ulrich", "desc": "Hipotiroidi veya Hipertiroidi.", "direct": ["65.33", "65.34"], "compact": ["00.00", "01.00", "02.00", "31.33", "35.10", "70.54", "64.10", "64.20", "64.30", "65.30", "31.50", "01.00"], "ulrich": [{"code": "4.08", "name": "Hormon Programı"}]},
        "Uyku Bozukluğu": {"source": "RAH + Ulrich", "desc": "Uykuya dalma ve sürdürme.", "direct": ["55.10", "55.20"], "compact": ["00.00", "01.00", "02.21", "31.10", "35.10", "70.10", "54.00", "55.10", "64.11", "65.30", "72.00", "75.10", "31.50", "01.00"], "ulrich": [{"code": "4.02", "name": "Stres (Uyku Öncesi)"}]},
        "Vertigo (Baş Dönmesi)": {"source": "RAH + Ulrich", "desc": "Denge kaybı.", "direct": ["55.53"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "54.00", "55.53", "39.10", "31.50", "01.00"], "ulrich": [{"code": "4.02", "name": "Stres / Denge"}]},
        "Yara İzi (Skar) Tedavisi": {"source": "Ulrich + RAH", "desc": "Yara izi dokusunun temizlenmesi.", "direct": ["31.81"], "compact": ["00.00", "01.00", "02.00", "31.10", "31.81", "31.80", "70.24", "31.50", "01.00"], "ulrich": [{"code": "4.22", "name": "Skar / Yara İzi"}]},
        "Yüksek Tansiyon": {"source": "RAH + Ulrich", "desc": "Hipertansiyon.", "direct": ["39.60"], "compact": ["00.00", "01.00", "02.00", "31.39", "35.10", "70.47", "38.00", "39.10", "39.40", "39.50", "39.60", "64.00", "31.50", "01.00"], "ulrich": [{"code": "4.18", "name": "Kalp Programı"}]}
    }
    return db

def get_program_name(code):
    names = {
        "00.00": "Analiz Hazırlığı", "01.00": "Vitalizasyon Komple", "01.10": "Enerji Yükleme", "01.30": "Ön Kontrol", "01.40": "Çakralar Komple",
        "02.00": "Akupunktur Meridyenleri", "07.21": "Demir Metabolizması",
        "19.00": "Hücresel Bütünlük", "19.20": "Hücresel Dejenerasyon", "99.00": "Tümör Desteği",
        "22.00": "Elektrosmog", "22.90": "Radyasyon Yükü", "24.10": "Borreliosis",
        "31.10": "ATP Üretimi", "31.50": "Temel Detoks", "31.51": "Detoks Kan", "31.52": "Detoks Lenf", "31.60": "Detoks Karaciğer", "31.61": "Ağır Metal Detoksu", "31.81": "Yara İzi Tedavisi",
        "35.10": "Bağışıklık Artırma", "35.20": "Alerji Temel",
        "70.45": "Migren Patojen", "70.47": "Tansiyon Düşürme", "75.16": "Sigara Bırakma", "75.17": "Yoksunluk Belirtileri"
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
        st.write("") # Boş sidebar

    # --- HEADER (LOGO + BAŞLIK) ---
    # Logoyu kodun içine dahil ettik (Layout ile)
    c1, c2 = st.columns([1, 5])
    with c1:
        try:
            if os.path.exists("drsaitlogo.jpeg"):
                st.image("drsaitlogo.jpeg", width=90)
        except:
            pass
    with c2:
        st.markdown("""
        <div class="header-container" style="margin-top:0; padding-top:1rem;">
            <div class="header-title">🧬 RAH Asistanı</div>
            <div class="header-subtitle">Dr. Sait SEVİNÇ</div>
        </div>
        """, unsafe_allow_html=True)
    
    # --- CİHAZ SEÇİMİ ---
    st.write("") 
    device_main = st.radio("Lütfen Cihazınızı Seçiniz:", ["Rayocomp PS 10", "Rayocomp PS 1000"], horizontal=True)
    
    if device_main == "Rayocomp PS 10":
        st.info("ℹ️ **PS 10:** Kodları sırasıyla manuel girin veya Green Card kullanın.")
    else:
        st.success("✅ **PS 1000:** Menüden otomatik seçebilirsiniz.")

    db = get_rah_database()
    
    # Arama Kutusu
    st.markdown('<h3 style="color:#2c3e50; margin-bottom:10px;">🔎 Rahatsızlık Seçimi</h3>', unsafe_allow_html=True)
    disease_list = sorted(db.keys())
    selected_disease = st.selectbox("Listeden seçim yapınız:", [""] + disease_list, label_visibility="collapsed")
    st.markdown('<div class="spacer-div"></div>', unsafe_allow_html=True) # Mobil için boşluk

    if selected_disease:
        data = db[selected_disease]
        
        # Bilgi Kartı
        st.markdown(f"""
        <div class="disease-card">
            <h2>📌 {selected_disease}</h2>
            <p style="font-size: 1.1rem; color: #555;">{data['desc']}</p>
            <div style="margin-top: 15px; font-size: 0.85rem; color: #888;">
                📚 <b>Kaynak:</b> {data['source']}
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
                    <b>ℹ️ Dr. Elmar Ulrich Modülü (M4):</b> Bu programlar özel sistem kartları veya 90.00 serisi içindedir (4.00 - 4.22).
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
