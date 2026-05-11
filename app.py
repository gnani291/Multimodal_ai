import streamlit as st
import yt_dlp
import whisper
import pytesseract

from PIL import Image
from gtts import gTTS


st.title("AI Multimedia Project")

st.write(
    "YouTube Download + Speech Recognition + OCR + Text To Speech"
)

#youtube video download
st.header("1. Download YouTube Video")

video_url = st.text_input(
    "Enter YouTube Video URL"
)

if st.button("Download Video"):

    ydl_opts = {
        "format": "best",
        "noplaylist": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    st.success("Video Downloaded Successfully")

# speech recognoisation(speech to text)
st.header("2. Speech Recognition")

audio_file = st.file_uploader(
    "Upload Audio File",
    type=["mp3", "wav"]
)

speech_text = ""

if audio_file is not None:

    with open(audio_file.name, "wb") as f:
        f.write(audio_file.read())

    if st.button("Convert Speech To Text"):

        model = whisper.load_model("base")

        result = model.transcribe(audio_file.name)

        speech_text = result["text"]

        st.subheader("Recognized Text")

        st.write(speech_text)

# text extraction (OCR)
st.header("3. Image Text Extraction")

image_file = st.file_uploader(
    "Upload Image",
    type=["png", "jpg", "jpeg"]
)

ocr_text = ""

if image_file is not None:

    img = Image.open(image_file)

    st.image(img, caption="Uploaded Image")

    if st.button("Extract Text"):

        ocr_text = pytesseract.image_to_string(
            img,
            lang="eng"
        )

        st.subheader("OCR Text")

        st.write(ocr_text)


combined_text = speech_text + "\n" + ocr_text


st.header("4. Text To Speech")

user_text = st.text_area(
    "Enter Text",
    value=combined_text
)
#text to speech

if st.button("Generate Audio"):

    tts = gTTS(user_text)

    tts.save("output.mp3")

    st.success("Audio Generated Successfully")

    audio = open("output.mp3", "rb")

    st.audio(audio.read())


st.write("Project Ready")
