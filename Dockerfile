FROM python:3.8-slim-buster

WORKDIR /app

# Copy everything except .env
COPY . /app
RUN rm -rf .env

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]