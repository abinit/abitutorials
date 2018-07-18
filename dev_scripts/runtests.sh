#!/bin/bash
set -e  # exit on first error

#echo "PMG_MAPI_KEY: 8pkvwRLQSCVbW2Fe" > ${HOME}/.pmgrc.yaml

abinit --version
abinit --build
abicheck.py --with-flow

#nosetests -v --with-coverage --cover-package=abipy --logging-level=INFO
#nosetests abipy -v --with-coverage --cover-package=abipy --logging-level=INFO

# Run unit tests with pytest. No doctests if 2.7
pytest tests -v 
#pytest --cov-config .coveragerc --cov=abipy -v  abipy # --doctest-modules 
# This is to run the integration tests (append results)
# pytest --cov-config .coveragerc --cov=abipy --cov-append -v abipy/integration_tests

# Generate documentation
#if [[ "${ABIPY_SPHINX}" == "yes" ]]; then
#    pip install -r ./docs/requirements.txt
#    ./docs/install_reqs.sh;
#    cd ./docs && make && cd ..
#fi
