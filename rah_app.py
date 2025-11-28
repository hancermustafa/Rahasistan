import streamlit as st
import pandas as pd
import os
import urllib.parse

# =============================================================================
# 1. GÖRSEL TASARIM (LAYOUT FIX & PREMIUM CSS)
# =============================================================================
def local_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800&display=swap');
    
    /* --- ANA GÖVDE --- */
    [data-testid="stAppViewContainer"] {
        background-color: #ffffff !important;
        font-family: 'Inter', sans-serif;
        color: #333333 !important;
    }
    h1, h2, h3, h4, h5, h6, p, div, span, label, li, button { color: #2c3e50; }

    /* --- SÜTUN DARALMA SORUNU ÇÖZÜMÜ (WIDTH 100%) --- */
    .step-row {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        background: white;
        border: 1px solid #f0f0f0;
        margin-bottom: 8px;
        padding: 12px 15px;
        border-radius: 8px;
        width: 100% !important; /* EKRANA TAM OTURMASI İÇİN */
        box-sizing: border-box;
    }
    
    /* --- HEADER --- */
    .header-container {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border-bottom: 4px solid #e67e22;
        text-align: center;
    }
    .header-title { font-size: 1.8rem; font-weight: 800; margin: 0; color: white !important; text-shadow: 1px 1px 2px rgba(0,0,0,0.2); }
    .header-subtitle { font-size: 0.9rem; color: #ecf0f1 !important; margin-top: 5px; opacity: 0.9; }

    /* --- GİRİŞ KUTULARI (SİYAH EKRAN FIX) --- */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important; border: 2px solid #dce1e6 !important; color: #333 !important; border-radius: 8px;
    }
    div[data-baseweb="select"] span { color: #333 !important; }
    ul[data-baseweb="menu"] { background-color: #ffffff !important; border: 1px solid #eee !important; }
    li[role="option"] { color: #333 !important; background-color: #ffffff !important; border-bottom: 1px solid #f9f9f9; }
    li[role="option"]:hover { background-color: #fff3e0 !important; color: #d35400 !important; font-weight: bold; }

    /* --- AI SOHBET KUTUSU FIX --- */
    .stChatInput input { color: #333 !important; background-color: white !important; }
    [data-testid="stChatMessage"] { background-color: #f8f9fa !important; color: #333 !important; border: 1px solid #eee; }

    /* --- DİĞER BİLEŞENLER --- */
    .whatsapp-btn {
        display: block; background-color: #25D366; color: white !important; padding: 12px; border-radius: 8px;
        text-decoration: none; font-weight: bold; text-align: center; margin-top: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    div[role="radiogroup"] {
        display: flex; flex-direction: row; justify-content: center; gap: 10px; background-color: #f8f9fa;
        padding: 10px; border-radius: 10px; border: 1px solid #eee; margin-bottom: 20px;
    }
    .code-pill {
        background: #2c3e50; color: #fff !important; font-family: monospace; font-weight: bold;
        padding: 5px 12px; border-radius: 5px; min-width: 80px; text-align: center; margin-right: 15px;
    }
    
    /* MOBİL AYARLARI */
    @media only screen and (max-width: 600px) {
        .header-container { padding: 1rem !important; }
        .header-title { font-size: 1.4rem !important; }
        ul[data-baseweb="menu"] { max-height: 250px !important; overflow-y: auto !important; }
        div[data-baseweb="select"] { margin-bottom: 20px !important; }
        .spacer-div { height: 200px; }
    }

    [data-testid="stSidebar"] { display: none; } 
    .stDeployButton, footer, header { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# 2. VERİTABANI (EKLEMELERLE GÜÇLENDİRİLMİŞ TAM LİSTE)
# =============================================================================
def get_rah_database():
    db = {
        # --- YENİ EKLENENLER (DİP ARAŞTIRMA) ---
        "Candida Albicans (Mantar)": {
            "source": "RAH 47.82 + Ulrich 4.05",
            "desc": "Bağırsak ve sistemik mantar enfeksiyonu.",
            "direct": ["47.82"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "47.00", "47.82", "63.50", "31.50", "01.00"],
            "ulrich": [{"code": "4.05", "name": "Mantar Programı"}]
        },
        "Helicobacter Pylori": {
            "source": "RAH 47.22",
            "desc": "Mide bakterisi ve ülser tetikleyicisi.",
            "direct": ["47.22"],
            "compact": ["00.00", "01.00", "02.00", "31.13", "35.10", "47.20", "47.22", "70.19", "31.50", "01.00"],
            "ulrich": [{"code": "4.07", "name": "Asidoz / Mide"}]
        },
        "Kolesterol (Yüksek)": {
            "source": "RAH 50.35 + Ulrich 4.19",
            "desc": "Lipid metabolizması bozukluğu.",
            "direct": ["50.35"],
            "compact": ["00.00", "01.00", "02.00", "31.14", "48.10", "50.00", "50.35", "39.15", "31.50", "01.00"],
            "ulrich": [{"code": "4.19", "name": "Metabolizma"}]
        },
        "Uyku Apnesi": {
            "source": "RAH 42.50",
            "desc": "Uyku sırasında solunum durması.",
            "direct": ["42.50"],
            "compact": ["00.00", "01.00", "02.00", "31.11", "42.00", "42.50", "42.60", "54.00", "31.50", "01.00"],
            "ulrich": [{"code": "4.20", "name": "Astım / Solunum"}]
        },

        # --- MEVCUT TAM LİSTE ---
        "Hücresel Dejenerasyon (Tümör Desteği)": {"source": "RAH C-Modülü", "desc": "Hücresel destek ve bağışıklık.", "direct": ["19.00", "19.20", "99.00"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "19.00", "19.20", "99.00", "31.50", "31.60", "01.00"], "ulrich": [{"code": "4.14", "name": "Temizleme / Detoks"}, {"code": "4.03", "name": "Ozon / Radyasyon"}]},
        "Kemoterapi Yan Etkileri": {"source": "RAH + Wellbeing", "desc": "Tedavi sonrası temizleme.", "direct": ["31.50", "31.60"], "compact": ["00.00", "01.00", "02.00", "31.10", "31.50", "31.60", "31.61", "22.90", "48.10", "44.10", "35.10", "01.00"], "ulrich": [{"code": "4.14", "name": "Temizleme"}]},
        "Sigara Bırakma Destek": {"source": "RAH Syf 207", "desc": "Nikotin detoksu.", "direct": ["75.16"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "75.16", "75.17", "48.10", "31.50", "01.00"], "ulrich": [{"code": "4.14", "name": "Temizleme"}]},
        "Anti-Aging": {"source": "Wellbeing", "desc": "Hücresel yenilenme.", "direct": ["30.65"], "compact": ["00.00", "01.00", "02.00", "30.65", "31.38", "62.10", "62.50", "64.00", "35.10", "31.50", "01.00"], "ulrich": [{"code": "4.06", "name": "Cilt / Saç"}]},
        "Selülit Tedavisi": {"source": "Wellbeing", "desc": "Bağ dokusu.", "direct": ["62.50"], "compact": ["00.00", "01.00", "02.00", "31.52", "36.00", "37.10", "62.50", "50.00", "31.50", "01.00"], "ulrich": [{"code": "4.07", "name": "Asidoz"}, {"code": "4.14", "name": "Detoks"}]},
        "Otizm Spektrum Desteği": {"source": "RAH + Ulrich", "desc": "Detoks ve öğrenme.", "direct": ["31.60", "47.00"], "compact": ["00.00", "01.00", "02.00", "31.60", "31.50", "47.00", "54.00", "35.10", "31.50", "01.00"], "ulrich": [{"code": "4.14", "name": "Temizleme"}, {"code": "4.04", "name": "Öğrenme"}]},
        "Ağır Metal Detoksu": {"source": "RAH + Ulrich", "desc": "Ağır metal atılımı.", "direct": ["31.60"], "compact": ["00.00", "01.00", "02.00", "31.10", "31.50", "31.60", "31.61", "09.34", "44.10", "48.10", "31.50", "01.00"], "ulrich": [{"code": "4.14", "name": "Temizleme"}]},
        "Alerji (Genel)": {"source": "RAH + Ulrich", "desc": "Alerjik reaksiyonlar.", "direct": ["35.20"], "compact": ["00.00", "01.00", "02.00", "31.10", "34.00", "35.10", "35.20", "36.00", "64.27", "31.50", "01.00"], "ulrich": [{"code": "4.01", "name": "Alerji"}]},
        "Alzheimer": {"source": "RAH + Ulrich", "desc": "Bellek desteği.", "direct": ["55.30"], "compact": ["00.00", "01.00", "02.00", "31.34", "31.35", "35.10", "70.10", "55.30", "31.50", "01.00"], "ulrich": [{"code": "4.04", "name": "Öğrenme"}]},
        "Anemi (Demir)": {"source": "RAH", "desc": "Kansızlık.", "direct": ["33.24"], "compact": ["00.00", "01.00", "02.00", "07.21", "31.39", "33.24", "31.50", "01.00"], "ulrich": [{"code": "4.18", "name": "Kalp/Dolaşım"}]},
        "Anjin Pektoris": {"source": "RAH + Ulrich", "desc": "Göğüs ağrısı.", "direct": ["41.40"], "compact": ["00.00", "01.00", "02.00", "31.15", "35.10", "41.40", "31.50", "01.00"], "ulrich": [{"code": "4.18", "name": "Kalp"}]},
        "Artroz / Kireçlenme": {"source": "RAH + Ulrich", "desc": "Eklem dejenerasyonu.", "direct": ["53.53"], "compact": ["00.00", "01.00", "02.00", "31.40", "31.41", "35.10", "53.53", "31.50", "01.00"], "ulrich": [{"code": "4.13", "name": "Fizik Sabitleri"}]},
        "Asidoz (Asitlenme)": {"source": "Ulrich", "desc": "pH dengesi.", "direct": ["31.53"], "compact": ["00.00", "01.00", "02.00", "31.10", "31.53", "06.00", "31.50", "01.00"], "ulrich": [{"code": "4.07", "name": "Asidoz"}]},
        "Astım (Bronşiyal)": {"source": "RAH + Ulrich", "desc": "Solunum zorluğu.", "direct": ["43.20"], "compact": ["00.00", "01.00", "02.00", "31.11", "35.10", "43.20", "31.50", "01.00"], "ulrich": [{"code": "4.20", "name": "Astım"}]},
        "Baş Ağrısı": {"source": "RAH + Ulrich", "desc": "Genel baş ağrısı.", "direct": ["55.55"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "55.55", "31.50", "01.00"], "ulrich": [{"code": "4.40", "name": "Baş Ağrısı"}]},
        "Bel Ağrısı": {"source": "RAH + Ulrich", "desc": "Lumbago.", "direct": ["53.83"], "compact": ["00.00", "01.00", "02.00", "31.40", "35.10", "53.83", "31.50", "01.00"], "ulrich": [{"code": "4.21", "name": "Sırt Ağrısı"}]},
        "Bronşit (Akut)": {"source": "RAH", "desc": "Öksürük.", "direct": ["43.13"], "compact": ["00.00", "01.00", "02.00", "31.11", "35.10", "43.13", "31.50", "01.00"], "ulrich": [{"code": "4.20", "name": "Astım/Solunum"}]},
        "Cilt Mantarı": {"source": "RAH + Ulrich", "desc": "Mikoz.", "direct": ["63.50"], "compact": ["00.00", "01.00", "02.00", "30.65", "63.50", "31.50", "01.00"], "ulrich": [{"code": "4.05", "name": "Mantar"}]},
        "Covid-19 / Long-Covid": {"source": "RAH", "desc": "Viral sonrası.", "direct": ["43.52"], "compact": ["00.00", "01.00", "02.00", "31.11", "35.10", "43.52", "31.50", "01.00"], "ulrich": [{"code": "90.48", "name": "Enfeksiyon"}]},
        "Depresyon": {"source": "RAH + Ulrich", "desc": "Ruhsal denge.", "direct": ["72.10"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "72.10", "31.50", "01.00"], "ulrich": [{"code": "90.58", "name": "Depresyon"}]},
        "Diyabet": {"source": "RAH + Ulrich", "desc": "Şeker hastalığı.", "direct": ["51.40"], "compact": ["00.00", "01.00", "02.00", "31.14", "35.10", "51.40", "31.50", "01.00"], "ulrich": [{"code": "4.19", "name": "Diyabet"}]},
        "Dolaşım Bozukluğu": {"source": "RAH + Ulrich", "desc": "Soğuk el/ayak.", "direct": ["39.10"], "compact": ["00.00", "01.00", "02.00", "31.39", "39.10", "31.50", "01.00"], "ulrich": [{"code": "4.18", "name": "Dolaşım"}]},
        "Düşük Tansiyon": {"source": "RAH + Ulrich", "desc": "Hipotansiyon.", "direct": ["39.70"], "compact": ["00.00", "01.00", "02.00", "31.39", "39.70", "31.50", "01.00"], "ulrich": [{"code": "4.18", "name": "Kalp/Dolaşım"}]},
        "Fibromiyalji": {"source": "RAH + Ulrich", "desc": "Yaygın ağrı.", "direct": ["53.84"], "compact": ["00.00", "01.00", "02.00", "31.38", "31.40", "53.84", "31.50", "01.00"], "ulrich": [{"code": "4.13", "name": "Fizik Sabitleri"}]},
        "Gastrit": {"source": "RAH + Ulrich", "desc": "Mide yanması.", "direct": ["47.20"], "compact": ["00.00", "01.00", "02.00", "31.13", "47.20", "31.50", "01.00"], "ulrich": [{"code": "4.07", "name": "Asidoz"}]},
        "Grip / Enfeksiyon": {"source": "RAH + Ulrich", "desc": "Viral enfeksiyon.", "direct": ["70.46"], "compact": ["00.00", "01.00", "02.00", "31.10", "70.46", "31.50", "01.00"], "ulrich": [{"code": "4.01", "name": "Enfeksiyon"}]},
        "Gut": {"source": "RAH + Ulrich", "desc": "Ürik asit.", "direct": ["51.50"], "compact": ["00.00", "01.00", "02.00", "30.70", "51.50", "31.50", "01.00"], "ulrich": [{"code": "4.07", "name": "Asidoz"}]},
        "Hemoroid": {"source": "RAH", "desc": "Rektal varis.", "direct": ["47.88"], "compact": ["00.00", "01.00", "02.00", "31.39", "47.88", "31.50", "01.00"], "ulrich": [{"code": "4.18", "name": "Dolaşım"}]},
        "Herpes": {"source": "RAH + Ulrich", "desc": "Uçuk.", "direct": ["16.50"], "compact": ["00.00", "01.00", "02.00", "31.10", "16.50", "31.50", "01.00"], "ulrich": [{"code": "4.01", "name": "Enfeksiyon"}]},
        "Hormonal Denge (K)": {"source": "RAH + Ulrich", "desc": "Kadın hormonları.", "direct": ["65.10"], "compact": ["00.00", "01.00", "02.00", "31.10", "65.10", "31.50", "01.00"], "ulrich": [{"code": "4.08", "name": "Kadın Hormon"}]},
        "Hormonal Denge (E)": {"source": "RAH + Ulrich", "desc": "Erkek hormonları.", "direct": ["65.20"], "compact": ["00.00", "01.00", "02.00", "31.10", "65.20", "31.50", "01.00"], "ulrich": [{"code": "4.09", "name": "Erkek Hormon"}]},
        "Jetlag": {"source": "Wellbeing", "desc": "Bioritim.", "direct": ["55.20"], "compact": ["00.00", "01.00", "02.00", "01.40", "55.20", "31.50", "01.00"], "ulrich": [{"code": "4.13", "name": "Fizik Sabitleri"}]},
        "Kabızlık": {"source": "RAH", "desc": "Bağırsak tembelliği.", "direct": ["47.86"], "compact": ["00.00", "01.00", "02.00", "31.12", "47.86", "31.50", "01.00"], "ulrich": [{"code": "4.07", "name": "Asidoz"}]},
        "Karaciğer Detoks": {"source": "RAH + Ulrich", "desc": "Temizleme.", "direct": ["48.10"], "compact": ["00.00", "01.00", "02.00", "31.29", "48.10", "31.50", "01.00"], "ulrich": [{"code": "4.14", "name": "Detoks"}]},
        "Menisküs / Diz": {"source": "RAH", "desc": "Diz sorunları.", "direct": ["53.51"], "compact": ["00.00", "01.00", "02.00", "31.39", "53.51", "31.50", "01.00"], "ulrich": [{"code": "4.13", "name": "Fizik Sabitleri"}]},
        "Menopoz": {"source": "RAH + Ulrich", "desc": "Ateş basması vb.", "direct": ["65.60"], "compact": ["00.00", "01.00", "02.00", "31.10", "65.60", "31.50", "01.00"], "ulrich": [{"code": "4.08", "name": "Kadın Hormon"}]},
        "Migren": {"source": "RAH + Ulrich", "desc": "Baş ağrısı.", "direct": ["55.60"], "compact": ["00.00", "01.00", "02.00", "31.10", "55.60", "31.50", "01.00"], "ulrich": [{"code": "4.40", "name": "Migren"}]},
        "Osteoporoz": {"source": "RAH + Ulrich", "desc": "Kemik erimesi.", "direct": ["53.80"], "compact": ["00.00", "01.00", "02.00", "31.41", "53.80", "31.50", "01.00"], "ulrich": [{"code": "4.13", "name": "Fizik Sabitleri"}]},
        "Panik Atak": {"source": "RAH + Ulrich", "desc": "Korku nöbeti.", "direct": ["72.05"], "compact": ["00.00", "01.00", "02.00", "31.10", "72.05", "31.50", "01.00"], "ulrich": [{"code": "4.02", "name": "Stres"}]},
        "Parkinson": {"source": "RAH + Ulrich", "desc": "Titreme.", "direct": ["55.31"], "compact": ["00.00", "01.00", "02.00", "31.34", "55.31", "31.50", "01.00"], "ulrich": [{"code": "4.17", "name": "Parkinson"}]},
        "Prostat": {"source": "RAH + Ulrich", "desc": "Büyüme / İltihap.", "direct": ["69.30"], "compact": ["00.00", "01.00", "02.00", "31.18", "69.30", "31.50", "01.00"], "ulrich": [{"code": "4.09", "name": "Erkek Hormon"}]},
        "Reflü": {"source": "RAH + Ulrich", "desc": "Mide asidi.", "direct": ["47.10"], "compact": ["00.00", "01.00", "02.00", "31.13", "47.10", "31.50", "01.00"], "ulrich": [{"code": "4.07", "name": "Asidoz"}]},
        "Romatizma": {"source": "RAH + Ulrich", "desc": "Eklem ağrısı.", "direct": ["53.52"], "compact": ["00.00", "01.00", "02.00", "31.40", "53.52", "31.50", "01.00"], "ulrich": [{"code": "4.13", "name": "Fizik Sabitleri"}]},
        "Sedef": {"source": "RAH + Ulrich", "desc": "Psoriasis.", "direct": ["63.10"], "compact": ["00.00", "01.00", "02.00", "31.38", "63.10", "31.50", "01.00"], "ulrich": [{"code": "4.06", "name": "Cilt"}]},
        "Sinüzit (Kronik)": {"source": "RAH + Ulrich", "desc": "Sinüs iltihabı.", "direct": ["43.16"], "compact": ["00.00", "01.00", "02.00", "31.25", "43.16", "31.50", "01.00"], "ulrich": [{"code": "4.01", "name": "Enfeksiyon"}]},
        "Sırt Ağrısı": {"source": "RAH + Ulrich", "desc": "Omurga.", "direct": ["53.70"], "compact": ["00.00", "01.00", "02.00", "31.40", "53.70", "31.50", "01.00"], "ulrich": [{"code": "4.21", "name": "Sırt Ağrısı"}]},
        "Spor Yaralanması": {"source": "RAH + Ulrich", "desc": "Travma.", "direct": ["53.21"], "compact": ["00.00", "01.00", "02.00", "31.39", "53.21", "31.50", "01.00"], "ulrich": [{"code": "4.22", "name": "Skar/Yara"}]},
        "Stres": {"source": "RAH + Ulrich", "desc": "Gerginlik.", "direct": ["75.10"], "compact": ["00.00", "01.00", "02.00", "31.10", "75.10", "31.50", "01.00"], "ulrich": [{"code": "4.02", "name": "Stres"}]},
        "Tinnitus": {"source": "RAH + Ulrich", "desc": "Kulak çınlaması.", "direct": ["59.10"], "compact": ["00.00", "01.00", "02.00", "31.10", "59.10", "31.50", "01.00"], "ulrich": [{"code": "4.12", "name": "Tinnitus"}]},
        "Tiroid": {"source": "RAH + Ulrich", "desc": "Dengesizlik.", "direct": ["65.33"], "compact": ["00.00", "01.00", "02.00", "31.33", "65.33", "31.50", "01.00"], "ulrich": [{"code": "4.08", "name": "Hormon"}]},
        "Uyku Bozukluğu": {"source": "RAH + Ulrich", "desc": "Uykusuzluk.", "direct": ["55.10"], "compact": ["00.00", "01.00", "02.21", "31.10", "55.10", "31.50", "01.00"], "ulrich": [{"code": "4.02", "name": "Stres"}]},
        "Yara İzi (Skar)": {"source": "Ulrich + RAH", "desc": "Skar dokusu.", "direct": ["31.81"], "compact": ["00.00", "01.00", "02.00", "31.10", "31.81", "31.50", "01.00"], "ulrich": [{"code": "4.22", "name": "Skar"}]},
        "Yüksek Tansiyon": {"source": "RAH + Ulrich", "desc": "Hipertansiyon.", "direct": ["39.60"], "compact": ["00.00", "01.00", "02.00", "31.39", "39.60", "31.50", "01.00"], "ulrich": [{"code": "4.18", "name": "Kalp"}]}
    }
    return db

def get_program_name(code):
    names = {
        "00.00": "Analiz Hazırlığı", "01.00": "Vitalizasyon Komple", "01.10": "Enerji Yükleme", "01.30": "Ön Kontrol", "01.40": "Çakralar Komple",
        "02.00": "Akupunktur Meridyenleri", "07.21": "Demir Metabolizması", "09.34": "Asit-Baz Dengesi",
        "16.00": "Bakteriyel Enfeksiyonlar", "16.20": "Epstein Barr", "16.50": "Herpes Simplex",
        "19.00": "Hücresel Bütünlük", "19.20": "Hücresel Dejenerasyon", "99.00": "Tümör Desteği",
        "22.00": "Elektrosmog", "22.10": "Geopati", "22.90": "Radyasyon Yükü", "22.93": "Elektrosensitivite", "24.00": "Parazitler", "24.10": "Borreliosis",
        "30.65": "Bağ Dokusu", "30.70": "Asitlenme", "30.90": "Mide Asidi Düzenleme",
        "31.10": "ATP Üretimi", "31.11": "Oksijenlenme", "31.12": "Su Dengesi", "31.13": "Mukoza Desteği", "31.14": "İnsülin Dengesi",
        "31.15": "Kalp Enerjisi", "31.16": "Bağırsak Florası", "31.17": "Mesane Desteği", "31.18": "Prostat Desteği",
        "31.20": "Rahim Desteği", "31.22": "Yumurtalık Desteği", "31.23": "Böbrek Enerjisi", "31.25": "Lenf Enerjisi",
        "31.29": "Karaciğer Enerjisi", "31.31": "Göz Enerjisi", "31.33": "Tiroid Enerjisi", "31.34": "Beyin Enerjisi", "31.35": "Sinir Enerjisi",
        "31.38": "Cilt Enerjisi", "31.39": "Kan Dolaşımı", "31.40": "Kas Enerjisi", "31.41": "Kemik Enerjisi",
        "31.50": "Temel Detoks", "31.51": "Detoks Kan", "31.52": "Detoks Lenf", "31.53": "Detoks Bağ Dokusu", "31.60": "Detoks Karaciğer", "31.61": "Ağır Metal Detoksu",
        "31.70": "İnflamasyon Akut", "31.80": "Yara İyileşmesi", "31.81": "Yara İzi Tedavisi", "31.87": "Ödem Çözme",
        "32.06": "Kan Yapımı", "32.10": "Eritrositler", "33.24": "Demir Eksikliği", "33.60": "Kan Dolaşımı",
        "34.00": "Bağışıklık Fizyolojisi", "35.10": "Bağışıklık Artırma", "35.11": "Th1 Bağışıklık", "35.20": "Alerji Temel", "35.30": "Fruktoz İntoleransı",
        "36.00": "Lenf Fizyolojisi", "36.50": "Dalak Desteği", "37.10": "Lenf Akışı", "37.13": "Lenf Drenajı", "37.15": "Lenfödem", "38.00": "Dolaşım Fizyolojisi",
        "38.10": "Arteriyel Dolaşım", "38.50": "Venöz Dolaşım", "39.10": "Dolaşım Bozukluğu", "39.15": "Arteriyoskleroz", "39.20": "Varis", "39.40": "Mikrodolaşım",
        "39.50": "Kan Basıncı Regülasyonu", "39.60": "Hipertansiyon", "39.65": "Böbrek Tansiyonu", "39.70": "Hipotansiyon", "40.00": "Kalp Fizyolojisi",
        "41.20": "Kalp Yetmezliği Sol", "41.30": "Kalp Yetmezliği Sağ", "41.40": "Anjin Pektoris", "41.50": "Koroner Damarlar",
        "42.00": "Solunum Fizyolojisi", "42.10": "Burun", "42.20": "Sinüsler", "42.50": "Uyku Apnesi", "42.60": "Bronşlar", "42.70": "Akciğerler",
        "43.10": "Öksürük", "43.11": "Nezle/Grip", "43.13": "Bronşit Akut", "43.14": "Bronşit Kronik", "43.15": "Sinüzit Akut", "43.16": "Sinüzit Kronik",
        "43.20": "Astım Bronşiyal", "43.30": "Alerjik Astım", "43.50": "Zatürre Sonrası", "43.52": "Covid-19 / Long-Covid",
        "44.00": "Böbrek Fizyolojisi", "44.10": "Böbrek Fonksiyonu", "44.17": "Böbrek Detoksu", "44.21": "İdrar Yolları", "45.05": "Böbrek Yetmezliği",
        "45.25": "Böbrek Taşı", "45.35": "Sistit", "45.40": "Mesane İltihabı", "45.80": "Ödem Atma",
        "46.00": "Sindirim Fizyolojisi", "46.10": "Ağız/Diş", "46.20": "Yemek Borusu", "46.30": "Mide Fonksiyonu", "46.40": "İnce Bağırsak", "46.50": "Kalın Bağırsak",
        "47.00": "Sindirim Bozukluğu", "47.10": "Reflü/Mide Yanması", "47.20": "Gastrit Akut", "47.22": "Helicobacter Pylori", "47.30": "Gastrit Kronik",
        "47.40": "Mide Ülseri", "47.50": "Crohn Hastalığı", "47.60": "Ülseratif Kolit", "47.70": "İrritabl Bağırsak", "47.82": "Candida Albicans",
        "47.86": "Kabızlık", "47.88": "Hemoroid", "48.10": "Karaciğer Fonksiyonu", "48.20": "Safra Kesesi", "48.35": "Pankreas",
        "49.10": "Karaciğer Yağlanması", "49.15": "Karaciğer Desteği", "49.34": "Safra Akışı", "49.37": "Safra Yolu İltihabı", "49.38": "Safra Taşı",
        "50.00": "Metabolizma Fizyolojisi", "50.10": "Yağ Metabolizması", "50.20": "Karbonhidrat Metabolizması", "50.35": "Kolesterol Dengeleme",
        "51.10": "Asit-Baz Metabolizması", "51.20": "Enzim Desteği", "51.40": "Diyabet", "51.50": "Gut",
        "52.00": "Kas-İskelet Fizyolojisi", "52.05": "Kalsiyum Metabolizması", "52.20": "Omurga", "52.25": "Bel Bölgesi", "52.60": "Diz Eklemi",
        "52.61": "Kıkırdak", "52.62": "Eklem Sıvısı", "53.11": "Kemik Kırığı", "53.21": "Spor Yaralanması", "53.22": "Burkulma", "53.23": "Kas Gerginliği",
        "53.24": "Kas Yırtılması", "53.25": "Kas Ağrısı", "53.28": "Miyogeloz", "53.41": "Disk Kayması", "53.51": "Menisküs", "53.52": "Artrit",
        "53.53": "Artroz", "53.54": "Romatizma", "53.62": "Tendinit", "53.70": "Sırt Ağrısı", "53.71": "Boyun Ağrısı", "53.73": "Bel Ağrısı",
        "53.80": "Osteoporoz", "53.83": "Lumbago", "53.84": "Fibromiyalji", "54.00": "Sinir Sistemi Fizyolojisi", "54.10": "Vejetatif Sinir Sistemi",
        "54.20": "Sempatik Sinir Sistemi", "54.22": "Görme Siniri", "54.25": "Trigeminal Sinir", "55.10": "Uykuya Dalma", "55.20": "Uykuyu Sürdürme",
        "55.30": "Alzheimer", "55.31": "Parkinson", "55.42": "Sinir Kılıfı", "55.43": "Multipl Skleroz", "55.45": "DEHB", "55.53": "Vertigo",
        "55.55": "Baş Ağrısı", "55.60": "Migren", "56.00": "Göz Fizyolojisi", "56.34": "Retina", "56.40": "Göz Merceği", "56.60": "Göz Basıncı",
        "56.61": "Göz Dolaşımı", "56.62": "Makula", "57.10": "Göz Tansiyonu Desteği", "57.20": "Katarakt", "57.30": "Glokom", "57.40": "Sarı Nokta",
        "57.52": "Konjonktivit", "57.53": "Göz Kuruluğu", "58.30": "İşitme Siniri", "58.40": "İç Kulak", "59.10": "Tinnitus", "59.30": "İşitme Kaybı", "59.40": "Ani İşitme Kaybı",
        "62.00": "Cilt Fizyolojisi", "62.10": "Cilt Rejenerasyonu", "62.20": "Cilt Nemlendirme", "62.50": "Bağ Dokusu Sıkılaştırma", "62.60": "Cilt Hücresi",
        "63.10": "Sedef", "63.20": "Nörodermatit", "63.40": "Ürtiker", "63.50": "Cilt Mantarı", "63.55": "Uçuk", "63.90": "Saç Dökülmesi",
        "64.00": "Hormonal Sistem", "64.05": "Hipofiz", "64.10": "Epifiz", "64.11": "Melatonin", "64.20": "Hipotalamus", "64.27": "Histamin",
        "64.28": "Serotonin", "64.29": "Dopamin", "64.30": "Tiroid", "64.35": "Paratiroid", "64.40": "Timus", "64.50": "Adrenal Bezler",
        "64.55": "Kortizol", "64.60": "Böbrek Üstü Bezi", "64.70": "Pankreas Hormon", "64.80": "Östrojen", "64.81": "Progesteron",
        "65.10": "Kadın Hormon Dengesi", "65.20": "Erkek Hormon Dengesi", "65.30": "Tiroid Dengesi", "65.31": "Haşimato", "65.33": "Hipertiroidi",
        "65.34": "Hipotiroidi", "65.40": "Adet Sancıları", "65.50": "Adet Düzensizliği", "65.60": "Menopoz",
        "66.00": "Kadın Cinsel Org.", "67.30": "Endometriozis", "68.00": "Erkek Cinsel Org.", "68.26": "Prostat", "69.10": "Prostat Büyümesi", "69.30": "Prostatit",
        "70.10": "Kronik Yorgunluk", "70.11": "Saç Kökü", "70.12": "Görme Gücü", "70.15": "İşitme Gücü", "70.16": "KBB Enfeksiyon", "70.17": "Alt Solunum Yolu",
        "70.18": "Kalp Güçlendirme", "70.19": "Mide-Bağırsak", "70.20": "Karaciğer-Safra", "70.21": "Böbrek-Mesane", "70.22": "Kadın Hastalıkları",
        "70.23": "Erkek Hastalıkları", "70.24": "Cilt Hastalıkları", "70.26": "Kas-İskelet", "70.27": "Yumuşak Doku", "70.28": "Eklem Dejenerasyonu",
        "70.41": "Mide Koruma", "70.45": "Migren Patojen", "70.46": "Grip Patojen", "70.47": "Tansiyon Düşürme", "70.51": "Kırık İyileşmesi",
        "70.54": "Tiroid Regülasyonu", "70.63": "Yara İyileşmesi", "70.68": "Titreme",
        "71.11": "Ürik Asit Atılımı", "71.50": "Ağrı Tedavisi", "72.00": "Psikolojik Denge", "72.05": "Korku/Panik", "72.10": "Depresyon",
        "75.00": "Kulak Çınlaması", "75.10": "Stres", "75.15": "Kilo Verme", "75.16": "Sigara Bırakma", "75.17": "Yoksunluk Belirtileri", "83.80": "Öğrenme Blokajı"
    }
    
    if code in names:
        return names[code]
    
    if code.startswith("70."):
        return "Sistem Tedavisi (Kombine)"
    
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

    # --- SIDEBAR (GİZLENDİ) ---
    with st.sidebar:
        st.write("")

    # --- HEADER ---
    c1, c2 = st.columns([1, 5])
    with c1:
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        try:
            if os.path.exists("drsaitlogo.jpeg"):
                st.image("drsaitlogo.jpeg", width=90)
        except: pass
        st.markdown('</div>', unsafe_allow_html=True)
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
    st.markdown('<div class="spacer-div"></div>', unsafe_allow_html=True)

    if selected_disease:
        data = db[selected_disease]
        
        # Bilgi Kartı
        st.markdown(f"""
        <div class="disease-card">
            <h2>📌 {selected_disease}</h2>
            <p style="font-size: 1.1rem; color: #555;">{data['desc']}</p>
            <div style="margin-top: 15px; font-size: 0.85rem; color: #888;">📚 <b>Kaynak:</b> {data['source']}</div>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["🚀 Kompakt Protokol", "⚡ Doğrudan Kodlar", "🧬 Ulrich Protokolü"])

        # --- RAH KOMPAKT ---
        with tab1:
            st.info("**Önerilen Yöntem:** Hazırlık > Enerji > Tedavi > Detoks sıralamasıdır.")
            share_text = f"🩺 *Dr. Sait Sevinç - RAH Protokolü*\n\n*Hastalık:* {selected_disease}\n\n*Uygulama Adımları:*\n"
            total_minutes = 0
            for step_code in data["compact"]:
                duration = get_duration(step_code)
                cat_class = get_category_class(step_code)
                cat_name = get_category_name(step_code)
                prog_name = get_program_name(step_code)
                if step_code == "00.00": prog_name = "Analiz Hazırlığı"
                try: total_minutes += int(duration.split()[0])
                except: pass
                share_text += f"- {step_code} ({prog_name}) - {duration}\n"
                st.markdown(f"""
                <div class="step-row">
                    <div class="code-pill">{step_code}</div>
                    <div style="flex-grow: 1; font-weight: 600; color: #34495e;">{prog_name}</div>
                    <span class="tag {cat_class}">{cat_name}</span>
                    <div style="margin-left: 15px; font-size: 0.85rem; color: #7f8c8d; font-weight: bold;">⏱️ {duration}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.success(f"⏱️ **Toplam Süre:** {total_minutes} Dakika")
            share_text += f"\n⏱️ *Toplam Süre:* {total_minutes} Dakika"
            
            # AI ASİSTAN & PAYLAŞIM
            st.markdown("---")
            st.markdown("##### 🤖 Asistan & Paylaşım")
            encoded_text = urllib.parse.quote(share_text + "\n\nSağlıklı günler dileriz.")
            whatsapp_url = f"https://wa.me/?text={encoded_text}"
            
            col_ai1, col_ai2 = st.columns(2)
            with col_ai1:
                 st.markdown(f'<a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">📲 WhatsApp ile Gönder</a>', unsafe_allow_html=True)
            with col_ai2:
                with st.expander("📋 Metni Kopyala"):
                    st.code(share_text + "\n\nSağlıklı günler dileriz.", language="text")

        # --- DOĞRUDAN KODLAR ---
        with tab2:
            st.warning("**Dikkat:** Bu kodlar sadece spesifik hastalık frekanslarıdır.")
            cols = st.columns(4)
            for i, code in enumerate(data["direct"]):
                with cols[i % 4]: st.metric(label=f"Kod {i+1}", value=code)

        # --- ULRICH ---
        with tab3:
            if "ulrich" in data:
                st.markdown(f"""<div class="ulrich-card"><b>ℹ️ Dr. Elmar Ulrich Modülü (M4):</b> Bu programlar özel sistem kartları veya 90.00 serisi içindedir.</div><br>""", unsafe_allow_html=True)
                ulrich_text = f"🧬 *Dr. Ulrich Protokolü ({selected_disease})*\n"
                for u_prog in data["ulrich"]:
                    ulrich_text += f"- {u_prog['code']} : {u_prog['name']}\n"
                    st.markdown(f"""
                    <div class="step-row" style="border-left: 5px solid #f1c40f;">
                        <div class="code-pill" style="background-color: #f39c12;">{u_prog['code']}</div>
                        <div style="flex-grow: 1; margin-left: 15px; font-weight: 700; color: #d35400;">{u_prog['name']}</div>
                        <div style="color: #7f8c8d; font-weight: 600;">⏱️ 10-20 dk</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("---")
                encoded_ulrich = urllib.parse.quote(ulrich_text + "\n\nDr. Sait Sevinç Kliniği")
                st.markdown(f'<a href="https://wa.me/?text={encoded_ulrich}" target="_blank" class="whatsapp-btn" style="background-color:#f39c12;">📲 Ulrich Protokolünü Paylaş</a>', unsafe_allow_html=True)
            else:
                st.info("Bu rahatsızlık için özel bir Ulrich protokolü tanımlanmamış.")

    else:
        # AI ASİSTAN (SOHBET MODU)
        st.markdown("---")
        st.markdown("### 🤖 Dr. Sait AI Asistan")
        st.caption("Hastalık kombinasyonları veya özel durumlar için bana sorabilirsiniz.")
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Örn: Migren ve Tansiyon hastası için ne önerirsin?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            response = "Üzgünüm, şu an için sadece veritabanımdaki hastalıkları çapraz kontrol edebilirim."
            found_diseases = []
            lower_prompt = prompt.lower()
            
            for key in db.keys():
                if key.lower() in lower_prompt or key.split()[0].lower() in lower_prompt:
                    found_diseases.append(key)
            
            if found_diseases:
                response = f"**Tespit Edilen Durumlar:** {', '.join(found_diseases)}\n\n"
                response += "Bu durumlar için önerilen **Kombine Protokol Sırası**:\n"
                response += "1. **Analiz Hazırlığı (00.00)** - Her zaman ilk adım.\n"
                response += "2. **Enerji Dengeleme (01.00)** - Vücudu hazırlamak için.\n"
                for disease in found_diseases:
                    response += f"3. **{disease}:** İlgili tedavi kodları uygulanır.\n"
                response += "4. **Detoks (31.50)** - Tedavi sonu atılım için.\n\n"
                response += "Not: Çoklu hastalıklarda toplam süre uzayacağı için seansları günlere bölmeniz önerilir."
            else:
                response = "Belirttiğiniz durumlar veritabanımda tam eşleşmedi. Lütfen 'Migren', 'Gastrit' gibi net hastalık isimleri kullanın."

            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        st.markdown('<div class="custom-footer">Developed for Dr. Sait Sevinç © 2025</div>', unsafe_allow_html=True)
        with st.expander("⚠️ Yasal Uyarı"):
            st.caption("Bu uygulama sadece eğitim ve bilgilendirme amaçlıdır. Tıbbi tanı veya tedavi yerine geçmez. RAH ve Ulrich protokolleri destekleyici tamamlayıcı tıp uygulamalarıdır.")

if __name__ == "__main__":
    main()
