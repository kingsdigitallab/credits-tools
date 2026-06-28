The Pydantic model was generated from citation.cff json schema like this:

```bash
mkdir v1_2_0
cd v1_2_0
wget https://raw.githubusercontent.com/citation-file-format/citation-file-format/0c5b4aa07071490eaf261775ce96ccdd13a6e2d5/schema.json
datamodel-codegen  --input schema.json --input-file-type jsonschema --output citation_cff_pydantic.py
```
