FROM public.ecr.aws/docker/library/python:3-bookworm
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY app/requirements.txt ./app/
RUN pip install -r ./app/requirements.txt
COPY app/ /usr/src/app/
CMD ["flask", "--app", "app\/app", "run", "--host=0.0.0.0", "--port=8080"]
