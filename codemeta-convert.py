# Code by Brave AI
from pydantic import ValidationError
from pydantic_yaml import to_yaml_str
import json
from models.codemeta.v3_1.codemeta_pydantic import Software
from crosswalks.codemeta_to_citation_cff import get_citation_file_format_from_codemeta_software, get_pydantic_model_from_dict
import sys

status = 1

# codemeta_path = 'tests/data/in/codemeta-codemeta-3.0.json'
codemeta_path = 'tests/data/in/codemeta-isicily.json'

# Load and parse the JSON file
with open(codemeta_path, 'r') as f:
    codemeta_data = json.load(f)

codemeta_software = get_pydantic_model_from_dict(codemeta_data, Software)

if codemeta_software:
    citation_cff = get_citation_file_format_from_codemeta_software(codemeta_software)

    if citation_cff:
        print(to_yaml_str(citation_cff, exclude_none=True))
        status = 0

sys.exit(status)
