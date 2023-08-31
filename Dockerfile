# First stage: build the app
FROM python:3.10 AS builder
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.prod.txt requirements.txt
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt --target=/app --no-cache-dir --require-hashes

# Second stage: copy the app and run it
FROM python:3.10-slim
WORKDIR /app
#copy from builder to the slim version
COPY --from=builder /app /app/
# copy the application to the /app directory

COPY ./app /app
RUN tree
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "$PORT"]
