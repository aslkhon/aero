import grpc
import wave
import time
from proto import aero_service_pb2, aero_service_pb2_grpc

now = 0
last = 0

def audio_chunk_generator(file_path, chunk_frames=1280):
    """
    Reads a WAV file and yields audio chunks as AudioChunk messages.

    :param file_path: Path to the WAV file.
    :param chunk_frames: Number of frames per chunk.
    """
    with wave.open(file_path, "rb") as wf:
        global now
        sample_rate = wf.getframerate()
        total_frames = wf.getnframes()
        num_chunks = (total_frames + chunk_frames - 1) // chunk_frames

        for i in range(num_chunks):
            # Read chunk_frames from file
            frames = wf.readframes(chunk_frames)
            # Determine if this is the last chunk
            is_last = i == num_chunks - 1
            yield aero_service_pb2.AudioChunk(
                samples=frames, sample_rate=sample_rate, eou=is_last
            )
            if is_last:
                now = time.time()
                print("sending last chunk for enhancement")
                print(now)
            time.sleep(0.16)


def run_client(file_path):
    """
    Sends audio chunks from a WAV file to the server and receives enhanced audio.

    :param file_path: Path to the WAV file.
    :return: Full enhanced audio as bytes.
    """
    # Create a channel to the server (ensure the port matches the server's setting)
    channel = grpc.insecure_channel("localhost:50052")
    stub = aero_service_pb2_grpc.AeroEnhancementStub(channel)

    # Open a bi-directional stream with the server
    response_iterator = stub.EnhanceStream(audio_chunk_generator(file_path))
    full_enhanced_audio = b""

    for response in response_iterator:
        if response.is_final:
            print("last enhanced chunk received")
            print(last)
            print("Received full enhanced speech.")
            print(time.time())
            full_enhanced_audio = response.samples  # Store final, complete utterance
        else:
            # print("Streaming enhanced chunk...")
            last = time.time()
            

    return full_enhanced_audio


def save_wav(filename, audio_data, sample_rate=16000, channels=1, sampwidth=2):
    """
    Save raw PCM audio data to a WAV file.

    :param filename: Name of the file to save.
    :param audio_data: Raw PCM audio bytes.
    :param sample_rate: Sample rate (e.g., 16000 Hz).
    :param channels: Number of audio channels (e.g., 1 for mono).
    :param sampwidth: Sample width in bytes (e.g., 2 for 16-bit audio).
    """
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sampwidth)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data)


if __name__ == "__main__":
    input_file = "audio/audio.wav"
    enhanced_audio = run_client(input_file)

    # Save the enhanced audio with a proper WAV header
    save_wav("enhanced_audio.wav", enhanced_audio, sample_rate=16000, channels=1, sampwidth=2)
    print("Enhanced audio saved as 'enhanced_audio.wav'")
