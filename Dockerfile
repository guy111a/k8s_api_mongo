FROM python:3.9-alpine

RUN pip3 install flask

RUN pip3 install pymongo 

COPY myapi.py /opt/

EXPOSE 5000

WORKDIR /opt

ENTRYPOINT [ "python", "myapi.py"]
