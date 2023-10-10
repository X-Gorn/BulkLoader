FROM python:3.9
COPY . /app/
WORKDIR /app/
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN apt-get install -y ffmpeg
RUN pip3 install --no-cache-dir -r requirements.txt
CMD python3 bot.py