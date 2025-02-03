import grpc
import wave
import time
from concurrent import futures
from proto import aero_service_pb2, aero_service_pb2_grpc

PARALLEL_PROCESSING = 8


def audio_chunk_generator(file_path, chunk_frames=1280):
    """Unchanged generator function from original code"""
    with wave.open(file_path, "rb") as wf:
        sample_rate = wf.getframerate()
        total_frames = wf.getnframes()
        num_chunks = (total_frames + chunk_frames - 1) // chunk_frames

        for i in range(num_chunks):
            frames = wf.readframes(chunk_frames)
            is_last = i == num_chunks - 1
            yield aero_service_pb2.AudioChunk(
                samples=frames, sample_rate=sample_rate, eou=is_last
            )
            time.sleep(0.16)


def run_client(file_path):
    """Unchanged client function from original code"""
    channel = grpc.insecure_channel("localhost:50052")
    stub = aero_service_pb2_grpc.AeroEnhancementStub(channel)
    response_iterator = stub.EnhanceStream(audio_chunk_generator(file_path))
    full_enhanced_audio = b""

    for response in response_iterator:
        if response.is_final:
            full_enhanced_audio = response.samples
        else:
            print(f"Streaming enhanced chunk from {file_path}...")

    return full_enhanced_audio


def save_wav(filename, audio_data, sample_rate=16000, channels=1, sampwidth=2):
    """Unchanged save function from original code"""
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sampwidth)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data)


def process_audio(input_file, output_suffix):
    """Helper function to process audio and save with unique suffix"""
    enhanced_audio = run_client(input_file)
    output_file = f"enhanced_audio_{output_suffix}.wav"
    save_wav(output_file, enhanced_audio)
    return output_file


if __name__ == "__main__":
    input_file = "audio/audio.wav"

    # Create a thread pool with 8 workers
    with futures.ThreadPoolExecutor(max_workers=8) as executor:
        # Submit 8 simultaneous processing tasks
        future_to_index = {
            executor.submit(process_audio, input_file, i): i
            for i in range(PARALLEL_PROCESSING)
        }

        # Collect results as they complete
        for future in futures.as_completed(future_to_index):
            index = future_to_index[future]
            try:
                output_file = future.result()
                print(f"Processing {index} completed. Saved to {output_file}")
            except Exception as exc:
                print(f"Processing {index} generated an exception: {exc}")
