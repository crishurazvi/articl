import streamlit as st
import math

# --- CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="TXT Splitter AI", page_icon="📄")
st.title("📄 TXT File Splitter pentru AI")
st.info("Încarcă un fișier text lung (cărți, documente, notițe) și împarte-l în bucăți digerabile pentru ChatGPT/Claude/Gemini.")

# --- SETĂRI ---
with st.expander("⚙️ Setări Avansate", expanded=True):
    CHUNK_SIZE = st.slider(
        "Mărime bucată (caractere)", 
        min_value=2000, 
        max_value=50000, 
        value=15000, 
        step=1000,
        help="15.000 este ideal pentru ChatGPT Free. 30.000+ merge pentru Gemini 1.5 Pro."
    )
    
    # Aici poți modifica ce îi spui AI-ului la începutul fiecărei bucăți
    CUSTOM_PROMPT = st.text_area(
        "Instrucțiuni pentru AI (Prompt):",
        value="""Ești un asistent expert. Analizează acest text (PARTEA {part} din {total}) și așteaptă următoarea parte.
Dacă aceasta este ultima parte, te rog să generezi un REZUMAT DETALIAT și IDEILE PRINCIPALE în limba ROMÂNĂ.

Textul de analizat:
-------------------"""
    )

# --- ZONA DE ÎNCĂRCARE ---
uploaded_file = st.file_uploader("Alege un fișier .txt", type="txt")

if uploaded_file is not None:
    try:
        # Citim fișierul. 'utf-8' este standardul, dar uneori fișierele vechi sunt 'latin-1'
        string_data = uploaded_file.read().decode("utf-8")
        
        total_chars = len(string_data)
        num_chunks = math.ceil(total_chars / CHUNK_SIZE)
        
        st.success(f"✅ Fișier încărcat! Are {total_chars} caractere.")
        st.info(f"Voi împărți textul în **{num_chunks} bucăți**.")
        
        st.markdown("---")
        
        # --- PROCESARE ȘI AFIȘARE ---
        for i in range(num_chunks):
            start = i * CHUNK_SIZE
            end = start + CHUNK_SIZE
            
            # Extragem bucata
            chunk_text = string_data[start:end]
            
            # Construim prompt-ul final
            # .format înlocuiește {part} și {total} în textul tău
            header = CUSTOM_PROMPT.format(part=i+1, total=num_chunks)
            final_block = header + "\n\n" + chunk_text
            
            # Afișăm vizual
            st.subheader(f"🔹 Partea {i+1} din {num_chunks}")
            st.caption("Apasă butonul de Copy din colțul dreapta-sus:")
            
            # Afișăm codul gata de copiat
            st.code(final_block, language=None)
            
            st.markdown("---")
            
    except UnicodeDecodeError:
        st.error("Eroare la citire: Fișierul nu pare să fie format UTF-8 standard. Încearcă să-l salvezi din nou ca UTF-8.")
    except Exception as e:
        st.error(f"A apărut o eroare neașteptată: {e}")

else:
    st.write("👈 Aștept să încarci un fișier...")
    
