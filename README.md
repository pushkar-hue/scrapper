# scrapper

This project extracts data from Earth911's public recycling search tool and classifies accepted materials into structured recycling categories using Google Gemini 1.5 Flash.

Project Objective

- Scrape relevant data (facility name, address, accepted materials, update info) from Earth911’s electronics recycling search.
  
- Classify accepted materials using a Gemini-powered LLM pipeline to map them into official structured recycling categories.
  
- Output clean, categorized JSON data from the raw site.

## Prompting Strategy
- I used explicit instruction prompting. The prompt was designed to:
- Provide a clear mapping rulebook — the official materials list.
- Present the model with raw scraped material names.
- Instruct the LLM to:
    - Identify material categories (materials_category)
    - Map to official structured material types (materials_accepted)
 
## Prompt Used:
```
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
```
## Tools and Libraries
- Scraping: 	Selenium, BeautifulSoup, Firefox WebDriver
- Data Cleaning: Custom clean_data() function
- LLM Integration: 	google-generativeai with Gemini 1.5 Flash
- Storage & Output: 	pandas, json, csv
  
