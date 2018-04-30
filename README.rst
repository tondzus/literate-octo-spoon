literate-octo-spoon
*******************

Installation
============

1. :code:`git clone https://github.com/tondzus/literate-octo-spoon/`
2. :code:`pip install -r requirements.txt`
3. :code:`python setup.py install`

How to run
==========

:code:`python -m pycoins challenge --api-key <alphavantage-api-key>`

Greatest iso weeks for both memory and sqlite computations will be printed
to the console. The two .csv files will be saved to the current folder - one for
memory and one for sqlite.


Docker
======

Alternatively, after cloning the repository you can build a docker image and
run the challenge code from it.

1. :code:`git clone https://github.com/tondzus/literate-octo-spoon/`
2. :code:`cd literate-octo-spoon`
3. :code:`sudo docker build -t dh-challenge .`
4. :code:`sudo docker run -it -v <absolute-output-path>:/usr/src/app/csvs dh-challenge python -m pycoins challenge --output-folder /usr/src/app/csvs --api-key <alphavantage-api-key>`

Greatest iso weeks for both memory and sqlite computations will be printed
to the console. The two .csv files will be saved to the <absolute-output-path>.
