# First stage: build the app
FROM --platform=linux/amd64 python:3.10 AS builder
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.prod.txt requirements.txt
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt --target=/app --no-cache-dir --require-hashes

# Second stage: copy the app and run it
FROM --platform=linux/amd64 python:3.10-slim
WORKDIR /code
#copy from builder to the slim version
COPY --from=builder /code /code/
# copy the application to the /app directory

COPY ./app code/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
