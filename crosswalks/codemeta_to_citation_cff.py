import models.codemeta.v3_1.codemeta_pydantic as cm
import models.citation_cff.v1_2_0.citation_cff_pydantic as cff
from pydantic import BaseModel, ValidationError
import sys

SPDX_URL_PREFIX = "https://spdx.org/licenses/"
SCHEMA_URL_PREFIX = "https://schema.org/"
ORCID_HOST = "orcid.org"
IS_PART_OF_DESCRIPTION = "Part of"
CODEMETA_TO_CFF_TYPE = {
    "SoftwareSourceCode": cff.Type.software,
    "SoftwareApplication": cff.Type.software,
    "Dataset": cff.Type.dataset,
}
VALID_SPDX_IDS = {e.value for e in cff.LicenseEnum}


def get_spdx_id_from_url(license_str: str) -> str | None:
    """Extract the SPDX identifier from an SPDX license URL, e.g. https://spdx.org/licenses/MIT -> MIT."""
    ret = None
    if license_str.startswith(SPDX_URL_PREFIX):
        ret = license_str[len(SPDX_URL_PREFIX):]
    return ret


def get_cff_license(codemeta_license) -> dict:
    """Convert a CodeMeta license value to a CFF 'license' or 'license-url' dict entry."""
    ret = {}
    license_value = codemeta_license
    if isinstance(license_value, list):
        license_value = license_value[0] if license_value else None
    if license_value is None:
        pass
    elif isinstance(license_value, cm.schemaorg.CreativeWork):
        if license_value.url:
            ret = {"license-url": str(license_value.url)}
    else:
        license_str = str(license_value)
        spdx_id = get_spdx_id_from_url(license_str)
        if spdx_id is None and license_str in VALID_SPDX_IDS:
            spdx_id = license_str
        if spdx_id and spdx_id in VALID_SPDX_IDS:
            ret = {"license": spdx_id}
        else:
            ret = {"license-url": license_str}
    return ret


def get_url_from_value(value) -> str | None:
    """Extract a URL string from a str/HttpUrl or a CreativeWork's url/@id."""
    ret = None
    if value is None:
        pass
    elif isinstance(value, cm.schemaorg.CreativeWork):
        if value.url:
            ret = str(value.url)
        elif value.id_:
            ret = value.id_
    else:
        ret = str(value)
    return ret


def get_cff_identifiers_from_is_part_of(codemeta_is_part_of) -> dict:
    """Convert CodeMeta isPartOf URL(s) to a CFF 'identifiers' dict entry (type url, 'Part of' description)."""
    ret = {}
    values = codemeta_is_part_of
    if values is None:
        pass
    else:
        if not isinstance(values, list):
            values = [values]
        identifiers = []
        for v in values:
            url = get_url_from_value(v)
            if url:
                identifiers.append({"type": "url", "value": url, "description": IS_PART_OF_DESCRIPTION})
        if identifiers:
            ret = {"identifiers": identifiers}
    return ret


def get_cff_type(codemeta_type: str | list) -> cff.Type | None:
    """Map a CodeMeta @type to a CFF type (software or dataset)."""
    ret = None
    types = codemeta_type
    if not isinstance(types, list):
        types = [types] if types else []
    for t in types:
        if isinstance(t, str):
            t = t.replace(SCHEMA_URL_PREFIX, "")
            if t in CODEMETA_TO_CFF_TYPE:
                ret = CODEMETA_TO_CFF_TYPE[t]
                break
    return ret


def get_cff_version(soft: cm.Software):
    """Return the version from a CodeMeta Software, preferring 'version' over 'softwareVersion'."""
    ret = soft.version
    if ret is None:
        ret = soft.softwareVersion
    return ret


def get_cff_affiliation(codemeta_affiliation) -> str | None:
    """Extract an affiliation name from a CodeMeta affiliation (Organization or string)."""
    ret = None
    if codemeta_affiliation is None:
        pass
    elif isinstance(codemeta_affiliation, cm.schemaorg.Organization):
        ret = codemeta_affiliation.name
    elif isinstance(codemeta_affiliation, str):
        ret = codemeta_affiliation
    return ret


def get_cff_orcid_from_id(codemeta_id: str | None) -> str | None:
    """Return the ORCID URL from a CodeMeta @id if it is an ORCID identifier."""
    ret = None
    if codemeta_id and ORCID_HOST in codemeta_id:
        ret = codemeta_id
    return ret

def get_cff_agent(agent: cm.Organization | cm.Person):
    if agent.type_ == 'Organization':
        ret = {
            "name": agent.name,
            "email": agent.email,
        }
        ret = cff.Entity(**ret)
    else:
        ret = {
            "given-names": agent.givenName,
            "family-names": agent.familyName,
            "email": agent.email,
            "affiliation": get_cff_affiliation(agent.affiliation),
            "orcid": get_cff_orcid_from_id(agent.id_),
        }
        ret = cff.Person(**ret)
    return ret

def get_citation_file_format_from_codemeta_software(codemeta_software: cm.Software) -> cff.CitationFileFormat:
    soft = codemeta_software

    cff_data = {
        "authors": [get_cff_agent(a) for a in soft.author or []],
        "title": soft.name,
        "repository-code": soft.codeRepository,
        "type": get_cff_type(soft.type_),
        "abstract": soft.description,
        "keywords": soft.keywords,
        "version": get_cff_version(soft),
        "date-released": soft.datePublished,
        "repository-artifact": soft.downloadUrl,
    }

    cff_data.update(get_cff_license(soft.license))
    cff_data.update(get_cff_identifiers_from_is_part_of(soft.isPartOf))

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
