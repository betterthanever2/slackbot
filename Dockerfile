FROM python:3.9.1-slim

ADD . /dash_app
WORKDIR /dash_app
RUN pip3 install numpy==1.20.1
RUN pip3 install --no-cache-dir \
    -r requirements.txt

CMD ["sh", "-c", "python main.py"]