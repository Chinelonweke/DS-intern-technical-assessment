import json
from parser import get_data_from_pdf, align_content
from data_processing import extract_data


# Main section
def run_pipeline(pdf_path, output_path):
    """Run the complete data pipeline"""
    try:
        # Step 1: Extract raw text from PDF
        raw_text = get_data_from_pdf(pdf_path)
        
        # Step 2: Align content line by line
        aligned_lines = align_content(raw_text)
        
        # Step 3: Extract and structure data
        structured_data = extract_data(aligned_lines)
        
        # Save output as JSON
        with open(output_path, 'w') as f:
            json.dump(structured_data, f, indent=2)
            
        print(f"Successfully processed PDF. Output saved to {output_path}")
        return True
        
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        return False

if __name__ == "__main__":
    input_pdf = r'C:\Users\Chinelo\DS-intern-technical-assessment\data\home_inventory.pdf'
    output_json =  r'C:\Users\Chinelo\DS-intern-technical-assessment\output'
    
    run_pipeline(input_pdf, output_json)
    
    