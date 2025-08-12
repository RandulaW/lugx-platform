FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install fastapi uvicorn mysql-connector-python prometheus-fastapi-instrumentator==7.1.0
EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
