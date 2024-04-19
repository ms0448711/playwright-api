# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM mcr.microsoft.com/playwright

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.5 \
    python3-pip \
    tmux \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED 1

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

RUN npm init

CMD exec uvicorn --workers 4 --host 0.0.0.0 --port 7000 app.main:app 