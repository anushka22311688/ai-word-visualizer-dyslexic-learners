import streamlit as st
import random
import pyphen
from gtts import gTTS
from io import BytesIO
import base64

st.set_page_config(page_title="AI Word Visualizer for Dyslexic Learners", layout="centered")

st.title("🧩 AI Word Visualizer for Dyslexic Learners")
st.markdown("""
This tool helps dyslexic learners **see**, **hear**, and **trace** words more effectively.
It splits words into syllables, colors them distinctly, and provides audio pronunciation.
""")

word = st.text_input("Enter any English word:")
slow_read = st.checkbox("Slow pronunciation")

if "test_word" not in st.session_state:
    st.session_state.test_word = None

test_words = [
    "beautiful", "extraordinary", "determination", "opportunity", "communication", "metamorphosis",
    "information", "photosynthesis", "pronunciation", "electricity", "rehabilitation", "anthropology",
    "civilization", "investigation", "encyclopedia", "responsibility", "exaggeration", "magnificent",
    "artificial", "imagination", "appreciation", "architecture", "philosophy", "transportation",
    "temperature", "development", "contribution", "circumstance", "intelligence", "representation",
    "observation", "application", "consideration", "environment", "conversation", "demonstration",
    "comprehensive", "presentation", "transformation", "identification", "classification"
]

def visualize_word(word):
    dic = pyphen.Pyphen(lang='en')
    syllables = dic.inserted(word)
    syllable_list = syllables.split("-")

    st.success(f"The word **{word}** has **{len(syllable_list)} syllable(s)**.")

    colors = ["#FF6F61", "#6A5ACD", "#20B2AA", "#FFB347", "#90EE90", "#FF69B4", "#87CEFA", "#9370DB"]

    highlighted = "".join(
        [f"<span style='color:{colors[i % len(colors)]}; font-size:36px; font-weight:700;'>{syll}</span>"
         for i, syll in enumerate(syllable_list)]
    )
    st.markdown(f"<div style='text-align:center; margin-top:20px;'>{highlighted}</div>", unsafe_allow_html=True)

    tts = gTTS(word, slow=slow_read)
    audio_bytes = BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    audio_b64 = base64.b64encode(audio_bytes.read()).decode()
    st.markdown(f"""
    <audio key="{word}" controls>
        <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
    </audio>
    """, unsafe_allow_html=True)

    # ✏️ Trace section with improved even spacing
    st.markdown("### ✏️ Trace the word:")
    trace_html = "<div style='display:flex; justify-content:center; gap:14px; margin-top:20px;'>"
    for i, syll in enumerate(syllable_list):
        color = colors[i % len(colors)]
        for letter in syll.upper():
            trace_html += f"<span style='color:{color}; font-size:28px; font-weight:600; letter-spacing:8px;'>{letter}</span>"
    trace_html += "</div>"
    st.markdown(trace_html, unsafe_allow_html=True)

# Learning Mode
if st.button("🔍 Visualize Word"):
    if word.strip():
        visualize_word(word)
    else:
        st.warning("Please enter a word first!")

# Test Mode
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("🧠 Test Mode: Random Difficult Word")

if st.button("🎯 Try a Random Word"):
    st.session_state.test_word = random.choice(test_words)

if st.session_state.test_word:
    st.info(f"Your test word is: **{st.session_state.test_word}**")
    visualize_word(st.session_state.test_word)

st.markdown("<br><hr><center>Made with ❤️ by Anushka Borude</center>", unsafe_allow_html=True)
