import models.codemeta.v3_1.codemeta_pydantic as cm
import models.citation_cff.v1_2_0.citation_cff_pydantic as cff

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

    return cff.CitationFileFormat(**cff_data)
