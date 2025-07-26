import streamlit as st
import tempfile
import os
import whisper
from openai import OpenAI
from pydub import AudioSegment
import datetime
from dotenv import load_dotenv
load_dotenv()

# Set your OpenAI API key
apikey = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=apikey)
# -----------------------------
# Utility for readable logs
# -----------------------------
def log(message):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    st.write(f"🕒 `{timestamp}` - {message}")
    print(f"[{timestamp}] {message}")

# -----------------------------
# Split audio into 10-minute chunks
# -----------------------------
def split_audio(file_path, chunk_length_ms=10 * 60 * 1000):
    log("🔧 Splitting audio into chunks...")
    audio = AudioSegment.from_file(file_path)
    chunks = []
    for i in range(0, len(audio), chunk_length_ms):
        chunk = audio[i:i+chunk_length_ms]
        chunk_path = f"{file_path}_chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)
    log(f"✅ Audio split into {len(chunks)} chunk(s)")
    return chunks

# -----------------------------
# Transcribe chunks serially
# -----------------------------
def transcribe_audio_serial(file_path):
    log("📦 Loading Whisper model...")
    model = whisper.load_model("medium")  # or "small"

    chunks = split_audio(file_path)
    transcript_parts = []

    progress_bar = st.progress(0)
    total_chunks = len(chunks)

    for idx, chunk_path in enumerate(chunks):
        log(f"🎧 Processing chunk {idx + 1} / {total_chunks}")
        result = model.transcribe(chunk_path, task="translate")

        chunk_text = result['text']
        transcript_parts.append(chunk_text)

        log(f"✅ Chunk {idx + 1} completed. Length: {len(chunk_text)} characters.")
        progress_bar.progress((idx + 1) / total_chunks)

        os.remove(chunk_path)

    full_transcript = " ".join(transcript_parts).strip()
    log("📝 All chunks transcribed successfully.")
    return full_transcript

# -----------------------------
# Extract structured info
# -----------------------------
def extract_info_from_transcript(transcript):
    log("🔍 Extracting structured information using GPT...")
    prompt = f"""
You are a police assistant AI. Given the following transcript of a police complaint call, extract:
1. Complaint Category (e.g., Robbery, Assault, Cybercrime, etc.)
2. Location of Incident
3. Time or Date if mentioned
4. Any names of suspects or victims mentioned

Transcript:
\"\"\"{transcript}\"\"\"

Return the result as a JSON object with keys:
"category", "location", "time", "suspect_or_victim"
"""
    response = client.responses.create(
        model="gpt-4",
        instructions="You are a police assistant that goes through audio files to find out details about the crime.",
        input=prompt
    )
    log("✅ Crime insights extraction complete.")
    return response.choices[0].message['content']

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Crime Insight Extractor", page_icon="🚓")
st.title("🚓 Crime Insight Extractor")

st.markdown("Upload a **police complaint audio** (.mp3 or .wav). The app will:")
st.markdown("""
- 🎙️ Transcribe & translate speech to English  
- 🔎 Extract key insights (e.g., category, location, people, time)  
- 📊 Display structured results
""")

uploaded_file = st.file_uploader("📤 Upload Audio File", type=["mp3", "wav"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
        log("📁 Audio file uploaded and saved temporarily.")

    with st.spinner("⏳ Processing audio... please wait"):
        transcript = transcribe_audio_serial(tmp_path)
        extracted_info = extract_info_from_transcript(transcript)

    st.success("✅ Done! Here's what we found:")

    st.subheader("📄 Transcript")
    st.write(transcript)

    st.subheader("📊 Extracted Crime Information")
    st.json(extracted_info)

    os.remove(tmp_path)
    log("🗑️ Temporary audio file deleted.")
