Toolbox to assist with software development credits

status: quick prototype

## convert a codemeta.json file into citation.cff

`python validate-codemeta.py tests/data/in/codemeta-isciliy.json 2>tests/data/out/errors.json 1>tests/data/out/CITATION.cff`

Returns 0 status if the conversion was completed

Any input or output which is invalid according to their resepctive standard causes an error.

## Pre-requisites

### install python environment

```bash
python -m venv venv
source venv/bin/activate
pip install -f requirements.txt
```
