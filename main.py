import pyaudio
import wave
import keyboard
import os
from datetime import datetime


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

        # Create recordings directory if it doesn't exist
        if not os.path.exists('recordings'):
            os.makedirs('recordings')

    def start_recording(self):
        """Start audio recording"""
        self.recording = True
        self.frames = []

        self.stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )

        print("\n🎙️  Recording started... Press Play/Pause to stop.")

        while self.recording:
            try:
                data = self.stream.read(self.CHUNK)
                self.frames.append(data)
            except:
                break

    def stop_recording(self):
        """Stop recording and save the file"""
        if not self.recording:
            return

        self.recording = False

        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recordings/guest_message_{timestamp}.wav"

        # Save the recording
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

        print(f"✅ Recording saved: {filename}")
        print("Press Play/Pause to record another message, or 'q' to quit.\n")

    def run(self):
        """Main loop for the guest book"""
        print("=" * 60)
        print("🎤 AUDIO GUEST BOOK")
        print("=" * 60)
        print("\nInstructions:")
        print("- Press the Play/Pause button to start recording")
        print("- Press Play/Pause again to stop and save")
        print("- Press 'q' to quit the application\n")
        print("Waiting for Play/Pause button press...")

        try:
            while True:
                # Listen for play/pause button (media key)
                if keyboard.is_pressed('play/pause media'):
                    if not self.recording:
                        self.start_recording()
                    else:
                        self.stop_recording()

                    # Wait for button release to avoid multiple triggers
                    while keyboard.is_pressed('play/pause media'):
                        pass

                # Check for quit command
                if keyboard.is_pressed('q'):
                    break

        except KeyboardInterrupt:
            print("\n\nShutting down...")
        finally:
            if self.recording:
                self.stop_recording()
            self.cleanup()

    def cleanup(self):
        """Clean up audio resources"""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.audio.terminate()
        print("Goodbye! 👋")


if __name__ == "__main__":
    guestbook = AudioGuestBook()
    guestbook.run()