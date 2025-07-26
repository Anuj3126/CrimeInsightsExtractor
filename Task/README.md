# Police Call Analytics - Crime Insight Extractor

An AI-powered solution that processes police complaint audio calls, transcribes them, and extracts structured crime-related information to support rapid investigation.

## Features

- 🎤 **Audio Processing**: Supports .wav and .mp3 file formats
- 🔉 **Speech-to-Text**: Accurate transcription using OpenAI's Whisper
- 🌍 **Multi-language Support**: Automatic translation to English (if needed)
- 🔍 **Crime Analysis**: Identifies crime categories and extracts key details
- 📊 **Structured Output**: Presents insights in an easy-to-understand format
- 🖥️ **Web Interface**: User-friendly Streamlit-based web application

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Anuj3126/CrimeInsightsExtractor.git
   cd CrimeInsightsExtractor
   cd Task
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Streamlit application**
   ```bash
   streamlit run src/app.py
   ```

2. **Upload an audio file** through the web interface

3. **View the analysis results** including:
   - Crime category detection
   - Location and time extraction
   - People and weapons mentioned
   - Additional contextual details
     
4. **Using Google Colab** (For monitoring each and every step):
   - Connect to T4 GPU kernel as it would make the whole process faster.
   - Include your OpenAI key for the code to work.
   - Run the requirements cell first to make sure we have all the dependencies installed
   - Upload the audio file that you want to process and run the subsequent cell to get the transcript and the info.

## IMPORTANT:
- Jupyter notebook has the sample input and output already done as a demo with both the transcript and the extracted data.
- OpenAI API key needs to be used for this purpose.

## Project Structure

```
CrimeInsightsExtractor/
Task/
├── data/                   # Sample audio files
├── notebooks/              # Jupyter notebook used for testing and for GPU purpose (Google colab)
├── src/                    # Source code
│   ├── app.py              # Streamlit application
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Dependencies

- streamlit
- openai
- pydub
- ffmpeg-python
- whisper

## Acknowledgments

- OpenAI for the Whisper speech recognition model
- Streamlit for the web application framework
- spaCy for natural language processing

---
