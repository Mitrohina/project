FROM python:3.7.1

RUN mkdir -p usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
RUN rm -f blog.db
RUN python ./db_create.py

EXPOSE 5000

ENV TZ Europe/Moscow

CMD ["python", "app.py"]