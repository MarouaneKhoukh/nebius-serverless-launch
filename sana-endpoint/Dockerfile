FROM pytorch/pytorch:2.13.0-cuda12.6-cudnn9-runtime

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HUB_DISABLE_TELEMETRY=1 \
    PIP_BREAK_SYSTEM_PACKAGES=1

RUN pip install --no-cache-dir \
      diffusers==0.39.0 \
      transformers==5.13.1 \
      accelerate==1.14.0 \
      fastapi==0.141.1 \
      uvicorn==0.52.1

WORKDIR /app
COPY serve.py /app/serve.py
EXPOSE 8000
CMD ["python", "serve.py"]
