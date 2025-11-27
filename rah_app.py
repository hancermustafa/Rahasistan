import streamlit as st
import pandas as pd
import os

# =============================================================================
# 1. GÖRSEL TASARIM (AYNI KALDI - SORUNSUZ ÇALIŞAN VERSİYON)
# =============================================================================
def local_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    [data-testid="stAppViewContainer"] { background-color: #ffffff !important; font-family: 'Inter', sans-serif; color: #333333 !important; }
    h1, h2, h3, h4, h5, h6, p, div, span, label, li, button { color: #2c3e50; }
    
    div[data-testid="stMetricValue"] { color: #d35400 !important; font-size: 1.6rem !important; font-weight: 800 !important; }
    div[data-testid="stMetricLabel"] { color: #7f8c8d !important; font-size: 0.85rem !important; font-weight: 600 !important; }
    div[data-testid="metric-container"] { background-color: #fff; border: 1px solid #eee; padding: 10px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }

    [data-testid="stSidebar"] { background-color: #f4f6f8 !important; border-right: 1px solid #e0e0e0; }
    [data-testid="stSidebar"] * { color: #2c3e50 !important; }
    .stRadio label { color: #2c3e50 !important; font-weight: 600; }

    div[data-baseweb="select"] > div { background-color: #ffffff !important; border: 2px solid #dce1e6 !important; color: #333 !important; }
    div[data-baseweb="select"] span { color: #333 !important; }
    ul[data-baseweb="menu"] { background-color: #ffffff !important; }
    li[role="option"] { color: #333 !important; background-color: #ffffff !important; }
    li[role="option"]:hover { background-color: #fff3e0 !important; font-weight: bold; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 5px; }
    .stTabs [data-baseweb="tab"] { height: 45px; background-color: #f1f2f6 !important; color: #57606f !important; border-radius: 6px 6px 0 0; font-weight: 600; border: 1px solid #e0e0e0; border-bottom: none; }
    .stTabs [aria-selected="true"] { background-color: #ffffff !important; color: #e67e22 !important; border-top: 3px solid #e67e22 !important; }

    .header-container { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 2rem; border-radius: 12px; color: white !important; box-shadow: 0 8px 20px rgba(0,0,0,0.15); margin-bottom: 30px; border-bottom: 5px solid #e67e22; text-align: center; }
    .header-container h1 { color: white !important; margin: 0; font-size: 1.8rem; text-shadow: 1px 1px 3px rgba(0,0,0,0.3); }
    .header-container p { color: #bdc3c7 !important; margin-top: 5px; font-size: 0.9rem; }

    .disease-card { background: white; border: 1px solid #eee; border-left: 6px solid #e67e22; padding: 20px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 25px; }
    .ulrich-card { background: #fff9db; border: 1px solid #f1c40f; padding: 15px; border-radius: 8px; color: #5d4037 !important; }
    .ulrich-card b { color: #d35400 !important; }

    .step-row { display: flex; flex-wrap: wrap; align-items: center; background: white; border: 1px solid #f0f0f0; margin-bottom: 8px; padding: 10px 15px; border-radius: 8px; transition: transform 0.2s; }
    .step-row:hover { border-color: #e67e22; transform: translateX(3px); box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
    .code-pill { background: #2c3e50; color: #fff !important; font-family: 'Courier New', monospace; font-weight: bold; padding: 5px 12px; border-radius: 5px; min-width: 80px; text-align: center; margin-right: 15px; font-size: 1.1rem; }
    
    .tag { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: bold; color: white !important; margin-left: auto; }
    .bg-blue { background-color: #3498db; }
    .bg-green { background-color: #27ae60; }
    .bg-purple { background-color: #9b59b6; }
    .bg-red { background-color: #e74c3c; }
    .bg-gold { background-color: #f39c12; }

    .stDeployButton, footer, header {visibility: hidden;}
    .custom-footer { margin-top: 50px; text-align: center; color: #95a5a6 !important; font-size: 0.8rem; border-top: 1px solid #eee; padding-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# 2. VERİTABANI (TAM KAPSAMLI - EKSİKSİZ LİSTE)
# =============================================================================
def get_rah_database():
    # RAH Source 2 (Ch 18) + Dr. Ulrich (4.01 - 4.22 Tam Liste)
    db = {
        # --- A ---
        "Alerji (Genel)": {
            "source": "RAH (Syf 121) + Ulrich (4.01)",
            "desc": "Alerjik reaksiyonlar, histamin dengesi.",
            "direct": ["35.20", "64.27"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "34.00", "35.10", "35.20", "36.00", "64.27", "31.50", "01.00"],
            "ulrich": [{"code": "4.01", "name": "Alerji Programı"}, {"code": "4.14", "name": "Temizleme (Clearing)"}]
        },
        "Alzheimer": {
            "source": "RAH (Syf 170)",
            "desc": "Bellek kaybı ve kognitif destek.",
            "direct": ["55.30"],
            "compact": ["00.00", "01.00", "02.00", "31.34", "31.35", "35.10", "70.10", "38.10", "39.10", "50.10", "54.00", "55.30", "55.42", "72.00", "75.10", "31.50", "01.00"],
            "ulrich": [{"code": "4.04", "name": "Öğrenme / Hafıza"}]
        },
        "Anemi (Demir Eksikliği)": {
            "source": "RAH (Syf 202)",
            "desc": "Kansızlık ve demir emilimi.",
            "direct": ["33.24"],
            "compact": ["00.00", "01.00", "02.00", "07.21", "31.39", "35.10", "32.06", "32.10", "33.24", "33.60", "31.50", "01.00"]
        },
        "Anjin Pektoris": {
            "source": "RAH (Syf 130) + Ulrich (4.18)",
            "desc": "Göğüs ağrısı ve kalp damar sıkışması.",
            "direct": ["41.40"],
            "compact": ["00.00", "01.00", "02.00", "31.15", "35.10", "38.00", "40.00", "41.40", "41.50", "31.50", "01.00"],
            "ulrich": [{"code": "4.18", "name": "Kalp Programı"}]
        },
        "Artroz / Kireçlenme": {
            "source": "RAH (Syf 160) + Ulrich (4.13)",
            "desc": "Eklem dejenerasyonu.",
            "direct": ["53.53"],
            "compact": ["00.00", "01.00", "02.00", "31.40", "31.41", "35.10", "70.28", "52.00", "52.61", "52.62", "53.53", "53.54", "31.50", "01.00"],
            "ulrich": [{"code": "4.13", "name": "Fizik Sabitleri (Denge)"}]
        },
        "Asidoz (Asitlenme)": {
            "source": "Ulrich (4.07)",
            "desc": "Vücut pH dengesinin bozulması.",
            "direct": ["31.53"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "31.53", "06.00", "31.50", "01.00"],
            "ulrich": [{"code": "4.07", "name": "Asidoz Programı"}]
        },
        "Astım (Bronşiyal)": {
            "source": "RAH (Syf 135) + Ulrich (4.20)",
            "desc": "Solunum zorluğu ve hava yolu darlığı.",
            "direct": ["43.20"],
            "compact": ["00.00", "01.00", "02.00", "31.11", "34.00", "35.10", "35.20", "70.16", "36.00", "42.60", "42.70", "43.10", "43.20", "43.30", "31.50", "01.00"],
            "ulrich": [{"code": "4.20", "name": "Astım Programı"}]
        },

        # --- B ---
        "Bağımlılık (Sigara/Alkol)": {
            "source": "RAH (Syf 207) + Ulrich (4.14)",
            "desc": "Bırakma süreci desteği.",
            "direct": ["75.17"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "48.10", "50.00", "54.10", "64.28", "64.29", "72.05", "75.10", "75.17", "31.50", "01.00"],
            "ulrich": [{"code": "4.14", "name": "Temizleme (Clearing)"}]
        },
        "Bağışıklık Güçlendirme": {
            "source": "RAH (Syf 121) + Ulrich (4.03)",
            "desc": "Genel direnç artırma.",
            "direct": ["35.10"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "34.00", "35.10", "35.11", "36.50", "31.50", "01.00"],
            "ulrich": [{"code": "4.03", "name": "Ozon / Radyasyon Koruma"}]
        },
        "Baş Ağrısı": {
            "source": "RAH (Syf 174) + Ulrich (4.40)",
            "desc": "Genel baş ağrıları.",
            "direct": ["55.55"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.45", "54.10", "55.55", "72.05", "31.50", "01.00"],
            "ulrich": [{"code": "4.40", "name": "Baş Ağrısı / Migren"}]
        },
        "Bel Ağrısı (Lumbago)": {
            "source": "RAH (Syf 166)",
            "desc": "Bel bölgesi ağrıları.",
            "direct": ["53.83"],
            "compact": ["00.00", "01.00", "02.00", "31.40", "35.10", "52.25", "53.23", "53.41", "53.73", "53.83", "31.50", "01.00"]
        },
        "Bronşit (Akut)": {
            "source": "RAH (Syf 132)",
            "desc": "Akut öksürük ve inflamasyon.",
            "direct": ["43.13"],
            "compact": ["00.00", "01.00", "02.00", "31.11", "35.10", "70.17", "36.00", "42.60", "43.13", "43.30", "31.50", "01.00"]
        },
        "Böbrek Taşı": {
            "source": "RAH (Syf 140)",
            "desc": "Nefrolityaz.",
            "direct": ["45.25"],
            "compact": ["00.00", "01.00", "02.00", "31.23", "35.10", "44.00", "44.21", "39.65", "45.25", "31.50", "01.00"]
        },

        # --- C ---
        "Cilt Mantarı": {
            "source": "RAH (Syf 183) + Ulrich (4.05)",
            "desc": "Mikoz enfeksiyonları.",
            "direct": ["63.50"],
            "compact": ["00.00", "01.00", "02.00", "30.65", "31.38", "35.10", "70.24", "62.10", "63.50", "31.50", "01.00"],
            "ulrich": [{"code": "4.05", "name": "Mantar Programı"}]
        },
        "Cilt Sorunları (Akne/Egzama)": {
            "source": "RAH (Syf 181)",
            "desc": "Genel cilt problemleri.",
            "direct": ["63.10"],
            "compact": ["00.00", "01.00", "02.00", "31.38", "30.65", "35.10", "70.24", "62.10", "63.10", "63.20", "31.50", "01.00"]
        },
        "Covid-19 / Long-Covid": {
            "source": "RAH (Syf 137)",
            "desc": "Viral enfeksiyon sonrası toparlanma.",
            "direct": ["43.52"],
            "compact": ["00.00", "01.00", "02.00", "31.11", "35.10", "22.93", "70.17", "42.70", "43.10", "43.30", "43.50", "43.52", "31.50", "01.00"]
        },
        "Crohn Hastalığı": {
            "source": "RAH (Syf 146)",
            "desc": "İnflamatuar bağırsak hastalığı.",
            "direct": ["47.50"],
            "compact": ["00.00", "01.00", "02.00", "31.12", "31.16", "31.70", "35.10", "70.19", "46.00", "47.50", "64.55", "72.00", "31.50", "01.00"]
        },

        # --- D ---
        "DEHB (Dikkat Eksikliği)": {
            "source": "RAH (Syf 172) + Ulrich (4.04)",
            "desc": "Konsantrasyon ve öğrenme güçlüğü.",
            "direct": ["55.45"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "35.20", "70.10", "54.00", "54.10", "55.45", "64.27", "83.80", "72.00", "31.50", "01.00"],
            "ulrich": [{"code": "4.04", "name": "Öğrenme Programı"}]
        },
        "Depresyon": {
            "source": "RAH (Syf 167) + Ulrich (4.16)",
            "desc": "Ruhsal çöküntü ve enerji düşüklüğü.",
            "direct": ["72.10"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "48.10", "64.10", "64.28", "64.29", "72.10", "75.10", "31.50", "01.00"],
            "ulrich": [{"code": "4.16", "name": "Kundalini (Enerji) Stresi"}]
        },
        "Diyabet (Şeker Hastalığı)": {
            "source": "RAH (Syf 154) + Ulrich (4.19)",
            "desc": "Metabolizma ve pankreas desteği.",
            "direct": ["51.40"],
            "compact": ["00.00", "01.00", "02.00", "31.14", "35.10", "70.20", "48.35", "50.20", "51.20", "51.40", "64.70", "31.50", "01.00"],
            "ulrich": [{"code": "4.19", "name": "Diyabet Programı"}]
        },
        "Dolaşım Bozukluğu": {
            "source": "RAH (Syf 125) + Ulrich (4.18)",
            "desc": "Soğuk el/ayak ve genel dolaşım.",
            "direct": ["39.10"],
            "compact": ["00.00", "01.00", "02.00", "31.39", "35.10", "38.00", "38.10", "39.10", "31.50", "01.00"],
            "ulrich": [{"code": "4.18", "name": "Kalp / Dolaşım"}]
        },

        # --- E ---
        "Endometriozis": {
            "source": "RAH (Syf 199)",
            "desc": "Rahim içi doku büyümesi.",
            "direct": ["67.30"],
            "compact": ["00.00", "01.00", "02.00", "31.20", "31.22", "31.81", "35.10", "70.22", "36.10", "64.80", "65.10", "65.30", "65.31", "65.50", "66.00", "67.30", "72.00", "75.00", "31.50", "01.00"]
        },

        # --- F ---
        "Fibromiyalji": {
            "source": "RAH (Syf 166)",
            "desc": "Yaygın kas ağrıları.",
            "direct": ["53.84"],
            "compact": ["00.00", "01.00", "02.00", "31.38", "31.40", "35.10", "70.26", "70.27", "36.00", "52.00", "53.23", "53.25", "53.28", "53.62", "53.84", "62.10", "64.00", "31.50", "01.00"]
        },
        "Fruktoz İntoleransı": {
            "source": "RAH (Syf 121)",
            "desc": "Fruktoz sindirim bozukluğu.",
            "direct": ["35.30"],
            "compact": ["00.00", "01.00", "02.00", "09.34", "31.10", "34.00", "35.10", "35.30", "46.40", "46.50", "47.70", "31.50", "01.00"]
        },

        # --- G ---
        "Gastrit / Mide Yanması": {
            "source": "RAH (Syf 143)",
            "desc": "Mide mukozası iltihabı ve reflü.",
            "direct": ["47.20", "47.10"],
            "compact": ["00.00", "01.00", "02.00", "31.13", "35.10", "70.19", "46.30", "47.20", "47.10", "31.50", "01.00"]
        },
        "Glokom (Göz Tansiyonu)": {
            "source": "RAH (Syf 176)",
            "desc": "Göz içi basıncı yüksekliği.",
            "direct": ["57.30"],
            "compact": ["00.00", "01.00", "02.00", "31.31", "35.10", "70.12", "56.00", "56.60", "57.10", "57.30", "31.50", "01.00"]
        },
        "Grip / Enfeksiyon": {
            "source": "RAH (Syf 82) + Ulrich (4.01)",
            "desc": "Viral enfeksiyonlar.",
            "direct": ["70.46", "43.11"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.46", "36.00", "42.10", "43.11", "31.50", "01.00"],
            "ulrich": [{"code": "4.01", "name": "Alerji/Enfeksiyon (Temel)"}]
        },
        "Gut Hastalığı": {
            "source": "RAH (Syf 154)",
            "desc": "Ürik asit birikimi.",
            "direct": ["51.50"],
            "compact": ["00.00", "01.00", "02.00", "30.70", "31.10", "35.10", "50.00", "51.10", "51.50", "52.60", "71.11", "71.50", "31.50", "01.00"]
        },

        # --- H ---
        "Hormonal Denge (Kadın)": {
            "source": "RAH (Syf 186) + Ulrich (4.08)",
            "desc": "Genel hormon düzenleme.",
            "direct": ["65.10"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.22", "64.00", "65.10", "31.50", "01.00"],
            "ulrich": [{"code": "4.08", "name": "Kadın Hormon Programı"}]
        },
        "Hormonal Denge (Erkek)": {
            "source": "RAH (Syf 186) + Ulrich (4.09)",
            "desc": "Genel hormon düzenleme.",
            "direct": ["65.20"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.23", "64.00", "65.20", "31.50", "01.00"],
            "ulrich": [{"code": "4.09", "name": "Erkek Hormon Programı"}]
        },

        # --- K ---
        "Kabızlık": {
            "source": "RAH (Syf 148)",
            "desc": "Bağırsak hareketliliği sorunu.",
            "direct": ["47.86"],
            "compact": ["00.00", "01.00", "02.00", "31.12", "31.16", "35.10", "70.19", "46.00", "47.86", "31.50", "01.00"]
        },
        "Karaciğer Detoks": {
            "source": "RAH (Syf 149)",
            "desc": "Karaciğer temizliği ve desteği.",
            "direct": ["48.10", "31.60"],
            "compact": ["00.00", "01.00", "02.00", "31.29", "35.10", "70.20", "48.10", "49.10", "31.60", "31.50", "01.00"]
        },
        "Katarakt": {
            "source": "RAH (Syf 176)",
            "desc": "Göz merceği bulanıklığı.",
            "direct": ["57.20"],
            "compact": ["00.00", "01.00", "02.00", "31.31", "35.10", "70.12", "56.00", "56.40", "57.20", "31.50", "01.00"]
        },
        "Kilo Verme": {
            "source": "RAH (Syf 152)",
            "desc": "Metabolizma hızlandırma.",
            "direct": ["75.15"],
            "compact": ["00.00", "01.00", "02.00", "09.00", "31.10", "36.00", "38.00", "44.00", "46.40", "48.10", "50.00", "64.00", "75.10", "75.15", "31.50", "01.00"]
        },

        # --- M ---
        "Menopoz": {
            "source": "RAH (Syf 195) + Ulrich (4.08)",
            "desc": "Klimakterik şikayetler.",
            "direct": ["65.60"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.22", "64.10", "64.20", "65.10", "65.60", "66.00", "72.00", "75.00", "31.50", "01.00"],
            "ulrich": [{"code": "4.08", "name": "Kadın Hormonları"}]
        },
        "Migren": {
            "source": "RAH (Syf 175) + Ulrich (4.40)",
            "desc": "Şiddetli baş ağrısı.",
            "direct": ["55.60"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.45", "38.10", "39.10", "39.40", "54.10", "54.25", "55.55", "55.60", "64.00", "72.05", "31.50", "01.00"],
            "ulrich": [{"code": "4.40", "name": "Baş Ağrısı/Migren"}]
        },

        # --- O ---
        "Operasyon Sonrası Bakım": {
            "source": "Dr. Ulrich (4.10)",
            "desc": "Cerrahi müdahale sonrası iyileşme.",
            "direct": ["70.63"],
            "compact": ["00.00", "01.00", "31.80", "31.81", "31.82", "70.63", "35.10", "31.50", "01.00"],
            "ulrich": [{"code": "4.10", "name": "Op. Sonrası Bakım"}]
        },
        "Osteoporoz": {
            "source": "RAH (Syf 165) + Ulrich (4.13)",
            "desc": "Kemik erimesi.",
            "direct": ["53.80"],
            "compact": ["00.00", "01.00", "02.00", "31.41", "35.10", "50.00", "52.00", "52.05", "53.80", "64.00", "64.81", "31.50", "01.00"],
            "ulrich": [{"code": "4.13", "name": "Fizik Sabitleri"}]
        },

        # --- P ---
        "Parkinson": {
            "source": "RAH (Syf 170)",
            "desc": "Titreme ve hareket bozukluğu.",
            "direct": ["55.31"],
            "compact": ["00.00", "01.00", "02.00", "31.34", "31.35", "35.10", "70.68", "38.10", "54.00", "55.31", "64.28", "72.00", "75.10", "31.50", "01.00"]
        },
        "Prostat Sorunları": {
            "source": "RAH (Syf 200) + Ulrich (4.09)",
            "desc": "Prostatit ve büyüme.",
            "direct": ["69.30"],
            "compact": ["00.00", "01.00", "02.00", "31.18", "35.10", "70.23", "68.26", "69.10", "69.30", "31.50", "01.00"],
            "ulrich": [{"code": "4.09", "name": "Erkek Hormonları"}]
        },

        # --- R ---
        "Radyasyon / 5G Koruma": {
            "source": "Ulrich (4.03)",
            "desc": "Elektrosmog ve radyasyon detoksu.",
            "direct": ["22.00", "22.90"],
            "compact": ["00.00", "01.00", "02.00", "22.00", "22.10", "22.90", "22.93", "31.10", "31.50", "01.00"],
            "ulrich": [{"code": "4.03", "name": "Ozon / Radyasyon Koruma"}]
        },
        "Romatizma / Artrit": {
            "source": "RAH (Syf 160)",
            "desc": "Eklem iltihabı ve ağrıları.",
            "direct": ["53.52"],
            "compact": ["00.00", "01.00", "02.00", "31.40", "31.41", "35.10", "70.28", "52.00", "53.52", "53.53", "53.54", "31.50", "01.00"]
        },

        # --- S ---
        "Sedef (Psoriasis)": {
            "source": "RAH (Syf 181)",
            "desc": "Cilt pullanması.",
            "direct": ["63.10"],
            "compact": ["00.00", "01.00", "02.00", "31.38", "30.65", "35.10", "70.24", "62.10", "62.20", "62.60", "63.10", "72.00", "75.00", "31.50", "01.00"]
        },
        "Sırt Ağrısı": {
            "source": "RAH (Syf 163)",
            "desc": "Omurga kaynaklı ağrılar.",
            "direct": ["53.70"],
            "compact": ["00.00", "01.00", "02.00", "31.40", "35.10", "71.11", "71.50", "52.00", "52.20", "53.23", "53.25", "53.41", "53.70", "72.05", "75.10", "31.50", "01.00"]
        },
        "Stres / Tükenmişlik": {
            "source": "RAH (Syf 207) + Ulrich (4.02)",
            "desc": "Sinirsel gerginlik ve rahatlama.",
            "direct": ["75.10"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "48.10", "50.00", "64.05", "64.10", "64.20", "64.28", "64.29", "64.30", "64.35", "64.40", "64.50", "72.05", "75.10", "31.50", "01.00"],
            "ulrich": [{"code": "4.02", "name": "Stres Programı"}, {"code": "4.15", "name": "İlişki Stresi"}, {"code": "4.16", "name": "Kundalini Stresi"}]
        },

        # --- T ---
        "Tinnitus (Çınlama)": {
            "source": "RAH (Syf 179) + Ulrich (4.12)",
            "desc": "Kulak çınlaması.",
            "direct": ["59.10"],
            "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.15", "38.10", "39.10", "58.30", "58.40", "59.10", "59.40", "72.00", "75.00", "31.50", "01.00"],
            "ulrich": [{"code": "4.12", "name": "Tinnitus Programı"}]
        },
        "Tiroid (Dengesizlik)": {
            "source": "RAH (Syf 188-189)",
            "desc": "Hipotiroidi veya Hipertiroidi.",
            "direct": ["65.33", "65.34"],
            "compact": ["00.00", "01.00", "02.00", "31.33", "35.10", "70.54", "64.10", "64.20", "64.30", "65.30", "31.50", "01.00"]
        },

        # --- U ---
        "Uyku Bozukluğu": {
            "source": "RAH (Syf 168) + Ulrich (4.02)",
            "desc": "Uykuya dalma ve sürdürme.",
            "direct": ["55.10", "55.20"],
            "compact": ["00.00", "01.00", "02.21", "31.10", "35.10", "70.10", "54.00", "55.10", "64.11", "65.30", "72.00", "75.10", "31.50", "01.00"],
            "ulrich": [{"code": "4.02", "name": "Stres (Uyku Öncesi)"}]
        },

        # --- Y ---
        "Yüksek Tansiyon": {
            "source": "RAH (Syf 127) + Ulrich (4.18)",
            "desc": "Hipertansiyon.",
            "direct": ["39.60"],
            "compact": ["00.00", "01.00", "02.00", "31.39", "35.10", "70.47", "38.00", "39.10", "39.40", "39.50", "39.60", "64.00", "31.50", "01.00"],
            "ulrich": [{"code": "4.18", "name": "Kalp Programı"}]
        }
    }
    return db

def get_program_name(code):
    names = {
        "00.00": "Analiz Hazırlığı", "01.00": "Vitalizasyon Komple", "01.10": "Enerji Yükleme", "01.30": "Ön Kontrol", "01.40": "Çakralar Komple",
        "02.00": "Akupunktur Meridyenleri", "07.21": "Demir Metabolizması",
        "22.00": "Elektrosmog", "22.90": "Radyasyon Yükü",
        "31.10": "ATP Üretimi", "31.50": "Temel Detoks", "31.60": "Detoks Karaciğer",
        "35.10": "Bağışıklık Artırma", "35.20": "Alerji Temel",
        "70.45": "Migren Patojen", "70.47": "Tansiyon Düşürme"
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
