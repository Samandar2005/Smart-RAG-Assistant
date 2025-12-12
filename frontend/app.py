import streamlit as st
import requests

# 1. Sahifa sozlamalari (Eng tepada turishi shart)
st.set_page_config(
    page_title="Smart RAG Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Backend manzili
API_URL = "http://127.0.0.1:8000"

# --- YORDAMCHI FUNKSIYALAR ---
def clear_history():
    st.session_state.messages = []

def main():
    # --- 2. SESSION STATE (Xotira) ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # --- 3. SIDEBAR (Sozlamalar) ---
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=50)
        st.title("Smart RAG")
        st.markdown("Fayl yuklang va sun'iy intellekt bilan suhbatlashing.")
        st.markdown("---")
        
        # A) Backend Status
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("**Server holati:**")
        with col2:
            if st.button("🔄"):
                pass # Shunchaki qayta yuklash uchun
        
        try:
            if requests.get(f"{API_URL}/", timeout=2).status_code == 200:
                st.success("🟢 Online")
            else:
                st.error("🔴 Offline")
        except:
            st.error("🔴 Offline")

        st.markdown("---")

        # B) Fayl yuklash
        st.subheader("📂 Hujjat yuklash")
        uploaded_file = st.file_uploader("PDF fayl tanlang", type=["pdf"])

        if uploaded_file:
            if st.button("⚡ Bazaga yuklash", use_container_width=True):
                with st.spinner("⏳ Hujjat tahlil qilinmoqda..."):
                    try:
                        files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                        res = requests.post(f"{API_URL}/upload", files=files)
                        if res.status_code == 200:
                            st.toast("✅ Hujjat muvaffaqiyatli qo'shildi!", icon="🎉")
                        else:
                            st.error(f"Xatolik: {res.text}")
                    except Exception as e:
                        st.error(f"Ulanish xatosi: {e}")
        
        st.markdown("---")
        
        # C) Chatni tozalash (YANGI)
        if st.button("🗑️ Suhbatni tozalash", on_click=clear_history, use_container_width=True):
            st.toast("Chat tarixi tozalandi", icon="🧹")

        st.markdown("---")
        st.caption("Developed by Samandar Bo'riyev")

    # --- 4. ASOSIY CHAT OYNASI ---
    st.header("🧠 Smart RAG Assistant")
    
    # Agar chat bo'sh bo'lsa - Welcome Message
    if not st.session_state.messages:
        st.info("👋 Salom! Chap tomondagi menyu orqali PDF yuklang va savol berishni boshlang.")

    # Tarixni chiqarish
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Yangi xabar
    if prompt := st.chat_input("Savolingizni yozing..."):
        
        # User xabari
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI Javobi
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Validating...")
            
            try:
                payload = {"question": prompt}
                response = requests.post(f"{API_URL}/chat", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    ai_answer = data.get("answer", "Javob yo'q")
                    sources = data.get("sources", [])
                    
                    # Javobni yozish
                    message_placeholder.markdown(ai_answer)
                    
                    # Manbalarni ko'rsatish
                    if sources:
                        with st.expander("📚 Manbalar (Context)"):
                            for idx, source in enumerate(sources):
                                st.markdown(f"**{idx+1}-manba:**\n> {source}")
                    
                    # Tarixga qo'shish
                    st.session_state.messages.append({"role": "assistant", "content": ai_answer})
                else:
                    message_placeholder.error(f"Server xatosi: {response.text}")
            
            except Exception as e:
                message_placeholder.error(f"Ulanish xatosi: {e}")

if __name__ == "__main__":
    main()