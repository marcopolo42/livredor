import pyaudio
import wave
import os
import threading
from time import sleep
from datetime import datetime

from evdev import InputDevice, ecodes, categorize


INPUT_DEVICE = "/dev/input/event6"  # ⬅️ À adapter si nécessaire


class AudioGuestBook:
    def __init__(self):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100

        self.recording = False
        self.frames = []

        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.record_thread = None

        self.device = InputDevice(INPUT_DEVICE)

        if not os.path.exists("recordings"):
            os.makedirs("recordings")

    # ================= AUDIO =================

    def _record_loop(self):
        while self.recording:
            try:
                data = self.stream.read(self.CHUNK, exception_on_overflow=False)
                self.frames.append(data)
            except Exception:
                break

    def start_recording(self):
        if self.recording:
            return

        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n🎙️ Enregistrement en cours...")
        print("Appuyez sur le bouton pour arrêter et sauvegarder votre message.")
        self.recording = True
        self.frames = []

        self.stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
        )

        self.record_thread = threading.Thread(target=self._record_loop, daemon=True)
        self.record_thread.start()

    def stop_recording(self):
        if not self.recording:
            return

        self.recording = False
        self.record_thread.join()

        self.stream.stop_stream()
        self.stream.close()
        self.stream = None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recordings/message_invité_{timestamp}.wav"

        with wave.open(filename, "wb") as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b"".join(self.frames))

        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"✅ Message enregistré avec succès !")
        print(f"📁 Fichier : {filename}")

        sleep(4)

        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 60)
        print("🎤 Bienvenue dans la capsule temporelle")
        print("🎉 Pour l'anniversaire de Benoît Dubuis !")
        print("=" * 60)
        print("\nInstructions :")
        print("- Appuyez sur le bouton du téléphone pour commencer l’enregistrement")
        print("- Appuyez à nouveau sur le même bouton pour arrêter et sauvegarder")

    # ================= BOUCLE PRINCIPALE =================

    def run(self):
        print("=" * 60)
        print("🎤 BIENVENUE DANS LE LIVRE D’OR AUDIO")
        print("🎉 Anniversaire de Benoît Dubuis")
        print("=" * 60)
        print("\nInstructions :")
        print("- Appuyez sur le bouton du téléphone pour commencer l’enregistrement")
        print("- Appuyez à nouveau sur le même bouton pour arrêter et sauvegarder")

        try:
            for event in self.device.read_loop():
                if event.type != ecodes.EV_KEY:
                    continue

                key = categorize(event)

                if key.keystate != key.key_down:
                    continue

                if key.keycode == "KEY_PLAYPAUSE":
                    if self.recording:
                        self.stop_recording()
                    else:
                        self.start_recording()

                elif key.keycode in ("KEY_Q", "KEY_ESC"):
                    print("\nFermeture de l’application...")
                    break

        except KeyboardInterrupt:
            print("\nInterruption détectée.")
        finally:
            if self.recording:
                self.stop_recording()
            self.cleanup()

    def cleanup(self):
        self.audio.terminate()
        print("Au revoir 👋 Merci pour votre message !")


if __name__ == "__main__":
    AudioGuestBook().run()