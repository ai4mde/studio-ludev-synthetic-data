import sys
import json
from utils.loading_json_utils import get_apps, authentication_is_present, use_synthetic_data_is_present, get_synthetic_instructions, get_synthetic_counts, get_synthetic_instructions_per_node

def main():
    if (len(sys.argv) >= 3 and str(sys.argv[1]) == "get_apps"):
        print(get_apps(sys.argv[2]))

    if (len(sys.argv) >= 3 and str(sys.argv[1]) == "get_auth"):
        print(authentication_is_present(sys.argv[2]))

    if (len(sys.argv) >= 3 and str(sys.argv[1]) == "get_synth"):
        print(use_synthetic_data_is_present(sys.argv[2]))
    
    if len(sys.argv) >= 3 and sys.argv[1] == "get_instr":
        print(get_synthetic_instructions(sys.argv[2]))

    if len(sys.argv) >= 3 and sys.argv[1] == "get_counts":
        print(json.dumps(get_synthetic_counts(sys.argv[2])))
    
    if len(sys.argv) >= 3 and sys.argv[1] == "get_instr_per_node":
        print(json.dumps(get_synthetic_instructions_per_node(sys.argv[2])))

if __name__ == "__main__":
    main()