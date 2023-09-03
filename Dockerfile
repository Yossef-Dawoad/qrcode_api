# First stage: build the app
FROM --platform=linux/amd64 python:3.11 AS requirements-stage
# Don't buffer stdout to show every stdout and stderr
ENV PYTHONUNBUFFERED=1 
WORKDIR /tmp
COPY requirements.prod.txt requirements.txt
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt --target=/app --no-cache-dir --require-hashes

# Second stage: copy the app and run it
FROM --platform=linux/amd64 python:3.11-slim

WORKDIR /code
#copy from requirements-stage to the slim version code dir
COPY --from=requirements-stage /tmp /code/
COPY ./app /code/app
EXPOSE 8000
ENV PYTHONPATH=/code
CMD uvicorn app.main:app --host 0.0.0.0 --port 8000
