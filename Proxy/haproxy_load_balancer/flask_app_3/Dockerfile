FROM python:3.11-slim

WORKDIR /app

# Install Flask directly
RUN pip install flask

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]