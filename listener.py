
# --- process lifecycle -----------------------------
import signal
import sys

# --- audio capture ---------------------------------
import queue
import sounddevice as sd

# --- speech recognition ----------------------------
import json
from vosk import Model, KaldiRecognizer, SetLogLevel

# --- messaging -------------------------------------
import paho.mqtt.client as mqtt
MQTT_HOST = "mosquitto"  # set this to the IP address of your mosquitto broker
MQTT_PORT = 1883
MQTT_TOPIC = "voice/command"

from commands import COMMANDS

# --- process lifecycle ----------------------------
signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))

# --- audio capture --------------------------------
mic_rate = int(sd.query_devices(kind="input")["default_samplerate"])
audio = queue.Queue()
def on_audio(data, frames, time, status):
    audio.put(bytes(data))

# --- speech recognition ---------------------------
SetLogLevel(-1)
model = Model(model_name="vosk-model-small-en-us-0.15")
grammar = json.dumps(list(COMMANDS) + ["[unk]"])
recognizer = KaldiRecognizer(model, mic_rate, grammar)

# --- messaging ------------------------------------
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(MQTT_HOST, MQTT_PORT)
client.loop_start()

# --- listener -------------------------------------
with sd.RawInputStream(samplerate=mic_rate,
                       blocksize=mic_rate // 2,
                       dtype="int16", channels=1,
                       callback=on_audio):
    print("listening...")
    while True:
        chunk = audio.get()
        if not recognizer.AcceptWaveform(chunk):
            continue
        text = json.loads(recognizer.Result())["text"]
        text = text.replace("[unk]", "").strip()
        if not text:
            continue
        print("heard:", text)
        if text in COMMANDS:
            command = COMMANDS.get(text)
            if (command):
                print("WE GOT A COMMAND:", command)
                client.publish(MQTT_TOPIC, command)
