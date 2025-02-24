import os
import pyaudio
import json
from vosk import Model, KaldiRecognizer

# # Check if the model directory exists
# if not os.path.exists("model"):
#     print("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
#     exit(1)

# # Load the Vosk model
# model = Model("model")
# # Set the sample rate. Ensure this matches your microphone's sample rate.
# sample_rate = 16000
# recognizer = KaldiRecognizer(model, sample_rate)

# # Set up PyAudio for microphone streaming
# p = pyaudio.PyAudio()

# stream = p.open(format=pyaudio.paInt16,
#                 channels=1,
#                 rate=sample_rate,
#                 input=True,
#                 frames_per_buffer=8000)
# stream.start_stream()

# print("Listening... Speak into your microphone.")

# try:
#     while True:
#         # Read audio data from the microphone
#         data = stream.read(4000, exception_on_overflow=False)
#         if len(data) == 0:
#             break

#         # Process the audio chunk with Vosk
#         if recognizer.AcceptWaveform(data):
#             # Final result when a phrase is complete
#             result = json.loads(recognizer.Result())
#             print("Final:", result.get("text", ""))
#         else:
#             # Partial result while still processing
#             partial_result = json.loads(recognizer.PartialResult())
#             print("Partial:", partial_result.get("partial", ""))
# except KeyboardInterrupt:
#     print("\nStopping...")
# finally:
#     stream.stop_stream()
#     stream.close()
#     p.terminate()
