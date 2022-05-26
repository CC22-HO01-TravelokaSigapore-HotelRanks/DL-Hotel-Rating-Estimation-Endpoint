FROM python:3.10.3-slim-buster

WORKDIR /app

COPY . .

# Initial Repository PPA Update
RUN apt-get update -y

# Install Container Dependencies
RUN apt-get install unzip curl gpg lsb-release python3-dev default-libmysqlclient-dev build-essential -y

# Install Redis
RUN echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/redis.list
# RUN apt-get update -y
RUN apt-get install redis -y
RUN redis-server --port 6379 --daemonize yes
ENV REDIS_HOST=127.0.0.1
ENV REDIS_PORT=6379

# Unpack pretrained model
RUN pip install gdown
# Replace this with the model version google drive ids
# The file is in the folder model/{version}/saved_model.zip
RUN gdown 1-hFm18fG2NYPQOgnYvG91dxputZ2fbKX
RUN unzip saved_model.zip
RUN rm saved_model.zip

# Prepare python runtime
RUN pip install -r requirements.txt

RUN apt-get autoremove -y

# Preprare network
ENV HOST 0.0.0.0
EXPOSE 8001

CMD ["python", "main.py"]