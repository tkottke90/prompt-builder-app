#! /bin/bash



cd $(dirname $0)
cd ..

# Check for Virtual Env
if [ ! -d ./.venv ]; then
  echo "> Setting up Virtual Environment...."
  python3.11 -m <env name> <directory name>
else
  echo "> Virtual Environment Found. Skipping....."
fi

# Check for Test Script
if [ ! -f "./.venv/bin/test-code" ]; then
  ln -s ./bin/test.sh ./.venv/bin/test-code
else
  echo "> Scripts Setup.  Skipping...."
fi
