#!/bin/bash
set -e  # exit on first error

echo "PMG_MAPI_KEY: 8pkvwRLQSCVbW2Fe" > ${HOME}/.pmgrc.yaml

abinit --version
abinit --build
abicheck.py --with-flow

# Run unit tests with pytest.
if [[ "${ABIPY_PYTEST}" == "yes" ]]; then 
    pytest --cov-config=.coveragerc --cov=abitutorials -v tests 
fi

# Generate documentation
#if [[ "${ABIPY_SPHINX}" == "yes" ]]; then
#    pip install -r ./docs/requirements.txt
#    ./docs/install_reqs.sh;
#    cd ./docs && make && cd ..
#fi
