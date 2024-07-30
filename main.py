import gradio as gr
import whisper
from translate import Translator
from dotenv import dotenv_values
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings

config = dotenv_values(".env")

ELVENLABS_API_KEY = config["ELVENLABS_API_KEY"]

def translator(audio_file):
    
    #1. Transcribing the text using Whisper
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_file)
        transcription = result["text"]

    except Exception as e:
        raise gr.Error(
            f"Error transcribing text: {str(e)}")
    
    #2. Translating the text using Translate

    try:
        es_transcription = Translator(
            from_lang="en", to_lang="es").translate(transcription)
        it_transcription = Translator(
            from_lang="es", to_lang="it").translate(transcription)
        fr_transcription = Translator(
            from_lang="es", to_lang="fr").translate(transcription)
        ja_transcription = Translator(
            from_lang="es", to_lang="ja").translate(transcription)
        
    except Exception as e:
        raise gr.Error(

            f"Error transcribing audio: {str(e)}")

    #3. Generating translated audio using ElevenLabs

    es_save_file_path = text_to_speech(es_transcription, "es")
    it_save_file_path = text_to_speech(it_transcription, "it")
    fr_save_file_path = text_to_speech(fr_transcription, "fr")
    ja_save_file_path = text_to_speech(ja_transcription, "ja")

    return es_save_file_path, it_save_file_path, fr_save_file_path, ja_save_file_path

def text_to_speech(text: str, language: str) -> str:
        try: 
            client = ElevenLabs(api_key = ELVENLABS_API_KEY)

            response = client.text_to_speech.convert(
            voice_id="pNInz6obpgDQGcFmaJgB",  # Adam
            optimize_streaming_latency="0",
            output_format="mp3_22050_32",
            text=text,
            model_id="eleven_turbo_v2",
            voice_settings=VoiceSettings(
                stability=0.0,
                similarity_boost=0.0,
                style=0.0,
                use_speaker_boost=True,
            ),
        )

            save_file_path = f"audios/{language}.mp3"

            with open(save_file_path, "wb") as f:
                for chunk in response:
                    if chunk:
                        f.write(chunk)

        except Exception as e:
            raise gr.Error(
                f"Error generating translated audio: {str(e)}")


        return save_file_path



web = gr.Interface(
    fn=translator,
    inputs=gr.Audio(
        sources=["microphone"],
        type="filepath",
        label= "English"
    ),
    outputs=[
        gr.Audio(label="Spanish"),
        gr.Audio(label= "Italian"),
        gr.Audio(label="French"),
        gr.Audio(label="Japanese")
    ],
    title= "Voice translator",
    description="Translates English voice to several languages thanks to AI",
)

web.launch()

