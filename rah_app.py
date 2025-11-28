import streamlit as st
import pandas as pd
import os
import urllib.parse

# =============================================================================
# 1. GÖRSEL TASARIM (ULTIMATE UI FIX - INPUTS & SPACING)
# =============================================================================
def local_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800&display=swap');
    
    /* --- 1. ANA GÖVDE (ZORUNLU BEYAZ) --- */
    [data-testid="stAppViewContainer"] {
        background-color: #ffffff !important;
        font-family: 'Inter', sans-serif;
        color: #2c3e50 !important;
    }
    h1, h2, h3, h4, h5, h6, p, span, label, li, button { color: #2c3e50 !important; }

    /* --- 2. CİHAZ SEÇİMİ (TEK SATIR & KOMPAKT) --- */
    /* Radyo butonlarını çevreleyen alan */
    div[role="radiogroup"] {
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 15px;
        background-color: #f1f3f5; /* Hafif gri şerit */
        padding: 8px 15px;
        border-radius: 30px; /* Hap şeklinde */
        border: 1px solid #e0e0e0;
        margin-bottom: 10px;
        width: fit-content; /* Sadece içeriği kadar yer kapla */
    }
    /* Seçeneklerin kendisi */
    div[role="radiogroup"] label {
        background-color: transparent;
        padding: 0px 10px;
        margin: 0;
        border: none;
        font-size: 0.9rem;
        font-weight: 600;
        color: #555 !important;
        cursor: pointer;
    }
    /* Seçili olanın rengi (Streamlit varsayılanını kullanır ama biz zorlayalım) */
    div[role="radiogroup"] label[data-baseweb="radio"] {
        align-items: center;
    }

    /* --- 3. INPUT ALANLARI (SİYAH EKRAN KESİN ÇÖZÜMÜ) --- */
    
    /* Arama Kutusu (Selectbox) */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important; /* Arka plan BEYAZ */
        border: 2px solid #d1d8dd !important;
        color: #333333 !important; /* Yazı KOYU */
        border-radius: 10px;
        min-height: 45px;
    }
    div[data-baseweb="select"] span {
        color: #333333 !important; /* Seçilen yazı rengi */
    }
    /* Açılan Liste */
    ul[data-baseweb="menu"] {
        background-color: #ffffff !important;
        border: 1px solid #eee !important;
    }
    li[role="option"] {
        color: #333333 !important;
        background-color: #ffffff !important;
        border-bottom: 1px solid #f5f5f5;
    }
    li[role="option"]:hover, li[aria-selected="true"] {
        background-color: #e3f2fd !important; /* Açık mavi vurgu */
        color: #1565c0 !important;
        font-weight: bold;
    }

    /* AI Sohbet Kutusu (Chat Input) */
    .stChatInput input, .stChatInput textarea {
        background-color: #ffffff !important; /* BEYAZ */
        color: #333333 !important; /* SİYAH YAZI */
        border: 2px solid #d1d8dd !important;
        border-radius: 10px !important;
    }
    /* Chat Mesaj Balonları */
    [data-testid="stChatMessage"] {
        background-color: #f8f9fa !important;
        border: 1px solid #eee;
        border-radius: 10px;
        padding: 10px;
        color: #333 !important;
    }

    /* --- 4. HEADER (LOGOLU & KOMPAKT) --- */
    .header-box {
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 1rem;
        border-radius: 12px;
        color: white !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        margin-bottom: 15px;
        border-bottom: 4px solid #e67e22;
        gap: 15px;
    }
    .header-text {
        text-align: left;
    }
    .header-title {
        font-size: 1.6rem; font-weight: 800; margin: 0; color: white !important;
        line-height: 1.1;
    }
    .header-subtitle {
        font-size: 0.8rem; color: #ecf0f1 !important; margin: 0; font-weight: 400;
    }
    .logo-img {
        width: 60px; border-radius: 8px; border: 2px solid rgba(255,255,255,0.3);
    }

    /* --- 5. DİĞER (TURKUAZ KUTU VB.) --- */
    [data-testid="stCodeBlock"] {
        background-color: #E0F2F1 !important;
        border: 1px solid #80CBC4 !important;
        border-radius: 8px !important;
    }
    [data-testid="stCodeBlock"] code {
        color: #004D40 !important;
        background-color: transparent !important;
        font-family: monospace !important;
    }
    [data-testid="stCodeBlock"] button { color: #004D40 !important; }

    .whatsapp-btn {
        display: block; background-color: #25D366; color: white !important;
        padding: 10px; border-radius: 8px; text-decoration: none; font-weight: bold;
        text-align: center; margin-top: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    /* Mobil Uyum */
    @media only screen and (max-width: 600px) {
        .header-title { font-size: 1.3rem !important; }
        div[role="radiogroup"] { width: 100%; justify-content: space-between; }
        /* Klavye açılınca liste yukarı kaçmasın */
        ul[data-baseweb="menu"] { max-height: 200px !important; overflow-y: auto !important; }
    }

    /* Gizleme */
    [data-testid="stSidebar"] { display: none; } 
    .stDeployButton, footer, header { visibility: hidden; }
    .custom-footer { margin-top: 30px; text-align: center; color: #bdc3c7 !important; font-size: 0.75rem; border-top: 1px solid #eee; padding-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# 2. VERİTABANI (DEĞİŞTİRİLMEDİ - TAM LİSTE)
# =============================================================================
def get_rah_database():
    db = {
        "Ağır Metal Detoksu": {"source": "RAH (Syf 149) + Ulrich (4.14)", "desc": "Vücuttan ağır metallerin atılımı.", "direct": ["31.60", "31.50"], "compact": ["00.00", "01.00", "02.00", "31.10", "31.50", "31.60", "31.61", "09.34", "44.10", "48.10", "31.50", "01.00"], "ulrich": [{"code": "4.14", "name": "Temizleme / Detoks"}]},
        "Alerji (Genel)": {"source": "RAH (Syf 121) + Ulrich (4.01)", "desc": "Alerjik reaksiyonlar, histamin dengesi.", "direct": ["35.20", "64.27"], "compact": ["00.00", "01.00", "02.00", "31.10", "34.00", "35.10", "35.20", "36.00", "64.27", "31.50", "01.00"], "ulrich": [{"code": "4.01", "name": "Alerji Programı"}, {"code": "4.14", "name": "Temizleme (Clearing)"}]},
        "Alzheimer": {"source": "RAH (Syf 170) + Ulrich (4.04)", "desc": "Bellek kaybı ve kognitif destek.", "direct": ["55.30"], "compact": ["00.00", "01.00", "02.00", "31.34", "31.35", "35.10", "70.10", "38.10", "39.10", "50.10", "54.00", "55.30", "55.42", "72.00", "75.10", "31.50", "01.00"], "ulrich": [{"code": "4.04", "name": "Öğrenme / Hafıza"}]},
        "Anemi (Demir Eksikliği)": {"source": "RAH (Syf 202)", "desc": "Kansızlık ve demir emilimi metabolizması.", "direct": ["33.24"], "compact": ["00.00", "01.00", "02.00", "07.21", "31.39", "35.10", "32.06", "32.10", "33.24", "33.60", "31.50", "01.00"]},
        "Anjin Pektoris": {"source": "RAH (Syf 130) + Ulrich (4.18)", "desc": "Göğüs ağrısı, kalp damar sıkışması.", "direct": ["41.40"], "compact": ["00.00", "01.00", "02.00", "31.15", "35.10", "38.00", "40.00", "41.40", "41.50", "31.50", "01.00"], "ulrich": [{"code": "4.18", "name": "Kalp Programı"}]},
        "Anti-Aging (Gençleşme)": {"source": "Wellbeing + RAH", "desc": "Hücresel yenilenme, cilt elastikiyeti.", "direct": ["30.65", "31.38"], "compact": ["00.00", "01.00", "02.00", "30.65", "31.38", "62.10", "62.50", "64.00", "35.10", "31.50", "01.00"], "ulrich": [{"code": "4.06", "name": "Cilt / Saç / Tırnak"}]},
        "Artroz / Kireçlenme": {"source": "RAH (Syf 160) + Ulrich (4.13)", "desc": "Eklem dejenerasyonu.", "direct": ["53.53"], "compact": ["00.00", "01.00", "02.00", "31.40", "31.41", "35.10", "70.28", "52.00", "52.61", "52.62", "53.53", "53.54", "31.50", "01.00"], "ulrich": [{"code": "4.13", "name": "Fizik Sabitleri"}]},
        "Asidoz (Asitlenme)": {"source": "Ulrich 4.07", "desc": "Vücut pH dengesinin bozulması.", "direct": ["31.53"], "compact": ["00.00", "01.00", "02.00", "31.10", "31.53", "06.00", "31.50", "01.00"], "ulrich": [{"code": "4.07", "name": "Asidoz Programı"}]},
        "Astım (Bronşiyal)": {"source": "RAH (Syf 135) + Ulrich 4.20", "desc": "Solunum zorluğu, bronşların daralması.", "direct": ["43.20"], "compact": ["00.00", "01.00", "02.00", "31.11", "34.00", "35.10", "35.20", "70.16", "36.00", "42.60", "42.70", "43.10", "43.20", "43.30", "31.50", "01.00"], "ulrich": [{"code": "4.20", "name": "Astım Programı"}]},
        "Bağımlılık (Alkol/Madde)": {"source": "RAH (Syf 207) + Ulrich 4.14", "desc": "Genel bağımlılık tedavisi.", "direct": ["75.17"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "48.10", "50.00", "54.10", "64.28", "64.29", "72.05", "75.10", "75.17", "31.50", "01.00"], "ulrich": [{"code": "4.14", "name": "Temizleme"}]},
        "Bağışıklık Güçlendirme": {"source": "RAH (Syf 121) + Ulrich 4.03", "desc": "Genel direnç artırma.", "direct": ["35.10"], "compact": ["00.00", "01.00", "02.00", "31.10", "34.00", "35.10", "35.11", "36.50", "31.50", "01.00"], "ulrich": [{"code": "4.03", "name": "Ozon / Radyasyon"}, {"code": "90.56", "name": "Bağışıklık Sistemi"}]},
        "Baş Ağrısı": {"source": "RAH (Syf 174) + Ulrich 4.40", "desc": "Genel baş ağrıları.", "direct": ["55.55"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.45", "54.10", "55.55", "72.05", "31.50", "01.00"], "ulrich": [{"code": "4.40", "name": "Baş Ağrısı"}]},
        "Bel Ağrısı (Lumbago)": {"source": "RAH (Syf 166) + Ulrich 4.21", "desc": "Bel bölgesi ağrıları.", "direct": ["53.83"], "compact": ["00.00", "01.00", "02.00", "31.40", "35.10", "52.25", "53.23", "53.41", "53.73", "53.83", "31.50", "01.00"], "ulrich": [{"code": "4.21", "name": "Sırt Ağrısı"}]},
        "Borreliosis (Lyme)": {"source": "RAH (Syf 85) + Ulrich 4.01", "desc": "Kene kaynaklı enfeksiyon.", "direct": ["24.10"], "compact": ["00.00", "01.00", "02.00", "24.00", "24.10", "31.10", "35.10", "72.00", "54.00", "53.52", "31.50", "01.00"], "ulrich": [{"code": "4.01", "name": "Alerji / Enfeksiyon"}]},
        "Bronşit (Akut)": {"source": "RAH (Syf 132)", "desc": "Akut öksürük.", "direct": ["43.13"], "compact": ["00.00", "01.00", "02.00", "31.11", "35.10", "70.17", "36.00", "42.60", "43.13", "43.30", "31.50", "01.00"]},
        "Bronşit (Kronik)": {"source": "RAH (Syf 133)", "desc": "Uzun süreli öksürük.", "direct": ["43.14"], "compact": ["00.00", "01.00", "02.00", "31.11", "35.10", "70.17", "36.00", "42.60", "43.14", "43.30", "31.50", "01.00"]},
        "Böbrek Taşı": {"source": "RAH (Syf 140)", "desc": "Nefrolityaz.", "direct": ["45.25"], "compact": ["00.00", "01.00", "02.00", "31.23", "35.10", "44.00", "44.21", "39.65", "45.25", "31.50", "01.00"]},
        "Böbrek Yetmezliği": {"source": "RAH (Syf 137)", "desc": "Böbrek fonksiyon yetersizliği.", "direct": ["45.05"], "compact": ["00.00", "01.00", "02.00", "31.23", "31.87", "35.10", "44.10", "44.17", "70.21", "45.05", "45.80", "31.50", "01.00"]},
        "Cilt Mantarı": {"source": "RAH (Syf 183) + Ulrich 4.05", "desc": "Mikoz enfeksiyonları.", "direct": ["63.50"], "compact": ["00.00", "01.00", "02.00", "30.65", "31.38", "35.10", "70.24", "62.10", "63.50", "31.50", "01.00"], "ulrich": [{"code": "4.05", "name": "Mantar Programı"}]},
        "Cilt Sorunları (Akne)": {"source": "RAH (Syf 181) + Ulrich 4.06", "desc": "Genel cilt problemleri.", "direct": ["63.10"], "compact": ["00.00", "01.00", "02.00", "31.38", "30.65", "35.10", "70.24", "62.10", "63.10", "63.20", "31.50", "01.00"], "ulrich": [{"code": "4.06", "name": "Cilt / Saç"}]},
        "Covid-19 / Long-Covid": {"source": "RAH (Syf 137)", "desc": "Viral enfeksiyon sonrası toparlanma.", "direct": ["43.52"], "compact": ["00.00", "01.00", "02.00", "31.11", "35.10", "22.93", "70.17", "42.70", "43.10", "43.30", "43.50", "43.52", "31.50", "01.00"], "ulrich": [{"code": "90.48", "name": "Enfeksiyon Desteği"}]},
        "Crohn Hastalığı": {"source": "RAH (Syf 146)", "desc": "İnflamatuar bağırsak hastalığı.", "direct": ["47.50"], "compact": ["00.00", "01.00", "02.00", "31.12", "31.16", "31.70", "35.10", "70.19", "46.00", "47.50", "64.55", "72.00", "31.50", "01.00"]},
        "Çakra Dengeleme": {"source": "Ulrich 4.13", "desc": "Enerji merkezleri.", "direct": ["01.40"], "compact": ["00.00", "01.00", "01.40", "01.41", "01.42", "01.43", "01.44", "01.45", "01.46", "01.47", "31.50", "01.00"], "ulrich": [{"code": "4.13", "name": "Fizik Sabitleri / Çakra"}]},
        "DEHB (Dikkat Eksikliği)": {"source": "RAH (Syf 172) + Ulrich 4.04", "desc": "Konsantrasyon.", "direct": ["55.45"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "35.20", "70.10", "54.00", "54.10", "55.45", "64.27", "83.80", "72.00", "31.50", "01.00"], "ulrich": [{"code": "4.04", "name": "Öğrenme Programı"}]},
        "Depresyon": {"source": "RAH (Syf 167) + Ulrich 4.16", "desc": "Ruhsal çöküntü.", "direct": ["72.10"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "48.10", "64.10", "64.28", "64.29", "72.10", "75.10", "31.50", "01.00"], "ulrich": [{"code": "4.16", "name": "Kundalini"}, {"code": "90.58", "name": "Depresyon"}]},
        "Detoks (Genel Arınma)": {"source": "Wellbeing + RAH", "desc": "Tüm sistemlerin temizlenmesi.", "direct": ["31.50", "31.60"], "compact": ["00.00", "01.00", "02.00", "31.50", "31.51", "31.52", "31.60", "31.61", "44.10", "48.10", "36.00", "01.00"], "ulrich": [{"code": "4.14", "name": "Temizleme (Clearing)"}]},
        "Diş Eti İltihabı": {"source": "RAH (Syf 144) + Ulrich 4.11", "desc": "Diş ve çene.", "direct": ["46.20"], "compact": ["00.00", "01.00", "02.00", "31.39", "46.00", "46.10", "46.20", "35.10", "31.50", "01.00"], "ulrich": [{"code": "4.11", "name": "Diş / Çene"}]},
        "Diyabet (Şeker Hastalığı)": {"source": "RAH (Syf 154) + Ulrich 4.19", "desc": "Metabolizma desteği.", "direct": ["51.40"], "compact": ["00.00", "01.00", "02.00", "31.14", "35.10", "70.20", "48.35", "50.20", "51.20", "51.40", "64.70", "31.50", "01.00"], "ulrich": [{"code": "4.19", "name": "Diyabet Programı"}]},
        "Dolaşım Bozukluğu": {"source": "RAH (Syf 125) + Ulrich 4.18", "desc": "Soğuk el/ayak.", "direct": ["39.10"], "compact": ["00.00", "01.00", "02.00", "31.39", "35.10", "38.00", "38.10", "39.10", "31.50", "01.00"], "ulrich": [{"code": "4.18", "name": "Kalp / Dolaşım"}]},
        "Duygusal Denge / İlişki Stresi": {"source": "Ulrich 4.15", "desc": "İlişki kaynaklı stres.", "direct": ["72.00"], "compact": ["00.00", "01.00", "02.00", "72.00", "72.05", "64.00", "31.10", "31.50", "01.00"], "ulrich": [{"code": "4.15", "name": "Partner / İlişki Stresi"}]},
        "Düşük Tansiyon": {"source": "RAH Syf 128 + Ulrich", "desc": "Hipotansiyon.", "direct": ["39.70"], "compact": ["00.00", "01.00", "02.00", "31.39", "35.10", "38.00", "39.50", "39.70", "64.00", "31.50", "01.00"], "ulrich": [{"code": "4.18", "name": "Kalp / Dolaşım"}]},
        "Elektrosmog / Radyasyon": {"source": "Ulrich (4.03) + RAH", "desc": "Elektromanyetik alan.", "direct": ["22.00"], "compact": ["00.00", "01.00", "02.00", "22.00", "22.10", "22.90", "31.10", "31.50", "01.00"], "ulrich": [{"code": "4.03", "name": "Ozon / Radyasyon"}]},
        "Endometriozis": {"source": "RAH (Syf 199)", "desc": "Rahim içi doku.", "direct": ["67.30"], "compact": ["00.00", "01.00", "02.00", "31.20", "31.22", "31.81", "35.10", "70.22", "36.10", "64.80", "65.10", "65.30", "65.31", "65.50", "66.00", "67.30", "72.00", "75.00", "31.50", "01.00"]},
        "Epstein Barr Virüsü (EBV)": {"source": "RAH (Syf 95)", "desc": "Kronik yorgunluk.", "direct": ["16.20"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "16.00", "16.20", "48.10", "36.00", "31.50", "01.00"]},
        "Fibromiyalji": {"source": "RAH (Syf 166) + Ulrich 4.13", "desc": "Yaygın ağrı.", "direct": ["53.84"], "compact": ["00.00", "01.00", "02.00", "31.38", "31.40", "35.10", "70.26", "70.27", "36.00", "52.00", "53.23", "53.25", "53.28", "53.62", "53.84", "62.10", "64.00", "31.50", "01.00"], "ulrich": [{"code": "4.13", "name": "Fizik Sabitleri"}]},
        "Fruktoz İntoleransı": {"source": "RAH (Syf 121)", "desc": "Sindirim bozukluğu.", "direct": ["35.30"], "compact": ["00.00", "01.00", "02.00", "09.34", "31.10", "34.00", "35.10", "35.30", "46.40", "46.50", "47.70", "31.50", "01.00"]},
        "Gastrit / Mide Yanması": {"source": "RAH + Ulrich", "desc": "Mide iltihabı.", "direct": ["47.20"], "compact": ["00.00", "01.00", "02.00", "31.13", "35.10", "70.19", "46.30", "47.20", "47.10", "31.50", "01.00"], "ulrich": [{"code": "4.07", "name": "Asidoz / Mide"}]},
        "Glokom": {"source": "RAH Syf 176", "desc": "Göz tansiyonu.", "direct": ["57.30"], "compact": ["00.00", "01.00", "02.00", "31.31", "35.10", "70.12", "56.00", "56.60", "57.10", "57.30", "31.50", "01.00"]},
        "Göz Kuruluğu": {"source": "RAH Syf 178", "desc": "Gözyaşı kanalı.", "direct": ["57.53"], "compact": ["00.00", "01.00", "02.00", "31.31", "35.10", "70.12", "56.00", "57.53", "31.50", "01.00"]},
        "Grip / Enfeksiyon": {"source": "RAH + Ulrich", "desc": "Viral enfeksiyon.", "direct": ["70.46"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.46", "36.00", "42.10", "43.11", "31.50", "01.00"], "ulrich": [{"code": "4.01", "name": "Alerji/Enfeksiyon"}]},
        "Gut Hastalığı": {"source": "RAH + Ulrich", "desc": "Ürik asit.", "direct": ["51.50"], "compact": ["00.00", "01.00", "02.00", "30.70", "31.10", "35.10", "50.00", "51.10", "51.50", "52.60", "71.11", "71.50", "31.50", "01.00"], "ulrich": [{"code": "4.07", "name": "Asidoz"}]},
        "Hemoroid": {"source": "RAH Syf 148", "desc": "Rektal varis.", "direct": ["47.88"], "compact": ["00.00", "01.00", "02.00", "31.39", "38.50", "39.20", "39.40", "47.88", "31.50", "01.00"], "ulrich": [{"code": "4.18", "name": "Venöz Dolaşım"}]},
        "Herpes (Uçuk)": {"source": "RAH + Ulrich", "desc": "Herpes Simplex.", "direct": ["16.50"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "16.50", "16.51", "63.55", "31.50", "01.00"], "ulrich": [{"code": "4.01", "name": "Enfeksiyon"}]},
        "Hormonal Denge (Kadın)": {"source": "RAH + Ulrich", "desc": "Hormon düzenleme.", "direct": ["65.10"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.22", "64.00", "65.10", "31.50", "01.00"], "ulrich": [{"code": "4.08", "name": "Kadın Hormonları"}]},
        "Hormonal Denge (Erkek)": {"source": "RAH + Ulrich", "desc": "Hormon düzenleme.", "direct": ["65.20"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.23", "64.00", "65.20", "31.50", "01.00"], "ulrich": [{"code": "4.09", "name": "Erkek Hormonları"}]},
        "Hücresel Dejenerasyon (Tümör Desteği)": {"source": "RAH C-Modülü", "desc": "Hücresel destek.", "direct": ["19.00", "19.20", "99.00"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "19.00", "19.20", "99.00", "31.50", "31.60", "01.00"], "ulrich": [{"code": "4.14", "name": "Temizleme"}, {"code": "4.03", "name": "Ozon / Radyasyon"}]},
        "Jetlag / Seyahat": {"source": "Wellbeing", "desc": "Bioritim dengesi.", "direct": ["55.20"], "compact": ["00.00", "01.00", "02.00", "01.40", "55.10", "55.20", "64.11", "31.10", "31.50", "01.00"], "ulrich": [{"code": "4.13", "name": "Fizik Sabitleri"}]},
        "Kabızlık": {"source": "RAH (Syf 148)", "desc": "Bağırsak hareketliliği.", "direct": ["47.86"], "compact": ["00.00", "01.00", "02.00", "31.12", "31.16", "35.10", "70.19", "46.00", "47.86", "31.50", "01.00"]},
        "Karaciğer Detoks": {"source": "RAH + Ulrich", "desc": "Karaciğer temizliği.", "direct": ["48.10"], "compact": ["00.00", "01.00", "02.00", "31.29", "35.10", "70.20", "48.10", "49.10", "31.60", "31.50", "01.00"], "ulrich": [{"code": "4.14", "name": "Temizleme / Detoks"}]},
        "Katarakt": {"source": "RAH (Syf 176)", "desc": "Göz merceği bulanıklığı.", "direct": ["57.20"], "compact": ["00.00", "01.00", "02.00", "31.31", "35.10", "70.12", "56.00", "56.40", "57.20", "31.50", "01.00"]},
        "Kemik Kırığı": {"source": "RAH (Syf 155)", "desc": "Kırık iyileşmesi.", "direct": ["53.11"], "compact": ["00.00", "01.00", "02.00", "31.39", "31.41", "35.10", "70.51", "52.00", "53.11", "31.50", "01.00"]},
        "Kemoterapi Yan Etkileri": {"source": "RAH + Wellbeing", "desc": "Tedavi sonrası temizleme.", "direct": ["31.50", "31.60"], "compact": ["00.00", "01.00", "02.00", "31.10", "31.50", "31.60", "31.61", "22.90", "48.10", "44.10", "35.10", "01.00"], "ulrich": [{"code": "4.14", "name": "Temizleme"}]},
        "Kilo Verme": {"source": "RAH + Ulrich", "desc": "Metabolizma hızlandırma.", "direct": ["75.15"], "compact": ["00.00", "01.00", "02.00", "09.00", "31.10", "36.00", "38.00", "44.00", "46.40", "48.10", "50.00", "64.00", "75.10", "75.15", "31.50", "01.00"], "ulrich": [{"code": "4.19", "name": "Diyabet / Metabolizma"}]},
        "Kronik Yorgunluk (CFS)": {"source": "RAH + Ulrich", "desc": "Sürekli yorgunluk.", "direct": ["16.20"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "16.20", "48.10", "70.10", "31.50", "01.00"], "ulrich": [{"code": "4.16", "name": "Kundalini"}]},
        "Menopoz": {"source": "RAH + Ulrich", "desc": "Klimakterik.", "direct": ["65.60"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.22", "64.10", "64.20", "65.10", "65.60", "66.00", "72.00", "75.00", "31.50", "01.00"], "ulrich": [{"code": "4.08", "name": "Kadın Hormonları"}]},
        "Migren": {"source": "RAH + Ulrich", "desc": "Şiddetli baş ağrısı.", "direct": ["55.60"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.45", "38.10", "39.10", "39.40", "54.10", "54.25", "55.55", "55.60", "64.00", "72.05", "31.50", "01.00"], "ulrich": [{"code": "4.40", "name": "Baş Ağrısı/Migren"}]},
        "Operasyon Sonrası Bakım": {"source": "Dr. Ulrich 4.10", "desc": "İyileşme.", "direct": ["70.63"], "compact": ["00.00", "01.00", "31.80", "31.81", "31.82", "70.63", "35.10", "31.50", "01.00"], "ulrich": [{"code": "4.10", "name": "Op. Sonrası Bakım"}]},
        "Osteoporoz": {"source": "RAH + Ulrich", "desc": "Kemik erimesi.", "direct": ["53.80"], "compact": ["00.00", "01.00", "02.00", "31.41", "35.10", "50.00", "52.00", "52.05", "53.80", "64.00", "64.81", "31.50", "01.00"], "ulrich": [{"code": "4.13", "name": "Fizik Sabitleri"}]},
        "Otizm Spektrum Desteği": {"source": "RAH + Ulrich", "desc": "Detoks ve öğrenme desteği.", "direct": ["31.60", "47.00"], "compact": ["00.00", "01.00", "02.00", "31.60", "31.50", "47.00", "54.00", "35.10", "31.50", "01.00"], "ulrich": [{"code": "4.14", "name": "Temizleme"}, {"code": "4.04", "name": "Öğrenme"}]},
        "Panik Atak": {"source": "RAH + Ulrich", "desc": "Ani korku.", "direct": ["72.05"], "compact": ["00.00", "01.00", "02.00", "31.10", "72.05", "75.10", "54.00", "64.10", "31.50", "01.00"], "ulrich": [{"code": "4.02", "name": "Stres Programı"}]},
        "Parkinson": {"source": "RAH + Ulrich", "desc": "Hareket bozukluğu.", "direct": ["55.31"], "compact": ["00.00", "01.00", "02.00", "31.34", "31.35", "35.10", "70.68", "38.10", "54.00", "55.31", "64.28", "72.00", "75.10", "31.50", "01.00"], "ulrich": [{"code": "4.17", "name": "Parkinson Programı"}]},
        "Prostat Sorunları": {"source": "RAH + Ulrich", "desc": "Prostatit.", "direct": ["69.30"], "compact": ["00.00", "01.00", "02.00", "31.18", "35.10", "70.23", "68.26", "69.10", "69.30", "31.50", "01.00"], "ulrich": [{"code": "4.09", "name": "Erkek Hormonları"}]},
        "Radyasyon / 5G Koruma": {"source": "Ulrich + RAH", "desc": "Elektrosmog.", "direct": ["22.00"], "compact": ["00.00", "01.00", "02.00", "22.00", "22.10", "22.90", "31.10", "31.50", "01.00"], "ulrich": [{"code": "4.03", "name": "Ozon / Radyasyon"}]},
        "Romatizma / Artrit": {"source": "RAH + Ulrich", "desc": "Eklem ağrıları.", "direct": ["53.52"], "compact": ["00.00", "01.00", "02.00", "31.40", "31.41", "35.10", "70.28", "52.00", "53.52", "53.53", "53.54", "31.50", "01.00"], "ulrich": [{"code": "4.13", "name": "Fizik Sabitleri"}]},
        "Sedef (Psoriasis)": {"source": "RAH + Ulrich", "desc": "Cilt pullanması.", "direct": ["63.10"], "compact": ["00.00", "01.00", "02.00", "31.38", "30.65", "35.10", "70.24", "62.10", "62.20", "62.60", "63.10", "72.00", "75.00", "31.50", "01.00"], "ulrich": [{"code": "4.06", "name": "Cilt / Saç"}]},
        "Selülit Tedavisi": {"source": "Wellbeing", "desc": "Bağ dokusu.", "direct": ["62.50"], "compact": ["00.00", "01.00", "02.00", "31.52", "36.00", "37.10", "62.50", "50.00", "31.50", "01.00"], "ulrich": [{"code": "4.07", "name": "Asidoz"}, {"code": "4.14", "name": "Detoks"}]},
        "Sigara Bırakma Destek": {"source": "RAH + Ulrich", "desc": "Nikotin detoksu.", "direct": ["75.16"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "75.16", "75.17", "48.10", "31.50", "01.00"], "ulrich": [{"code": "4.14", "name": "Temizleme"}]},
        "Sınav / İş Performansı": {"source": "Wellbeing + Ulrich", "desc": "Odaklanma.", "direct": ["54.00"], "compact": ["00.00", "01.00", "02.00", "31.10", "54.00", "54.10", "35.20", "64.27", "83.80", "31.50", "01.00"], "ulrich": [{"code": "4.04", "name": "Öğrenme"}]},
        "Sırt Ağrısı": {"source": "RAH + Ulrich", "desc": "Omurga ağrıları.", "direct": ["53.70"], "compact": ["00.00", "01.00", "02.00", "31.40", "35.10", "71.11", "71.50", "52.00", "52.20", "53.23", "53.25", "53.41", "53.70", "72.05", "75.10", "31.50", "01.00"], "ulrich": [{"code": "4.21", "name": "Sırt Ağrısı"}]},
        "Spor Yaralanmaları": {"source": "RAH + Ulrich", "desc": "Travma.", "direct": ["53.21"], "compact": ["00.00", "01.00", "02.00", "31.39", "31.40", "35.10", "53.21", "53.22", "53.24", "31.50", "01.00"], "ulrich": [{"code": "4.22", "name": "Skar / Yara İzi"}]},
        "Stres / Tükenmişlik": {"source": "RAH + Ulrich", "desc": "Sinirsel gerginlik.", "direct": ["75.10"], "compact": ["00.00", "01.00", "02.00", "31.10", "48.10", "50.00", "64.05", "64.10", "64.20", "64.28", "64.29", "64.30", "64.35", "64.40", "64.50", "72.05", "75.10", "31.50", "01.00"], "ulrich": [{"code": "4.02", "name": "Stres Programı"}, {"code": "4.15", "name": "İlişki Stresi"}, {"code": "4.16", "name": "Kundalini"}]},
        "Tinnitus (Çınlama)": {"source": "RAH + Ulrich", "desc": "Kulak çınlaması.", "direct": ["59.10"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.15", "38.10", "39.10", "58.30", "58.40", "59.10", "59.40", "72.00", "75.00", "31.50", "01.00"], "ulrich": [{"code": "4.12", "name": "Tinnitus"}]},
        "Tiroid (Dengesizlik)": {"source": "RAH + Ulrich", "desc": "Tiroid sorunları.", "direct": ["65.33", "65.34"], "compact": ["00.00", "01.00", "02.00", "31.33", "35.10", "70.54", "64.10", "64.20", "64.30", "65.30", "31.50", "01.00"], "ulrich": [{"code": "4.08", "name": "Hormon Programı"}]},
        "Uyku Bozukluğu": {"source": "RAH + Ulrich", "desc": "Uyku sorunu.", "direct": ["55.10"], "compact": ["00.00", "01.00", "02.21", "31.10", "35.10", "70.10", "54.00", "55.10", "64.11", "65.30", "72.00", "75.10", "31.50", "01.00"], "ulrich": [{"code": "4.02", "name": "Stres (Uyku Öncesi)"}]},
        "Vertigo (Baş Dönmesi)": {"source": "RAH + Ulrich", "desc": "Denge kaybı.", "direct": ["55.53"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "54.00", "55.53", "39.10", "31.50", "01.00"], "ulrich": [{"code": "4.02", "name": "Stres / Denge"}]},
        "Yara İzi (Skar) Tedavisi": {"source": "Ulrich + RAH", "desc": "Skar temizliği.", "direct": ["31.81"], "compact": ["00.00", "01.00", "02.00", "31.10", "31.81", "31.80", "70.24", "31.50", "01.00"], "ulrich": [{"code": "4.22", "name": "Skar / Yara İzi"}]},
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

    # --- SIDEBAR (GİZLENDİ) ---
    with st.sidebar:
        st.write("")

    # --- HEADER ---
    c1, c2 = st.columns([1, 5])
    with c1:
        st.markdown("""
        <div class="logo-container">
        """, unsafe_allow_html=True)
        try:
            if os.path.exists("drsaitlogo.jpeg"):
                st.image("drsaitlogo.jpeg", width=90)
        except:
            pass
        st.markdown("</div>", unsafe_allow_html=True)
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
            
            # Metin oluşturma (Kopyalama için)
            share_text = f"🧬 Dr. Sait Sevinç - RAH Protokolü\n\n*Hastalık:* {selected_disease}\n\n*Uygulama Adımları:*\n"
            
            total_minutes = 0
            for step_code in data["compact"]:
                duration = get_duration(step_code)
                cat_class = get_category_class(step_code)
                cat_name = get_category_name(step_code)
                prog_name = get_program_name(step_code)
                if step_code == "00.00": prog_name = "Analiz Hazırlığı"
                
                # Süre Toplama
                try: total_minutes += int(duration.split()[0])
                except: pass
                
                share_text += f"- {step_code} ({prog_name}) - {duration}\n"
                
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
            
            st.success(f"⏱️ **Toplam Süre:** {total_minutes} Dakika")
            
            # Metne Süre Ekleme
            share_text += f"\n⏱️ *Toplam Süre:* {total_minutes} Dakika"

            # AI ASİSTAN & PAYLAŞIM
            st.markdown("---")
            st.markdown("##### 🤖 Asistan & Paylaşım")
            
            # Paylaşım İçeriği
            encoded_text = urllib.parse.quote(share_text + "\n\nSağlıklı günler dileriz.")
            whatsapp_url = f"https://wa.me/?text={encoded_text}"
            
            col_ai1, col_ai2 = st.columns(2)
            with col_ai1:
                 st.markdown(f'<a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">📲 WhatsApp ile Gönder</a>', unsafe_allow_html=True)
            with col_ai2:
                with st.expander("📋 Metni Kopyala"):
                    # HTML KUTUSU (TURKUAZ FİX)
                    st.markdown(f"""
                    <div class="protocol-box">
{share_text}

Sağlıklı günler dileriz.
                    </div>
                    """, unsafe_allow_html=True)

        # --- TAB 2: DOĞRUDAN KODLAR ---
        with tab2:
            st.warning("**Dikkat:** Bu kodlar sadece spesifik hastalık frekanslarıdır.")
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
                
                ulrich_text = f"🧬 *Dr. Ulrich Protokolü ({selected_disease})*\n"
                
                for u_prog in data["ulrich"]:
                    ulrich_text += f"- {u_prog['code']} : {u_prog['name']}\n"
                    st.markdown(f"""
                    <div class="step-row" style="border-left: 5px solid #f1c40f;">
                        <div class="code-pill" style="background-color: #f39c12;">{u_prog['code']}</div>
                        <div style="flex-grow: 1; margin-left: 15px; font-weight: 700; color: #d35400;">
                            {u_prog['name']}
                        </div>
                        <div style="color: #7f8c8d; font-weight: 600;">⏱️ 10-20 dk</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Ulrich Paylaşım
                st.markdown("---")
                encoded_ulrich = urllib.parse.quote(ulrich_text + "\n\nDr. Sait Sevinç Kliniği")
                st.markdown(f'<a href="https://wa.me/?text={encoded_ulrich}" target="_blank" class="whatsapp-btn" style="background-color:#f39c12;">📲 Ulrich Protokolünü Paylaş</a>', unsafe_allow_html=True)

            else:
                st.info("Bu rahatsızlık için özel bir Ulrich protokolü tanımlanmamış.")

    else:
        # Yapay Zeka Sohbet Botu (Sadece Boş Ekranda)
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

            # Basit Kural Tabanlı AI Mantığı
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
        # Yasal Uyarı
        with st.expander("⚠️ Yasal Uyarı"):
            st.caption("Bu uygulama sadece eğitim ve bilgilendirme amaçlıdır. Tıbbi tanı veya tedavi yerine geçmez. RAH ve Ulrich protokolleri destekleyici tamamlayıcı tıp uygulamalarıdır.")

if __name__ == "__main__":
    main()
