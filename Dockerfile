FROM python:3.6.6-alpine3.8

RUN apk update && \
  apk upgrade && \
  apk add make automake gcc g++ subversion python3-dev freetype-dev libpng-dev openblas-dev libxml2-dev libxslt-dev

RUN pip install matplotlib jupyterlab jupyter_contrib_nbextensions 
RUN jupyter contrib nbextension install
RUN pip install pyfolio
RUN pip install quantx-sdk

