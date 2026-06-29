from pydantic_yaml import to_yaml_str
from models.codemeta.v3_1.codemeta_pydantic_desc import Software
from models.citation_cff.v1_2_0.citation_cff_pydantic import CitationFileFormat, Person, Entity

def get_cff_agent(agent):
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

def get_citation_file_format_from_codemeta_software(codemeta_software: Software) -> CitationFileFormat:
    soft = codemeta_software
    
    cff = {
        "authors": [get_cff_agent(a) for a in soft.author],
        "title": soft.name,
        "repository": soft.codeRepository
    }

    return CitationFileFormat(**cff)
