# First stage: build the app
FROM --platform=linux/amd64 python:3.10 AS requirements-stage
WORKDIR /tmp
COPY requirements.prod.txt requirements.txt
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt --target=/app --no-cache-dir --require-hashes

# Second stage: copy the app and run it
FROM --platform=linux/amd64 python:3.10-slim
WORKDIR /code
#copy from requirements-stage to the slim version code dir
COPY --from=requirements-stage /tmp /code/
COPY ./app /code/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
