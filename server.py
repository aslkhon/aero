from pathlib import Path
import time
import grpc
import torch
from dotmap import DotMap

from concurrent import futures

import yaml
from proto import aero_service_pb2, aero_service_pb2_grpc
from src.models import modelFactory
from src.model_serializer import (
    SERIALIZE_KEY_MODELS,
    SERIALIZE_KEY_STATE,
)


class AeroEnhancementServicer(aero_service_pb2_grpc.AeroEnhancementServicer):
    def __init__(self, model, device):
        super().__init__()
        self.model = model
        self.device = device

    def EnhanceStream(self, request_iterator, context):
        global now
        """
        Handles real-time enhancement and full utterance reconstruction.
        """
        speech_buffer = []  # Stores all enhanced chunks for final full audio

        for chunk in request_iterator:
            # 1. Convert bytes to tensor
            audio_data = torch.frombuffer(chunk.samples, dtype=torch.int16)
            audio_data = (
                audio_data.view(1, -1).to(torch.float32) / 32768.0
            )  # Normalize to [-1, 1]

            # 2. Send to model
            with torch.no_grad():
                enhanced_chunk = (
                    self.model(audio_data.unsqueeze(0).to(self.device)).squeeze(0).cpu()
                )

            # 3. Convert back to bytes
            enhanced_int16 = (enhanced_chunk * 32768.0).clamp_(-32768, 32767).short()
            enhanced_bytes = enhanced_int16.cpu().numpy().tobytes()

            # 4. Buffer the enhanced chunks for full utterance reconstruction
            speech_buffer.append(enhanced_bytes)

            # 5. Stream the enhanced chunk back to client immediately
            yield aero_service_pb2.EnhancedAudioChunk(
                samples=enhanced_bytes,
                sample_rate=16000,  # or model's output sample rate
                is_final=False,
            )

            # 6. If the client signals "EOU", send full enhanced speech back
            if chunk.eou:
                full_speech = b"".join(speech_buffer)  # Concatenate all buffered chunks

                yield aero_service_pb2.EnhancedAudioChunk(
                    samples=full_speech, sample_rate=16000, is_final=True
                )

                # Reset buffer for the next utterance
                speech_buffer.clear()


def load_model(config: dict):
    checkpoint_path = Path(config.checkpoint_file)
    model = modelFactory.get_model(config)["generator"]
    package = torch.load(checkpoint_path, config.device)

    model.load_state_dict(
        package[SERIALIZE_KEY_MODELS]["generator"][SERIALIZE_KEY_STATE]
    )

    return model


def serve():
    with open("conf.yaml", "r") as f:
        config = yaml.safe_load(f)

    config = DotMap(config)

    model = load_model(config)
    device = torch.device(config.device)
    model.to(device)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
    aero_service_pb2_grpc.add_AeroEnhancementServicer_to_server(
        AeroEnhancementServicer(model, device), server
    )

    server.add_insecure_port("[::]:50052")
    server.start()
    print("AERO gRPC service is running on port 50052...")
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()
