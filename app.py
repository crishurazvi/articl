import streamlit as st
import yt_dlp
import os
import glob
import math

# --- CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="AI Debate & Summary", page_icon="🧠")
st.title("🧠 Analizator Universal (Video & Text)")

# --- SELECTOR DE MOD ---
mod_lucru = st.radio("Ce vrei să analizezi?", ["📺 Video YouTube", "📝 Text / Postare Facebook / Articol"])

# --- CONFIGURĂRI GENERALE ---
st.write("🔧 **Setări:**")
CHUNK_SIZE = st.slider("Mărime bucată (caractere)", 2000, 30000, 15000, 1000)

# --- PROMPTURI INTELIGENTE ---
PROMPT_VIDEO = """
Ești un analist expert. Analizează acest transcript (Partea {part}/{total}) și așteaptă continuarea.
La final, livrează în ROMÂNĂ:
1. REZUMAT EXECUTIV.
2. IDEI PRINCIPALE.
3. CONCLUZIE PRACTICĂ.
"""

PROMPT_DEBATE = """
Ești un moderator de dezbateri expert și un logician desăvârșit.
Analizează textul furnizat mai jos (care poate fi o postare Facebook, un articol sau o opinie) și realizează următoarele în limba ROMÂNĂ:

1. 🕵️‍♂️ VERIFICAREA FAPTELOR (Fact-Check): Există afirmații dubioase?
2. 🥊 DEZBATERE (PRO vs CONTRA): Prezintă argumentele autorului și contra-argumente solide.
3. ⚖️ ANALIZĂ LOGICĂ: Identifică erori de logică (sofisme) sau manipulare emoțională.
4. 📝 REZUMAT IMPARȚIAL.

Iată textul de analizat:
--------------------------------------------------
"""

# ==========================================
# LOGICA PENTRU YOUTUBE
# ==========================================
if mod_lucru == "📺 Video YouTube":
    url = st.text_input("Lipește Link-ul YouTube:")
    
    if st.button("Extrage și Pregătește"):
        if not url:
            st.warning("Pune un link!")
        else:
            status = st.empty()
            status.info("⏳ Descarc subtitrarea...")
            
            options = {
                'skip_download': True,
                'writeautomaticsub': True,
                'writesubtitles': True,
                'subtitleslangs': ['en', 'ro'], # Încercăm și RO și EN
                'outtmpl': 'temp_stream',
                'quiet': True,
                'no_warnings': True
            }

            try:
                for f in glob.glob("temp_stream*"): 
                    try: os.remove(f)
                    except: pass

                with yt_dlp.YoutubeDL(options) as ydl:
                    ydl.download([url])

                files = glob.glob("temp_stream*.vtt")
                
                if files:
                    filename = files[0]
                    with open(filename, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    full_text_list = []
                    seen = set()
                    for line in lines:
                        line = line.strip()
                        if "-->" in line or line == "WEBVTT" or not line: continue
                        if line.startswith("<") and line.endswith(">"): continue
                        if "<" in line and ">" in line:
                            import re
                            line = re.sub(r'<[^>]+>', '', line)
                        if line in seen: continue
                        seen.add(line)
                        full_text_list.append(line)

                    whole_text = " ".join(full_text_list)
                    
                    # Logica de împărțire (Chunking)
                    num_chunks = math.ceil(len(whole_text) / CHUNK_SIZE)
                    
                    status.success(f"✅ Transcript extras! ({len(whole_text)} caractere)")
                    st.markdown("---")
                    
                    for i in range(num_chunks):
                        start = i * CHUNK_SIZE
                        end = start + CHUNK_SIZE
                        chunk = whole_text[start:end]
                        
                        header = PROMPT_VIDEO.format(part=i+1, total=num_chunks)
                        final_block = header + "\n" + chunk
                        
                        st.subheader(f"🔹 Partea {i+1}")
                        st.code(final_block, language=None)
                        st.markdown("---")

                    os.remove(filename)
                else:
                    status.error("Nu am găsit subtitrări (YouTube nu le are sau link-ul e greșit).")
            except Exception as e:
                status.error(f"Eroare: {str(e)}")

# ==========================================
# LOGICA PENTRU FACEBOOK / TEXT
# ==========================================
elif mod_lucru == "📝 Text / Postare Facebook / Articol":
    st.info("Pentru Facebook/Știri: Copiază textul manual și lipește-l aici. Eu voi crea prompt-ul perfect pentru AI.")
    
    raw_text = st.text_area("Lipește textul aici:", height=300)
    
    if st.button("Generează Analiza DEBATE"):
        if not raw_text:
            st.warning("Nu ai lipit niciun text.")
        else:
            # Aici nu mai avem nevoie neapărat de chunking complex dacă textul e mic,
            # dar îl păstrăm pentru articole foarte lungi.
            num_chunks = math.ceil(len(raw_text) / CHUNK_SIZE)
            
            st.success(f"✅ Text procesat! Pregătit pentru dezbatere.")
            st.markdown("---")
            
            for i in range(num_chunks):
                start = i * CHUNK_SIZE
                end = start + CHUNK_SIZE
                chunk = raw_text[start:end]
                
                # Dacă e o singură bucată, punem promptul direct
                # Dacă sunt mai multe, i-am putea spune AI-ului să aștepte, 
                # dar pentru debate e mai bine să analizeze tot odată dacă încape.
                
                final_block = PROMPT_DEBATE + "\n" + chunk
                
                st.subheader(f"🔹 Analiză Debate (Partea {i+1})")
                st.caption("Copiază asta în ChatGPT/Gemini:")
                st.code(final_block, language=None)
                st.markdown("---")
