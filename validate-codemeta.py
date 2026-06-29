# Code by Brave AI
from pydantic import BaseModel, ValidationError
from pydantic_yaml import to_yaml_str
from typing import Optional
import json
from models.codemeta.v3_1.codemeta_pydantic_desc import Software
from models.citation_cff.v1_2_0.citation_cff_pydantic import CitationFileFormat, Person, Entity

codemeta_path = 'tests/data/codemeta-codemeta-3.0.json'
codemeta_path = 'tests/data/codemeta-isicily.json'

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

def convert_agent(agent):
    if agent.type_ == 'Organization':
        ret = {
            "name": agent.name,
        }
        ret = Entity(**ret)
    else:
        ret = {
            "given-names": agent.givenName,
            "family-names": agent.familyName,
        }
        ret = Person(**ret)
    return ret

data = {
    "authors": [convert_agent(a) for a in codemeta_software.author],
    "title": codemeta_software.name,
    "repository": codemeta_software.codeRepository
}
citation_cff = CitationFileFormat(**data)

print(to_yaml_str(citation_cff, exclude_none=True))
