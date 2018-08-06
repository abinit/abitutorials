#!/bin/bash
set -e  # exit on first error

echo "PMG_MAPI_KEY: 8pkvwRLQSCVbW2Fe" > ${HOME}/.pmgrc.yaml

abinit --version
abinit --build
abicheck.py --with-flow

#nosetests -v --with-coverage --cover-package=abipy --logging-level=INFO
#nosetests abipy -v --with-coverage --cover-package=abipy --logging-level=INFO

# Run unit tests with pytest. No doctests if 2.7
if [[ "${ABIPY_PYTEST}" == "yes" ]]; then 
    pytest -n 2 --cov-config=.coveragerc --cov=abitutorials -v tests 
fi

# Generate documentation
#if [[ "${ABIPY_SPHINX}" == "yes" ]]; then
#    pip install -r ./docs/requirements.txt
#    ./docs/install_reqs.sh;
#    cd ./docs && make && cd ..
#fi
