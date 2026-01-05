import pyaudio
import wave
import os
import threading
from time import sleep
from datetime import datetime

from evdev import InputDevice, ecodes, categorize


INPUT_DEVICE = "/dev/input/event6"  # ⬅️ CHANGE THIS


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

        print("\n🎙️ Recording started... Press Play/Pause to stop.")
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
        filename = f"recordings/guest_message_{timestamp}.wav"

        with wave.open(filename, "wb") as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b"".join(self.frames))

        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"✅ Recording saved: {filename}")
        sleep(5)
        print("=" * 60)
        print("🎤 WELCOME TO AUDIO GUEST BOOK FOR Benoît Dubuis !")
        print("=" * 60)
        print("\nInstructions:")
        print("- Press the button on the phone to start recording !")
        print("- Press the same button again to stop & save")

    # ================= MAIN LOOP =================

    def run(self):
        print("=" * 60)
        print("🎤 WELCOME TO AUDIO GUEST BOOK FOR Benoît Dubuis !")
        print("=" * 60)
        print("\nInstructions:")
        print("- Press the button on the phone to start recording !")
        print("- Press the same button again to stop & save")

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
                    print("\nExiting...")
                    break

        except KeyboardInterrupt:
            print("\nInterrupted.")
        finally:
            if self.recording:
                self.stop_recording()
            self.cleanup()

    def cleanup(self):
        self.audio.terminate()
        print("Goodbye! 👋")


if __name__ == "__main__":
    AudioGuestBook().run()