FROM python:3.9-slim

WORKDIR /app

COPY requirements/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

EXPOSE 5000

CMD ["python", "src/web_app/backend/app.py"] 