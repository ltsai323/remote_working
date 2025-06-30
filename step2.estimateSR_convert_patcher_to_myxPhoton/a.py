import json

def format_json(input_file, output_file, indent=4):
    try:
        # Load the JSON data from the input file
        with open(input_file, 'r', encoding='utf-8') as infile:
            data = json.load(infile)
        
        # Write the formatted JSON data to the output file
        with open(output_file, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, indent=indent, ensure_ascii=False)
        
        print(f"Formatted JSON saved to {output_file}")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    input_json_file = "data/Photon_scale_smearing.json"  # Change to your input file name
    output_json_file = "formatted_photon_scale_smear.json"  # Change to your output file name
    format_json(input_json_file, output_json_file)

