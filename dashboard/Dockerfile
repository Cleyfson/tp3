FROM python:3.10-slim

RUN pip install --no-cache-dir streamlit redis

WORKDIR /app
COPY dashboard.py .

EXPOSE 8501

ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

ENTRYPOINT ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
