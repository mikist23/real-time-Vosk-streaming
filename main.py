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


# ************* CHINESE MODEL ******************
import os
import pyaudio
import json
from vosk import Model, KaldiRecognizer

def main():
    # Check if the Chinese model directory exists
    if not os.path.exists("model2"):
        print("Error: model directory not found.  ")
        exit(1)

    print("Loading Chinese model...")
    model = Model("model2")
    sample_rate = 16000
    recognizer = KaldiRecognizer(model, sample_rate)

    # Initialize PyAudio
    p = pyaudio.PyAudio()
    try:
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=4000)
        stream.start_stream()
    except Exception as e:
        print("Error opening audio stream:", e)
        p.terminate()
        exit(1)

    print("Listening... Speak into your microphone (in Chinese).")
    last_partial = ""

    try:
        while True:
            data = stream.read(4000, exception_on_overflow=False)
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
