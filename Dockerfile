# # First stage: build the app
# FROM python:3.11 AS requirements-app-stage
# # Don't buffer stdout to show every stdout and stderr
# ENV PYTHONUNBUFFERED=1 
# WORKDIR /tmp
# COPY requirements.prod.txt tmp/requirements.txt
# RUN python -m pip install --upgrade pip && \
#     pip install --no-cache-dir --upgrade --target=/tmp -r /tmp/requirements.txt 

# # Second stage: copy the app and run it
# FROM python:3.11-slim
# WORKDIR /code
# #copy from requirements-stage to the slim version code dir
# COPY --from=requirements-app-stage /tmp /code/
# COPY --from=requirements-app-stage /tmp/app /code/app
# COPY ./app /code/app
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# 
FROM python:3.11

# 
WORKDIR /code

# 
COPY ./requirements.prod.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /code/app

# 
CMD ["uvicorn", "app.main:app", "--workers", "2", "--host", "0.0.0.0", "--port", "8000"]
