FROM python:3.9.5-alpine3.13

RUN apk update && apk add git npm
RUN npm install -g codefresh
RUN pip install pyyaml

CMD ["/bin/sh"]