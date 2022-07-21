#!/bin/bash
WORKDIR=$(dirname "$0")
cd "$WORKDIR"
echo "start notifier...by $USER / WORKDIR = $(pwd)"
. ./venv/bin/activate
PYV=$(python -c "import sys;t='{v[0]}'.format(v=list(sys.version_info[:1]));sys.stdout.write(t)";)
if [ "$PYV" != "3" ]; then
  echo "Python version should be 3.x"
  exit 1
fi

python ./notifier.py