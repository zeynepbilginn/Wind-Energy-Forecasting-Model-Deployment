import streamlit as st

st.set_page_config(page_title = "Rüzgar Enerjisi",page_icon = "⚡")
st.sidebar.markdown("<div style='position: fixed; top: 0; padding: 20px;'></div>", unsafe_allow_html=True)
st.sidebar.image("img/BZDAY.jpg", use_column_width=True)

kisiler = [
    {"ad": "Tutku Deniz Kayacan", "pozisyon": "Veri Bilimci", "github": "https://github.com/deniz-kayacan", "linkedin": "https://www.linkedin.com/in/deniz-kayacan-16663a292/", "foto": "img/Deniz.png"},
    {"ad": "Asya Aleyna Yılmaz", "pozisyon": "Veri Bilimci", "github": "https://github.com/asyaaleyna", "linkedin": "www.linkedin.com/in/asyaaleynayilmaz", "foto": "img/Asya.png"},
    {"ad": "Zeynep Bilgin", "pozisyon": "Veri Bilimci", "github": "https://github.com/zeynepbilginn", "linkedin": "https://www.linkedin.com/in/zeynep-bilgin4268/", "foto": "img/Zeynep.png"},
    {"ad": "Büşra Demir", "pozisyon": "Veri Bilimci", "github": "https://github.com/Vegastarr", "linkedin": "https://www.linkedin.com/in/busraerim/", "foto": "img/Busra.png"},
    {"ad": "Yağmur Bulkur", "pozisyon": "Veri Bilimci", "github": "https://github.com/yagmurbulkur", "linkedin": "https://www.linkedin.com/in/yağmur-bulkur1/", "foto": "img/Yagmur.jpeg"}
]

# Her iki kişi için yan yana kart oluşturma fonksiyonu
def iki_kisi_karti(kisi1, kisi2):
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"## {kisi1['ad']}")
        st.image(kisi1['foto'], caption=kisi1['ad'], use_column_width=True)
        st.write(f"**Pozisyon:** {kisi1['pozisyon']}")
        st.write(f"GitHub: [{kisi1['github']}]({kisi1['github']})")
        st.write(f"LinkedIn: [{kisi1['linkedin']}]({kisi1['linkedin']})")

    if kisi2 is not None:
        with col2:
            st.write(f"## {kisi2['ad']}")
            st.image(kisi2['foto'], caption=kisi2['ad'], use_column_width=True)
            st.write(f"**Pozisyon:** {kisi2['pozisyon']}")
            st.write(f"GitHub: [{kisi2['github']}]({kisi2['github']})")
            st.write(f"LinkedIn: [{kisi2['linkedin']}]({kisi2['linkedin']})")

# Her iki kişi için yan yana kartları oluştur
for i in range(0, len(kisiler), 2):
    iki_kisi_karti(kisiler[i], kisiler[i+1] if i+1 < len(kisiler) else None)
