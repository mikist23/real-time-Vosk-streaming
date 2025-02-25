# ************* ENGLISH MODEL ******************
# import os
# import pyaudio
# import json
# from vosk import Model, KaldiRecognizer

# def main():
#     # Check if the model directory exists
#     if not os.path.exists("model1"):
#         print("Error: 'model' directory not found.")
#         exit(1)

#     print("Loading model...")
#     model = Model("model1")
#     sample_rate = 16000
#     recognizer = KaldiRecognizer(model, sample_rate)

#     # Initialize PyAudio
#     p = pyaudio.PyAudio()
#     try:
#         stream = p.open(format=pyaudio.paInt16,
#                         channels=1,
#                         rate=sample_rate,
#                         input=True,
#                         frames_per_buffer=4000)
#         stream.start_stream()
#     except Exception as e:
#         print("Error opening audio stream:", e)
#         p.terminate()
#         exit(1)

#     print("Listening... Speak into your microphone.")
#     last_partial = ""

#     try:
#         while True:
#             data = stream.read(4000, exception_on_overflow=False)
#             if not data:
#                 break

#             if recognizer.AcceptWaveform(data):
#                 result = json.loads(recognizer.Result())
#                 text = result.get("text", "").strip()
#                 if text:
#                     print("Final:", text)
#                 last_partial = ""  # reset last partial result
#             else:
#                 partial_result = json.loads(recognizer.PartialResult())
#                 partial = partial_result.get("partial", "").strip()
#                 # Only print if the partial result changed
#                 if partial and partial != last_partial:
#                     print("Partial:", partial)
#                     last_partial = partial
#     except KeyboardInterrupt:
#         print("\nStopping...")
#     finally:
#         stream.stop_stream()
#         stream.close()
#         p.terminate()

# if __name__ == "__main__":
#     main()


# # ************* CHINESE MODEL ******************
# import os
# import pyaudio
# import json
# from vosk import Model, KaldiRecognizer

# def main():
#     # Check if the Chinese model directory exists
#     if not os.path.exists("model2"):
#         print("Error: model directory not found.  ")
#         exit(1)

#     print("Loading Chinese model...")
#     model = Model("model2")
#     sample_rate = 16000
#     recognizer = KaldiRecognizer(model, sample_rate)

#     # Initialize PyAudio
#     p = pyaudio.PyAudio()
#     try:
#         stream = p.open(format=pyaudio.paInt16,
#                         channels=1,
#                         rate=sample_rate,
#                         input=True,
#                         frames_per_buffer=4000)
#         stream.start_stream()
#     except Exception as e:
#         print("Error opening audio stream:", e)
#         p.terminate()
#         exit(1)

#     print("Listening... Speak into your microphone (in Chinese).")
#     last_partial = ""

#     try:
#         while True:
#             data = stream.read(4000, exception_on_overflow=False)
#             if not data:
#                 break

#             if recognizer.AcceptWaveform(data):
#                 result = json.loads(recognizer.Result())
#                 text = result.get("text", "").strip()
#                 if text:
#                     print("Final:", text)
#                 last_partial = ""
#             else:
#                 partial_result = json.loads(recognizer.PartialResult())
#                 partial = partial_result.get("partial", "").strip()
#                 if partial and partial != last_partial:
#                     print("Partial:", partial)
#                     last_partial = partial
#     except KeyboardInterrupt:
#         print("\nStopping...")
#     finally:
#         stream.stop_stream()
#         stream.close()
#         p.terminate()

# if __name__ == "__main__":
#     main()


import os
import pyaudio
import json
from vosk import Model, KaldiRecognizer

def contains_chinese(text):
    """
    Check if the text contains any Chinese characters.
    """
    for ch in text:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

def record_snippet(duration, stream, frames_per_buffer, sample_rate):
    """
    Record a snippet of audio for a given duration.
    """
    frames = []
    # Calculate the number of buffers needed
    num_buffers = int(duration * sample_rate / frames_per_buffer)
    for _ in range(num_buffers):
        data = stream.read(frames_per_buffer, exception_on_overflow=False)
        frames.append(data)
    return b"".join(frames)

def detect_language(snippet, model_en, model_cn, sample_rate, frames_per_buffer):
    """
    Feed the audio snippet into both English and Chinese recognizers,
    then determine which language is more likely based on the transcription.
    """
    # Create a new recognizer for each model for the snippet
    recognizer_en = KaldiRecognizer(model_en, sample_rate)
    recognizer_cn = KaldiRecognizer(model_cn, sample_rate)
    
    # Process the snippet in chunks to simulate streaming
    for i in range(0, len(snippet), frames_per_buffer):
        chunk = snippet[i:i+frames_per_buffer]
        recognizer_en.AcceptWaveform(chunk)
        recognizer_cn.AcceptWaveform(chunk)
    
    result_en = json.loads(recognizer_en.Result())
    result_cn = json.loads(recognizer_cn.Result())
    
    text_en = result_en.get("text", "").strip()
    text_cn = result_cn.get("text", "").strip()
    
    print("English recognizer result:", text_en)
    print("Chinese recognizer result:", text_cn)
    
    # Use a simple check: if the Chinese recognizer returns text with Chinese characters, assume it's Chinese.
    if text_cn and contains_chinese(text_cn):
        return "chinese"
    elif text_en and not contains_chinese(text_en):
        return "english"
    else:
        # Default to English if unsure
        return "english"

def main():
    sample_rate = 16000
    frames_per_buffer = 4000
    snippet_duration = 3  # seconds for language detection

    # Ensure both model directories exist
    if not os.path.exists("model1"):
        print("Error: English model directory 'model_en' not found.")
        exit(1)
    if not os.path.exists("model2"):
        print("Error: Chinese model directory 'model_cn' not found.")
        exit(1)

    print("Loading English model...")
    model_en = Model("model1")
    print("Loading Chinese model...")
    model_cn = Model("model2")

    # Set up PyAudio
    p = pyaudio.PyAudio()
    try:
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=frames_per_buffer)
        stream.start_stream()
    except Exception as e:
        print("Error opening audio stream:", e)
        p.terminate()
        exit(1)

    print("Please speak for {} seconds for language detection...".format(snippet_duration))
    snippet = record_snippet(snippet_duration, stream, frames_per_buffer, sample_rate)

    # Detect language using the recorded snippet
    detected_language = detect_language(snippet, model_en, model_cn, sample_rate, frames_per_buffer)
    print("Detected language:", detected_language)

    # Choose the appropriate model for continuous recognition
    if detected_language == "english":
        recognizer = KaldiRecognizer(model_en, sample_rate)
        print("Using English model for continuous recognition.")
    else:
        recognizer = KaldiRecognizer(model_cn, sample_rate)
        print("Using Chinese model for continuous recognition.")

    print("Listening... Speak into your microphone.")
    last_partial = ""
    try:
        while True:
            data = stream.read(frames_per_buffer, exception_on_overflow=False)
            if not data:
                break

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").strip()
                if text:
                    print("Final:", text)
                last_partial = ""
            else:
                partial_result = json.loads(recognizer.PartialResult())
                partial = partial_result.get("partial", "").strip()
                # Print partial result only if it's new
                if partial and partial != last_partial:
                    print("Partial:", partial)
                    last_partial = partial
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    main()
