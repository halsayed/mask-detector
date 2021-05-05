FROM python:3.8-alpine

COPY requirements.txt ./
RUN pip install -U pip && pip install -r requirements.txt

RUN mkdir /web-ui
WORKDIR /web-ui
COPY  . /web-ui/

RUN addgroup -S appgroup && adduser -S appuser -G appgroup
RUN chown appuser:appgroup -R /web-ui
USER appuser

EXPOSE 8000
ENTRYPOINT ["gunicorn", "--config", "gunicorn-cfg.py", "wsgi:app"]