FROM python:3.9

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app

ENV PYTHONPATH=/

RUN groupadd emailtidy
RUN useradd emailtidy -g emailtidy
RUN chown emailtidy:emailtidy -R /app

USER emailtidy:emailtidy

CMD [ "/app/start.sh" ]
