import streamlit as st

st.set_page_config(layout="wide", page_title="Rüzgar Enerjisi", page_icon="⚡")
st.sidebar.markdown("<div style='position: fixed; top: 0; padding: 20px;'></div>", unsafe_allow_html=True)
st.sidebar.image("img/BZDAY.jpg", use_column_width=True)

image_path = "img/Roadmap.jpg"
col1, col2, col3 = st.columns((1,2,1))
col2.title("Yol Haritası 🗺️")

col2.write("<div style='text-align:center'>", unsafe_allow_html=True)
col2.image(image_path, caption='Yol Haritası', width=400)
col2.write("</div>", unsafe_allow_html=True)
