# lodb
Linked Open Database

[![Coverage Status](https://coveralls.io/repos/github/sparkd/lodb/badge.svg?branch=master)](https://coveralls.io/github/sparkd/lodb?branch=master)

[![Build Status](https://travis-ci.org/sparkd/lodb.svg?branch=master)](https://travis-ci.org/sparkd/lodb)


## Usage
FLASK_DEBUG=1 python lodb/app.py

FLASK_DEBUG=1 FLASK_APP=lodb/app.py flask load_schema

FLASK_DEBUG=1 FLASK_APP=lodb/app.py flask load_schema http://rs.tdwg.org/dwc/tdwg_dw_core.xsd

## Tests
nosetests tests/test_api.py --nocapture




