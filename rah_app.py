import streamlit as st
import pandas as pd
import os

# =============================================================================
# 1. GÖRSEL TASARIM (ULTIMATE CSS FIX)
# =============================================================================
def local_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');
    
    /* --- 1. TEMEL AYARLAR (ZORUNLU BEYAZ MOD) --- */
    [data-testid="stAppViewContainer"] {
        background-color: #fdfdfd !important;
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, p, div, span, label {
        color: #2c3e50; /* Koyu gri/lacivert yazı rengi - Okunabilirlik için */
    }

    /* --- 2. SIDEBAR (SOL MENÜ) DÜZELTMESİ --- */
    [data-testid="stSidebar"] {
        background-color: #f4f6f8 !important;
        border-right: 1px solid #e0e0e0;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #2c3e50 !important;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span {
        color: #34495e !important; /* Sidebar yazıları kesinlikle koyu renk */
    }
    /* Radio Button Düzeltmesi */
    div[role="radiogroup"] label {
        color: #333 !important;
    }

    /* --- 3. SEKMELER (TABS) - SORUN 2 ÇÖZÜMÜ --- */
    /* Sekme Konteynerı */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        padding-bottom: 5px;
    }
    /* Pasif (Seçili Olmayan) Sekme */
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #e9ecef !important; /* Açık Gri Arkaplan */
        color: #495057 !important; /* Koyu Gri Yazı - ARTIK GÖRÜNÜR! */
        border-radius: 8px;
        border: 1px solid #dee2e6;
        font-weight: 600;
        padding: 0 20px;
        transition: all 0.3s ease;
    }
    /* Aktif (Seçili) Sekme */
    .stTabs [aria-selected="true"] {
        background-color: #2980b9 !important; /* Ana Renk */
        color: #ffffff !important; /* Beyaz Yazı */
        border: 1px solid #2980b9;
        box-shadow: 0 4px 6px rgba(41, 128, 185, 0.2);
    }
    /* Üzerine Gelince (Hover) */
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #dbe2ef !important;
        color: #2980b9 !important;
    }

    /* --- 4. AÇILIR KUTU (SELECTBOX) - SORUN 1 ÇÖZÜMÜ --- */
    /* Kutunun kendisi */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 2px solid #e0e0e0 !important;
        color: #333 !important;
        border-radius: 8px;
    }
    /* Kutunun içindeki yazı */
    div[data-baseweb="select"] span {
        color: #333 !important;
    }
    /* Ok işareti */
    div[data-baseweb="select"] svg {
        fill: #333 !important;
    }
    /* Açılan Liste (Dropdown Menü) */
    ul[data-baseweb="menu"] {
        background-color: #ffffff !important;
    }
    li[role="option"] {
        color: #333 !important; /* Liste elemanları siyah */
        background-color: #fff !important;
    }
    li[role="option"]:hover, li[aria-selected="true"] {
        background-color: #e3f2fd !important; /* Seçili/Hover mavi */
        color: #1565c0 !important;
        font-weight: bold;
    }

    /* --- 5. HEADER VE KART TASARIMLARI --- */
    .header-box {
        background: linear-gradient(120deg, #2980b9, #2c3e50);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 25px -5px rgba(44, 62, 80, 0.3);
        margin-bottom: 30px;
        border-bottom: 6px solid #f39c12; /* Dr. Sait Turuncusu */
    }
    .header-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        color: white !important;
        letter-spacing: -1px;
    }
    
    .disease-info-card {
        background: #fff;
        border: 1px solid #eee;
        border-left: 6px solid #f39c12;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }

    /* --- 6. TIMELINE GÖRÜNÜMÜ --- */
    .timeline-step {
        display: flex;
        align-items: center;
        background: #fff;
        border: 1px solid #f0f2f5;
        margin-bottom: 10px;
        padding: 12px 15px;
        border-radius: 10px;
        transition: transform 0.2s;
    }
    .timeline-step:hover {
        transform: translateX(5px);
        border-color: #2980b9;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .step-code {
        background-color: #2c3e50;
        color: #fff !important;
        font-family: 'Courier New', monospace;
        font-weight: 700;
        padding: 6px 12px;
        border-radius: 6px;
        min-width: 85px;
        text-align: center;
        margin-right: 15px;
        font-size: 1.1rem;
    }
    
    /* Etiketler */
    .badge { padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; color: white !important; margin-left: auto; }
    .b-blue { background-color: #3498db; }
    .b-green { background-color: #27ae60; }
    .b-purple { background-color: #9b59b6; }
    .b-red { background-color: #e74c3c; }
    .b-orange { background-color: #e67e22; }

    /* Ulrich Kartı */
    .ulrich-box {
        background-color: #fff8e1;
        border: 2px solid #ffecb3;
        padding: 20px;
        border-radius: 12px;
        color: #5d4037 !important;
    }

    /* Gizleme */
    .stDeployButton, header, footer {visibility: hidden;}
    .custom-footer {
        text-align: center; margin-top: 50px; color: #bdc3c7; font-size: 0.8rem; border-top: 1px solid #eee; padding-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# 2. VERİTABANI (TAM KAPSAM)
# =============================================================================
def get_rah_database():
    # Source 2: Syf 104-207 + Ulrich Modülü
    db = {
        # --- 1. BAĞIŞIKLIK ---
        "Alerji (Genel)": {"source": "Source 2, Syf 121 & Ulrich", "desc": "Alerjik reaksiyonlar ve histamin dengesi.", "direct": ["35.20", "64.27"], "compact": ["00.00", "01.00", "02.00", "31.10", "34.00", "35.10", "35.20", "36.00", "64.27", "31.50", "01.00"], "ulrich": [{"code": "90.38", "name": "Alerji Tedavisi"}]},
        "Grip (Influenza)": {"source": "Source 2, Syf 82 & Ulrich", "desc": "Viral enfeksiyonlar ve grip.", "direct": ["70.46", "43.11"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.46", "36.00", "42.10", "43.11", "31.50", "01.00"], "ulrich": [{"code": "90.48", "name": "Grip / Enfeksiyon"}]},
        "Bağışıklık Güçlendirme": {"source": "Source 2, Syf 121 & Ulrich", "desc": "Genel savunma sistemi.", "direct": ["35.10"], "compact": ["00.00", "01.00", "02.00", "31.10", "34.00", "35.10", "35.11", "36.50", "31.50", "01.00"], "ulrich": [{"code": "90.56", "name": "Bağışıklık Sistemi"}]},
        
        # --- 2. SİNİR SİSTEMİ ---
        "Migren": {"source": "Source 2, Syf 175 & Ulrich", "desc": "Şiddetli baş ağrısı tedavisi.", "direct": ["55.60", "55.55"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.45", "38.10", "39.10", "39.40", "54.10", "54.25", "55.55", "55.60", "64.00", "31.50", "01.00"], "ulrich": [{"code": "90.40", "name": "Migren / Baş Ağrısı"}]},
        "Depresyon": {"source": "Source 2, Syf 167 & Ulrich", "desc": "Ruhsal denge ve vitalite.", "direct": ["72.10", "72.00"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "48.10", "64.10", "64.28", "64.29", "72.10", "75.10", "31.50", "01.00"], "ulrich": [{"code": "90.58", "name": "Depresyon / Ruhsal Denge"}]},
        "Uyku Bozukluğu": {"source": "Source 2, Syf 168 & Ulrich", "desc": "Uykuya dalma sorunları.", "direct": ["55.10", "55.20"], "compact": ["00.00", "01.00", "02.21", "31.10", "35.10", "70.10", "54.00", "55.10", "64.11", "65.30", "72.00", "75.10", "31.50", "01.00"], "ulrich": [{"code": "90.59", "name": "Stres / Gevşeme"}]},
        "Stres Azaltma": {"source": "Source 2, Syf 207 & Ulrich", "desc": "Sinirsel gerginlik ve rahatlama.", "direct": ["75.10", "72.05"], "compact": ["00.00", "01.00", "02.00", "31.10", "48.10", "50.00", "64.05", "64.10", "72.05", "75.10", "31.50", "01.00"], "ulrich": [{"code": "90.57", "name": "Vejetatif Dystoni"}]},

        # --- 3. KAS & İSKELET ---
        "Romatizma / Artrit": {"source": "Source 2, Syf 160 & Ulrich", "desc": "Eklem iltihabı ve ağrıları.", "direct": ["53.52", "53.53"], "compact": ["00.00", "01.00", "02.00", "31.40", "31.41", "35.10", "70.28", "52.00", "53.52", "53.53", "53.54", "31.50", "01.00"], "ulrich": [{"code": "90.62", "name": "Romatizma"}]},
        "Sırt Ağrısı": {"source": "Source 2, Syf 163 & Ulrich", "desc": "Omurga ve bel ağrıları.", "direct": ["53.70", "53.73"], "compact": ["00.00", "01.00", "02.00", "31.40", "35.10", "71.11", "71.50", "52.00", "53.70", "53.73", "72.05", "31.50", "01.00"], "ulrich": [{"code": "90.64", "name": "Sırt Ağrısı / Omurga"}]},
        "Osteoporoz": {"source": "Source 2, Syf 165 & Ulrich", "desc": "Kemik erimesi.", "direct": ["53.80"], "compact": ["00.00", "01.00", "02.00", "31.41", "35.10", "50.00", "52.00", "52.05", "53.80", "64.00", "64.81", "31.50", "01.00"], "ulrich": [{"code": "90.63", "name": "Kemik Metabolizması"}]},

        # --- 4. KALP & DOLAŞIM ---
        "Yüksek Tansiyon": {"source": "Source 2, Syf 127 & Ulrich", "desc": "Kan basıncı regülasyonu.", "direct": ["39.60", "70.47"], "compact": ["00.00", "01.00", "02.00", "31.39", "35.10", "70.47", "38.00", "39.10", "39.40", "39.50", "39.60", "64.00", "31.50", "01.00"], "ulrich": [{"code": "90.22", "name": "Hipertansiyon"}]},
        "Dolaşım Bozukluğu": {"source": "Source 2, Syf 125 & Ulrich", "desc": "Genel dolaşım sorunları.", "direct": ["39.10"], "compact": ["00.00", "01.00", "02.00", "31.39", "35.10", "38.00", "38.10", "39.10", "31.50", "01.00"], "ulrich": [{"code": "90.20", "name": "Dolaşım / Kalp"}]},

        # --- 5. SİNDİRİM ---
        "Gastrit": {"source": "Source 2, Syf 143 & Ulrich", "desc": "Mide iltihabı ve yanması.", "direct": ["47.20", "47.10"], "compact": ["00.00", "01.00", "02.00", "31.13", "35.10", "70.19", "46.30", "47.20", "47.10", "31.50", "01.00"], "ulrich": [{"code": "90.30", "name": "Mide / Bağırsak"}]},
        "Karaciğer Detoks": {"source": "Source 2, Syf 149 & Ulrich", "desc": "Karaciğer fonksiyonu ve temizlik.", "direct": ["48.10", "31.60"], "compact": ["00.00", "01.00", "02.00", "31.29", "35.10", "70.20", "48.10", "49.10", "31.60", "31.50", "01.00"], "ulrich": [{"code": "90.32", "name": "Karaciğer / Safra"}]},
        "Diyabet": {"source": "Source 2, Syf 154 & Ulrich", "desc": "Şeker hastalığı.", "direct": ["51.40"], "compact": ["00.00", "01.00", "02.00", "31.14", "35.10", "70.20", "48.35", "50.20", "51.20", "51.40", "64.70", "31.50", "01.00"], "ulrich": [{"code": "90.54", "name": "Metabolizma / Diyabet"}]},

        # --- 6. DİĞER ---
        "Cilt Sorunları (Akne)": {"source": "Source 2, Syf 181 & Ulrich", "desc": "Cilt problemleri.", "direct": ["63.10", "63.20"], "compact": ["00.00", "01.00", "02.00", "31.38", "30.65", "35.10", "70.24", "62.10", "63.10", "63.20", "31.50", "01.00"], "ulrich": [{"code": "90.36", "name": "Cilt / Saç / Tırnak"}]},
        "Hormonal Denge (Kadın)": {"source": "Source 2, Syf 186 & Ulrich", "desc": "Menstruasyon ve menopoz.", "direct": ["65.10", "65.60"], "compact": ["00.00", "01.00", "02.00", "31.10", "35.10", "70.22", "64.00", "65.10", "65.60", "31.50", "01.00"], "ulrich": [{"code": "90.42", "name": "Hormonal Düzenleme (Kadın)"}]},
        "Prostat Sorunları": {"source": "Source 2, Syf 200 & Ulrich", "desc": "Prostatit ve büyüme.", "direct": ["69.30", "69.10"], "compact": ["00.00", "01.00", "02.00", "31.18", "35.10", "70.23", "68.26", "69.10", "69.30", "31.50", "01.00"], "ulrich": [{"code": "90.43", "name": "Hormonal Düzenleme (Erkek)"}]}
    }
    return db

def get_program_name(code):
    names = {
        "00.00": "Analiz Hazırlığı", "01.00": "Vitalizasyon Komple", "02.00": "Akupunktur Meridyenleri",
        "31.10": "ATP Üretimi Komple", "31.50": "Temel Detoksifikasyon", "35.10": "Bağışıklık Artırma",
        "70.45": "Migren, Patojen Odaklı", "70.47": "Kan Basıncı Düşürme"
    }
    if code in names: return names[code]
    if code.startswith("70."): return "Sistem Tedavisi (Kombine)"
    return f"RAH Programı {code}"

def get_category_class(code):
    if code.startswith("01.") or code.startswith("02."): return "b-blue" 
    if code.startswith("31.5") or code.startswith("31.6"): return "b-green" 
    if code.startswith("70."): return "b-purple" 
    return "b-red" 

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
        st.caption("v7.0 - Final Stable")
        st.markdown("---")
        
        st.markdown("#### ⚙️ Cihaz Ayarı")
        device = st.radio("Cihaz Seçimi:", ["Rayocomp PS 10", "Rayocomp PS 1000"], label_visibility="collapsed")
        
        if device == "Rayocomp PS 10":
            st.info("**PS 10 Modu:** Kodları manuel girin veya Green Card kullanın.")
        else:
            st.success("**PS 1000 Modu:** Otomatik menüden seçin.")

    # --- MAIN CONTENT ---
    st.markdown("""
    <div class="header-box">
        <div class="header-title">🧬 RAH Biyorezonans Asistanı</div>
        <div style="font-size:1rem; opacity:0.8; margin-top:5px;">Profesyonel Terapi Protokolleri & Kod Rehberi</div>
    </div>
    """, unsafe_allow_html=True)
    
    db = get_rah_database()
    
    # Arama Kutusu
    st.markdown('<h3 style="color:#2c3e50;">🔎 Rahatsızlık Seçimi</h3>', unsafe_allow_html=True)
    disease_list = sorted(db.keys())
    selected_disease = st.selectbox("Listeden seçim yapınız:", [""] + disease_list, label_visibility="collapsed")

    if selected_disease:
        data = db[selected_disease]
        
        st.markdown(f"""
        <div class="disease-info-card">
            <h2 style="color:#2c3e50; margin-top:0;">📌 {selected_disease}</h2>
            <p style="font-size:1.1rem; color:#555;">{data['desc']}</p>
            <small style="color:#888;">📚 <b>Kaynak:</b> {data['source']}</small>
        </div>
        """, unsafe_allow_html=True)

        # Sekmeler
        tab1, tab2, tab3 = st.tabs(["🚀 Kompakt Protokol (RAH)", "⚡ Doğrudan Kodlar", "🧬 Ulrich Protokolü"])

        # --- TAB 1: RAH KOMPAKT ---
        with tab1:
            st.info("**Önerilen Yöntem:** Bu sıralama, cihazın 'Kompakt Programlar' mantığına göre (Hazırlık > Tedavi > Detoks) düzenlenmiştir.")
            
            for step_code in data["compact"]:
                cat_class = get_category_class(step_code)
                cat_name = get_category_name(step_code)
                prog_name = get_program_name(step_code)
                if step_code == "00.00": prog_name = "Analiz Hazırlığı"
                duration = "10 dk" if step_code.startswith("70.") else "5 dk"
                
                st.markdown(f"""
                <div class="timeline-step">
                    <div class="step-code">{step_code}</div>
                    <div style="flex-grow:1; font-weight:600; color:#34495e;">{prog_name}</div>
                    <span class="badge {cat_class}">{cat_name}</span>
                    <div style="margin-left:15px; font-size:0.85rem; color:#7f8c8d; font-weight:bold;">⏱️ {duration}</div>
                </div>
                """, unsafe_allow_html=True)

        # --- TAB 2: DOĞRUDAN KODLAR ---
        with tab2:
            st.warning("Bu kodlar sadece spesifik hastalık frekanslarıdır. Enerji dengelemesi içermez.")
            cols = st.columns(4)
            for i, code in enumerate(data["direct"]):
                with cols[i % 4]:
                    st.metric(label=f"Kod {i+1}", value=code)

        # --- TAB 3: ULRICH ---
        with tab3:
            if "ulrich" in data:
                st.markdown("""
                <div class="ulrich-box">
                    <b>ℹ️ Dr. Elmar Ulrich Modülü (M4):</b> Bu programlar, özel sistem kartları veya 90.00 serisi içinde yer alır.
                </div><br>
                """, unsafe_allow_html=True)
                
                for u in data["ulrich"]:
                    st.markdown(f"""
                    <div class="timeline-step" style="border-left: 5px solid #f1c40f;">
                        <div class="step-code" style="background-color:#f39c12;">{u['code']}</div>
                        <div style="flex-grow:1; font-weight:700; color:#d35400;">{u['name']}</div>
                        <div style="color:#7f8c8d; font-weight:bold;">⏱️ 10-20 dk</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Bu rahatsızlık için özel bir Ulrich protokolü tanımlanmamış.")

    else:
        st.markdown('<div class="custom-footer">Developed for Dr. Sait Sevinç © 2025</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
