# Code by Brave AI
from pydantic import ValidationError
from pydantic_yaml import to_yaml_str
import json
from models.codemeta.v3_1.codemeta_pydantic import Software
from crosswalks.codemeta_to_citation_cff import get_citation_file_format_from_codemeta_software, get_pydantic_model_from_dict
import sys
import subprocess

status = 1

def validate_cff(citation_cff_yaml_str):
    # Assuming the CITATION.cff file is in the current directory
    result = subprocess.run(["cffconvert", "--validate"], capture_output=True, text=True)

    ret = result.returncode == 0
    
    if not ret:
        print("ERROR: cffconvert validation failed.", result.stderr, file=sys.stderr)

    return ret

def convert(codemeta_path: str):
    # codemeta_path = 'tests/data/in/codemeta-codemeta-3.0.json'
    # codemeta_path = 'tests/data/in/codemeta-isicily.json'

    ret = 1

    codemeta_data = None

    # Load and parse the JSON file
    try:
        with open(codemeta_path, 'r') as f:
            codemeta_data = json.load(f)
    except Exception as e:
        print(f'ERROR: {e}', file=sys.stderr)

    if codemeta_data:
        codemeta_software = get_pydantic_model_from_dict(codemeta_data, Software)

        if codemeta_software:
            citation_cff = get_citation_file_format_from_codemeta_software(codemeta_software)

            if citation_cff:
                citation_cff_yaml_str = to_yaml_str(citation_cff, exclude_none=True)
                print(citation_cff_yaml_str)
                
                if validate_cff(citation_cff_yaml_str):
                    ret = 0

    return ret

import argparse

parser = argparse.ArgumentParser(description='Codemeta converter')
parser.add_argument('--file', '-f', 
                    default='codemeta.json', 
                    help='Path to the input file (default: input.txt)')
args = parser.parse_args()

if args.file:
    status = convert(args.file)

sys.exit(status)
