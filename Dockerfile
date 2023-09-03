# First stage: build the app
FROM --platform=linux/amd64 python:3.11 AS requirements-app-stage
# Don't buffer stdout to show every stdout and stderr
ENV PYTHONUNBUFFERED=1 
WORKDIR /tmp
COPY requirements.prod.txt tmp/requirements.txt
RUN python -m pip install --upgrade pip && \
    pip install -r code/requirements.txt --no-cache-dir --require-hashes 
COPY ./app /tmp/app

# Second stage: copy the app and run it
FROM --platform=linux/amd64 python:3.11-slim

WORKDIR /code
#copy from requirements-stage to the slim version code dir
COPY --from=requirements-app-stage /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=requirements-app-stage /tmp/app /code/app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]