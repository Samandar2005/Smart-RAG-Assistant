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
    
    # --- 1. SESSION STATE (Xotira) ---
    # Agar chat tarixi mavjud bo'lmasa, bo'sh ro'yxat ochamiz
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # --- 2. SIDEBAR (Fayl yuklash) ---
    with st.sidebar:
        st.header("⚙️ Sozlamalar")
        
        # Backend check
        if st.button("Backendni tekshirish"):
            try:
                if requests.get(f"{API_URL}/").status_code == 200:
                    st.success("✅ Backend aloqada!")
                else:
                    st.error("❌ Xatolik")
            except:
                st.error("❌ Ulanib bo'lmadi")

        st.markdown("---")
        st.subheader("📄 Hujjat yuklash")
        uploaded_file = st.file_uploader("PDF fayl tanlang", type=["pdf"])

        if uploaded_file and st.button("Bazaga yuklash"):
            with st.spinner("⏳ Tahlil qilinmoqda..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                    res = requests.post(f"{API_URL}/upload", files=files)
                    if res.status_code == 200:
                        st.success("✅ Hujjat qo'shildi!")
                    else:
                        st.error(f"Xatolik: {res.text}")
                except Exception as e:
                    st.error(f"Xatolik: {e}")

    # --- 3. CHAT INTERFEYSI (Asosiy qism) ---
    
    # A) Eski xabarlarni chiqarish (History)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # B) Yangi xabar yozish (Input)
    if prompt := st.chat_input("Hujjat bo'yicha savol bering..."):
        
        # 1. Foydalanuvchi xabarini ko'rsatish va saqlash
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 2. AI dan javob olish
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Biroz kuting...")
            
            try:
                # Backendga so'rov (POST /chat)
                payload = {"question": prompt}
                response = requests.post(f"{API_URL}/chat", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    ai_answer = data.get("answer", "Javob yo'q")
                    sources = data.get("sources", [])
                    
                    # Javobni chiqarish
                    message_placeholder.markdown(ai_answer)
                    
                    # Agar manbalar bo'lsa, pastda chiroyli qilib ko'rsatish
                    if sources:
                        with st.expander("📚 Foydalanilgan manbalar (Kontekst)"):
                            for source in sources:
                                st.caption(source)
                    
                    # AI javobini tarixga saqlash
                    st.session_state.messages.append({"role": "assistant", "content": ai_answer})
                
                else:
                    message_placeholder.error(f"Server xatosi: {response.text}")
            
            except Exception as e:
                message_placeholder.error(f"Ulanish xatosi: {e}")

if __name__ == "__main__":
    main()