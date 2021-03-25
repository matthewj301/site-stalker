FROM python:3.9

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /site-stalker
ENV PYTHONPATH="$PYTHONPATH:/site-stalker"
ENV PYTHONUNBUFFERED=0

CMD python site-stalker/site_stalker/runner.py