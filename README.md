# flask-template

[![travis-ci](https://travis-ci.org/weak-head/flask-template.svg?branch=master)](https://travis-ci.org/weak-head/flask-template)
[![codecov](https://codecov.io/gh/weak-head/flask-template/branch/master/graph/badge.svg)](https://codecov.io/gh/weak-head/flask-template)

```bash
# create virtual environment
python3 -m venv venv
. venv/bin/activate

# install dependencies
pip install flask

# generate coverage report
coverage run -m pytest
coverage report
coverage html

# run the app
export FLASK_APP=fplate
export FLASK_ENV=development
flask run
```