import streamlit as st
import requests

# Sahifa sozlamalari
st.set_page_config(
    page_title="Smart RAG Assistant",
    page_icon="🤖",
    layout="wide"
)

# Backend manzili (Lokalda)
API_URL = "http://127.0.0.1:8000"

def main():
    st.title("🤖 Smart RAG Assistant")
    st.markdown("---")

    # 1. Sidebar (Chap menyu)
    with st.sidebar:
        st.header("⚙️ Tizim holati")
        if st.button("Backendni tekshirish"):
            try:
                # Backendga so'rov yuboramiz
                response = requests.get(f"{API_URL}/")
                if response.status_code == 200:
                    st.success("✅ Backend aloqada!")
                    st.json(response.json())
                else:
                    st.error(f"❌ Xatolik: {response.status_code}")
            except requests.exceptions.ConnectionError:
                st.error("❌ Backendga ulanib bo'lmadi. Uvicorn ishlayaptimi?")

    # 2. Asosiy oyna
    st.info("👈 Chap tomondagi menyu orqali tizimni boshqaring.")
    st.write("Hozircha faqat aloqani tekshiryapmiz. Keyingi qadamlarda Chat va Upload qo'shiladi.")

if __name__ == "__main__":
    main()