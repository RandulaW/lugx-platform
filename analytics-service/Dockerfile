FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install fastapi uvicorn requests prometheus-fastapi-instrumentator==7.1.0
EXPOSE 3000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
