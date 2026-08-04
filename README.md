Toolbox to assist with software development credits

status: quick prototype

## convert a codemeta.json file into citation.cff

`python validate-codemeta.py tests/data/in/codemeta-isciliy.json 2>tests/data/out/errors.json 1>tests/data/out/CITATION.cff`

## Pre-requisites

### install python environment

```bash
python -m venv venv
source venv/bin/activate
pip install -f requirements.txt
```
