FROM jupyter/datascience-notebook:x86_64-python-3.11.6
USER root

COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt
RUN rm /tmp/requirements.txt

EXPOSE 8888
