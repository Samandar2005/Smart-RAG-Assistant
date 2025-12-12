import streamlit as st
import requests

# Sahifa sozlamalari
st.set_page_config(
    page_title="Smart RAG Assistant",
    page_icon="🤖",
    layout="wide"
)

# Backend manzili
API_URL = "http://127.0.0.1:8000"

def main():
    st.title("🤖 Smart RAG Assistant")
    st.markdown("---")

    # --- SIDEBAR: Fayl yuklash va Sozlamalar ---
    with st.sidebar:
        st.header("⚙️ Sozlamalar")
        
        # 1. Tizim holatini tekshirish
        if st.button("Backend aloqasini tekshirish"):
            try:
                response = requests.get(f"{API_URL}/")
                if response.status_code == 200:
                    st.success("✅ Backend aloqada!")
                else:
                    st.error(f"❌ Xatolik: {response.status_code}")
            except requests.exceptions.ConnectionError:
                st.error("❌ Backendga ulanib bo'lmadi!")

        st.markdown("---")
        
        # 2. Fayl yuklash qismi (YANGI QO'SHILDI)
        st.subheader("📄 Hujjat yuklash")
        uploaded_file = st.file_uploader("PDF fayl tanlang", type=["pdf"])

        if uploaded_file is not None:
            # Yuklash tugmasi
            if st.button("Faylni bazaga yuklash"):
                with st.spinner("⏳ Fayl o'qilmoqda va vektorga aylantirilmoqda..."):
                    try:
                        # Faylni backendga yuborish uchun tayyorlaymiz
                        files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                        
                        # POST so'rov yuborish
                        response = requests.post(f"{API_URL}/upload", files=files)
                        
                        if response.status_code == 200:
                            st.success("✅ Muvaffaqiyatli! Hujjat bilimlar bazasiga qo'shildi.")
                            st.json(response.json()) # API javobini ko'rsatish
                        else:
                            st.error(f"❌ Xatolik yuz berdi: {response.text}")
                            
                    except Exception as e:
                        st.error(f"❌ Ulanishda xatolik: {e}")

    # --- MAIN AREA: Hozircha bo'sh ---
    st.info("👈 Chap tomondagi menyu orqali PDF fayl yuklang. Keyingi qadamda Chat paydo bo'ladi.")

if __name__ == "__main__":
    main()