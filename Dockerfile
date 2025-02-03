FROM python:3.10-slim

WORKDIR /app

# Install libgomp1 for torchaudio
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsndfile1 \
    sox \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Default model location
ENV CHECKPOINT_PATH=/models/model.th

# Prevents OpenMP from using multiple threads
ENV OMP_NUM_THREADS=1
ENV MKL_NUM_THREADS=1
ENV NUMEXPR_NUM_THREADS=1
ENV OPENBLAS_NUM_THREADS=1

EXPOSE 50052

ENTRYPOINT ["python", "server.py"]