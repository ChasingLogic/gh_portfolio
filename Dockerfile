FROM python:3

RUN mkdir /gh_portfolio
ADD . /gh_portfolio/

WORKDIR /gh_portfolio
RUN pip install -r requirements.txt
