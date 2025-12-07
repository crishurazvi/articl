import streamlit as st
import math

# --- CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="TXT Splitter Didactic", page_icon="🎓")
st.title("🎓 TXT la Curs Didactic (Splitter)")
st.info("Încarcă un fișier text. Îl voi împărți compact, iar AI-ul va primi instrucțiuni să creeze un Curs Didactic structurat.")

# --- SETĂRI ---
with st.expander("⚙️ Setări Prompt & Mărime", expanded=True):
    CHUNK_SIZE = st.slider(
        "Mărime bucată (caractere)", 
        min_value=2000, 
        max_value=50000, 
        value=15000, 
        step=1000,
        help="15.000 e standard. Trage spre dreapta pentru modele noi (Gemini 1.5, GPT-4o)."
    )
    
    # Noul Prompt Didactic & Limba Originală
    default_prompt = """Ești un expert în design educațional și pedagogie. 
Analizează textul următor (care este PARTEA {part} din {total}) și memorează informația. Așteaptă următoarea parte.

Dacă aceasta este ULTIMA parte (sau singura), te rog să ignori cererea de rezumat simplu și să structurezi TOATĂ informația acumulată sub forma unui CURS DIDACTIC COMPLET, redactat în LIMBA ORIGINALĂ a textului furnizat.

Structura cerută:
1. 🎓 TITLUL CURSULUI & OBIECTIVE DE ÎNVĂȚARE
2. 📚 MODULE (împarte informația logic în capitole/module)
3. 🧠 CONCEPTE CHEIE & DEFINIȚII (explicații didactice)
4. 💡 EXEMPLE PRACTICE (din text sau deduse)
5. 📝 EXERCIȚIU DE REFLECȚIE sau TEST SCURT

Textul de analizat:
-------------------"""

    CUSTOM_PROMPT = st.text_area(
        "Instrucțiuni pentru AI (Prompt):",
        value=default_prompt,
        height=300
    )

# --- ZONA DE ÎNCĂRCARE ---
uploaded_file = st.file_uploader("Alege un fișier .txt", type="txt")

if uploaded_file is not None:
    try:
        # Citire fișier
        string_data = uploaded_file.read().decode("utf-8")
        
        total_chars = len(string_data)
        num_chunks = math.ceil(total_chars / CHUNK_SIZE)
        
        st.success(f"✅ Fișier încărcat! ({total_chars} caractere). Pregătit în **{num_chunks} module**.")
        st.markdown("---")
        
        # --- PROCESARE ȘI AFIȘARE COMPACTĂ ---
        for i in range(num_chunks):
            start = i * CHUNK_SIZE
            end = start + CHUNK_SIZE
            
            # Extragem bucata
            chunk_text = string_data[start:end]
            
            # Construim prompt-ul final
            header = CUSTOM_PROMPT.format(part=i+1, total=num_chunks)
            final_block = header + "\n\n" + chunk_text
            
            # --- MODIFICAREA UI: EXPANDER ---
            # Folosim st.expander ca să ținem textul ascuns până dai click
            label = f"🔹 Partea {i+1} din {num_chunks} (Click pentru Copy)"
            
            # 'expanded=False' înseamnă că pornesc toate închise -> economie de spațiu
            # Primul îl lăsăm deschis (opțional) ca să vezi că merge
            is_expanded = (i == 0) 
            
            with st.expander(label, expanded=is_expanded):
                st.caption("Butonul de 'Copy' apare în colțul din dreapta-sus al blocului de mai jos:")
                st.code(final_block, language=None)
            
    except UnicodeDecodeError:
        st.error("Eroare la citire: Fișierul nu pare să fie format UTF-8 standard.")
    except Exception as e:
        st.error(f"A apărut o eroare neașteptată: {e}")

else:
    st.write("👈 Încarcă un curs sau o carte în format .txt")
    
