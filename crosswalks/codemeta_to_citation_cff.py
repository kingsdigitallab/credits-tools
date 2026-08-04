import models.codemeta.v3_1.codemeta_pydantic as cm
import models.citation_cff.v1_2_0.citation_cff_pydantic as cff
from pydantic import BaseModel, ValidationError
import sys

def get_cff_agent(agent: cm.Organization | cm.Person):
    if agent.type_ == 'Organization':
        ret = {
            "name": agent.name,
        }
        ret = cff.Entity(**ret)
    else:
        ret = {
            "given-names": agent.givenName,
            "family-names": agent.familyName,
        }
        ret = cff.Person(**ret)
    return ret

def get_citation_file_format_from_codemeta_software(codemeta_software: cm.Software) -> cff.CitationFileFormat:
    soft = codemeta_software
    
    cff_data = {
        "authors": [get_cff_agent(a) for a in soft.author],
        "title": soft.name,
        "repository": soft.codeRepository
    }

    return get_pydantic_model_from_dict(cff_data, cff.CitationFileFormat)

def get_pydantic_model_from_dict(data: dict, pydantic_model: BaseModel):
    ret = None

    try:
        ret = pydantic_model.model_validate(data)
    except ValidationError as e:
        print(f"ERROR: Validation failed ({pydantic_model.__name__})", file=sys.stderr)   
        for error in e.errors():
            # eg. {'type': 'missing', 'loc': ('authors',), 'msg': 'Field required', 'input': {'title': 'Corpus building edition', 'repository': 'https://github.com/kingsdigitallab/corpus-building'}, 'url': 'https://errors.pydantic.dev/2.13/v/missing'}            
            print(f'ERROR: {error["msg"]}: {error["loc"]}', file=sys.stderr)

    return ret
