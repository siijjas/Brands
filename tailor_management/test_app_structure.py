# Copyright (c) 2025, siijjas and contributors
# For license information, please see license.txt

"""
Test module for Tailor Management App DocTypes
This file can be used to validate the DocType relationships and basic functionality
"""

def validate_doctype_structure():
    """Validate that all DocTypes have the required structure"""
    import json
    import os
    
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    doctype_path = os.path.join(base_path, 'doctype')
    
    required_doctypes = [
        'garment_measurement',
        'measurement_profile', 
        'tailoring_job',
        'fitting_appointment'
    ]
    
    for doctype in required_doctypes:
        json_file = os.path.join(doctype_path, doctype, f'{doctype}.json')
        py_file = os.path.join(doctype_path, doctype, f'{doctype}.py')
        
        # Check if files exist
        assert os.path.exists(json_file), f"Missing JSON file for {doctype}"
        assert os.path.exists(py_file), f"Missing Python file for {doctype}"
        
        # Validate JSON structure
        with open(json_file, 'r') as f:
            doctype_json = json.load(f)
            assert doctype_json.get('doctype') == 'DocType', f"Invalid DocType structure for {doctype}"
            assert doctype_json.get('name'), f"Missing name field for {doctype}"
            assert doctype_json.get('fields'), f"Missing fields for {doctype}"
    
    print("✓ All DocTypes have valid structure")

def validate_relationships():
    """Validate DocType relationships"""
    import json
    import os
    
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    doctype_path = os.path.join(base_path, 'doctype')
    
    # Check Measurement Profile has child table
    mp_file = os.path.join(doctype_path, 'measurement_profile', 'measurement_profile.json')
    with open(mp_file, 'r') as f:
        mp_data = json.load(f)
        measurements_field = None
        for field in mp_data['fields']:
            if field['fieldname'] == 'measurements':
                measurements_field = field
                break
        assert measurements_field, "Missing measurements child table in Measurement Profile"
        assert measurements_field['fieldtype'] == 'Table', "measurements should be Table field"
        assert measurements_field['options'] == 'Garment Measurement', "measurements should link to Garment Measurement"
    
    # Check Tailoring Job has links
    tj_file = os.path.join(doctype_path, 'tailoring_job', 'tailoring_job.json')
    with open(tj_file, 'r') as f:
        tj_data = json.load(f)
        has_mp_link = False
        has_customer_link = False
        for field in tj_data['fields']:
            if field['fieldname'] == 'measurement_profile' and field['options'] == 'Measurement Profile':
                has_mp_link = True
            if field['fieldname'] == 'customer' and field['options'] == 'Customer':
                has_customer_link = True
        assert has_mp_link, "Tailoring Job missing Measurement Profile link"
        assert has_customer_link, "Tailoring Job missing Customer link"
    
    # Check Fitting Appointment has Tailoring Job link
    fa_file = os.path.join(doctype_path, 'fitting_appointment', 'fitting_appointment.json')
    with open(fa_file, 'r') as f:
        fa_data = json.load(f)
        has_tj_link = False
        for field in fa_data['fields']:
            if field['fieldname'] == 'tailoring_job' and field['options'] == 'Tailoring Job':
                has_tj_link = True
                break
        assert has_tj_link, "Fitting Appointment missing Tailoring Job link"
    
    print("✓ All DocType relationships are valid")

if __name__ == "__main__":
    try:
        validate_doctype_structure()
        validate_relationships()
        print("\n🎉 All validations passed! The Tailor Management App structure is correct.")
    except Exception as e:
        print(f"\n❌ Validation failed: {e}")
        exit(1)