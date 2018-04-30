FROM python:3
ADD . /usr/src/app
RUN cd /usr/src/app&&pip install -r requirements.txt&&python setup.py sdist&&pip install dist/*.tar.gz