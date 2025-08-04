import pandas as pd
import google.generativeai as genai
import dotenv
import json
import ast
from datetime import datetime
import os

dotenv.load_dotenv()
GENAI_API_KEY = os.getenv('GOOGLE_API_KEY')

try:
    genai.configure(api_key=GENAI_API_KEY)
except KeyError:
    print("ERROR: GOOGLE_API_KEY environment variable not set.")
    print("Please set your API key to run the script.")
    exit()

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-1.5-flash-latest') # Using the fast and efficient model
generation_config = genai.GenerationConfig(
    temperature=0.4
)

# Define the CSV file name and the output JSON file name
INPUT_CSV_FILE = 'extracted_data.csv'
OUTPUT_JSON_FILE = 'processed_data.json'

# --- The Prompt for the Gemini API ---
# This prompt contains all the rules, context, and the desired output format.
prompt_template = """
You are an expert data processor. Your task is to analyze a list of raw material names from a recycling facility and map them to a predefined, structured format.

**Instructions:**
1.  Based on the "MATERIALS" list below, you must determine the appropriate `materials_category`. A facility can belong to multiple categories.
2.  You must map each material to one or more of the official `materials_accepted` items from the "OFFICIAL LIST".
3.  Your output **must be only a valid JSON object** with two keys: "materials_category" and "materials_accepted". Do not include any other text, explanations, or markdown formatting like ```json.
4.  Return all the materials in the same order as they appear in the input list. 
5. Return all the materials in the materials_accepted list, even if they are not in the official list

**OFFICIAL LIST (Ground Truth):**
- **Electronics** (This is the group tag [Materials_Category]): 
1.   Computers, Laptops, Tablets 
2.   Monitors, TVs (CRT & Flat Screen) 
3.   Cell Phones, Smartphones 
4.   Printers, Copiers, Fax Machines 
5.   Audio/Video Equipment 
6.   Gaming Consoles 
7.   Small Appliances (Microwaves, Toasters, etc.) 
8.   Computer Peripherals (Keyboards, Mice, Cables, etc.) 
- **Batteries** (This is the group tag [Materials_Category]): 
1.   Household Batteries (AA, AAA, 9V, etc.) 
2.   Rechargeable Batteries 
3.   Lithium-ion Batteries 
4.   Button/Watch Batteries 
5.   Power Tool Batteries 
6.   E-bike/Scooter Batteries 
7.   Car/Automotive Batteries 
- **Paint & Chemicals** (This is the group tag [Materials_Category]): 
1.   Latex/Water-based Paint 
2.   Oil-based Paint and Stains 
3.   Spray Paint 
4.   Paint Thinners and Solvents 
5.   Household Cleaners 
6.   Pool Chemicals 
7.   Pesticides and Herbicides 
8.   Automotive Fluids (Oil, Antifreeze) 
- **Medical Sharps** (This is the group tag [Materials_Category]): 
1.   Needles and Syringes 
2.   Lancets 
3.   Auto-injectors (EpiPens) 
4.   Insulin Pens 
5.   Home Dialysis Equipment 
- **Textiles & Clothing** (This is the group tag [Materials_Category]): 
1.   Clothing and Shoes 
2.   Household Textiles (Towels, Bedding) 
3.   Fabric Scraps 
4.   Accessories (Belts, Bags, etc.) 
- **Other Important Materials** (This is the group tag [Materials_Category]): 
1.   Fluorescent Bulbs and CFLs 
2.   Mercury Thermometers 
3.   Smoke Detectors 
4.   Fire Extinguishers 
5.   Propane Tanks 
6.   Mattresses and Box Springs 
7.   Large Appliances (Fridges, Washers, etc.) 
8.   Construction Debris (Residential Quantities)

**MATERIALS ACCEPTED from the facility:**
{materials}

**Required Output (JSON only):**
{{
  "materials_category": ["List of categories based on the raw materials"],
  "materials_accepted": ["List of mapped items from the OFFICIAL LIST"]
}}
"""

def process_data():
    """Reads the CSV, processes each row with the Gemini API, and saves the result."""
    try:
        df = pd.read_csv(INPUT_CSV_FILE)
    except FileNotFoundError:
        print(f"ERROR: Input file '{INPUT_CSV_FILE}' not found.")
        return

    all_processed_records = []

    for index, row in df.iterrows():
        print(f"Processing '{row['buisness_name']}'...")

        # Safely evaluate the string representation of the list
        try:
            materials_list = ast.literal_eval(row['materials_accepted'])
        except (ValueError, SyntaxError):
            print(f"  - Could not parse materials for {row['buisness_name']}. Skipping.")
            continue
            
        # Format the prompt with the current row's data
        prompt = prompt_template.format(materials=json.dumps(materials_list))

        try:
            # Call the Gemini API
            response = model.generate_content(prompt, generation_config=generation_config)
            
            # Clean up the response from the model
            response_text = response.text.strip().replace("```json", "").replace("```", "")
            
            # Parse the JSON response from the API
            classified_data = json.loads(response_text)

            # Reformat the date from "Updated Feb 23, 2016" to "2016-02-23"
            date_str = row['last_updated'].replace('Updated ', '')
            try:
                date_obj = datetime.strptime(date_str, '%b %d, %Y')
                formatted_date = date_obj.strftime('%Y-%m-%d')
            except ValueError:
                formatted_date = None # Handle cases where date format is unexpected

            # Build the final JSON record for this row
            processed_record = {
                "business_name": row['buisness_name'],
                "last_update_date": formatted_date,
                "street_address": row['address'],
                "materials_category": classified_data.get("materials_category", []),
                "materials_accepted": classified_data.get("materials_accepted", [])
            }
            all_processed_records.append(processed_record)

        except Exception as e:
            print(f"  - An error occurred while processing {row['buisness_name']}: {e}")

    # Save the final list of dictionaries to a JSON file
    with open(OUTPUT_JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_processed_records, f, indent=4)

    print(f"\nProcessing complete. Data saved to '{OUTPUT_JSON_FILE}'")

# Run the main function
if __name__ == "__main__":
    process_data()