# Code by Brave AI
from pydantic import ValidationError
from pydantic_yaml import to_yaml_str
import json
from models.codemeta.v3_1.codemeta_pydantic_desc import Software
from crosswalks.codemeta_to_citation_cff import get_citation_file_format_from_codemeta_software

codemeta_path = 'tests/data/codemeta-codemeta-3.0.json'
# codemeta_path = 'tests/data/codemeta-isicily.json'

# Load and parse the JSON file
with open(codemeta_path, 'r') as f:
    json_data = json.load(f)

# Validate against the Pydantic model
try:
    # validated_product = Software(**json_data)
    codemeta_software = Software.model_validate(json_data)
    print("Data structure is valid:", codemeta_software)
    # print(codemeta_obj.model_dump_json(by_alias=True, exclude_none=True, indent=2))
except ValidationError as e:
    print("Validation failed:")   
    for error in e.errors():
        print(error)

citation_cff = get_citation_file_format_from_codemeta_software(codemeta_software)

print(to_yaml_str(citation_cff, exclude_none=True))
