# Copyright (c) 2025, siijjas and contributors
# For license information, please see license.txt

"""
Demo data setup for Tailor Management App
This module helps create sample data for testing the app
"""

import frappe
from frappe.utils import today, add_days

def create_demo_data():
    """Create demo customers, measurement profiles, and tailoring jobs"""
    
    # Check if demo data already exists
    if frappe.db.exists("Measurement Profile", {"customer": "Demo Customer 1"}):
        print("Demo data already exists. Skipping...")
        return
    
    # Create demo customers if they don't exist
    demo_customers = [
        {"customer_name": "Demo Customer 1", "customer_group": "Individual", "territory": "All Territories"},
        {"customer_name": "Demo Customer 2", "customer_group": "Individual", "territory": "All Territories"}
    ]
    
    for customer_data in demo_customers:
        if not frappe.db.exists("Customer", customer_data["customer_name"]):
            customer = frappe.new_doc("Customer")
            customer.customer_name = customer_data["customer_name"]
            customer.customer_group = customer_data["customer_group"] 
            customer.territory = customer_data["territory"]
            customer.save()
            customer.submit()
            print(f"Created customer: {customer.customer_name}")
    
    # Create measurement profiles
    measurement_profiles = [
        {
            "customer": "Demo Customer 1",
            "measurements": [
                {"garment_type": "Shirt", "measurement_name": "Chest", "measurement_value": 42, "unit_of_measurement": "inches"},
                {"garment_type": "Shirt", "measurement_name": "Waist", "measurement_value": 36, "unit_of_measurement": "inches"},
                {"garment_type": "Shirt", "measurement_name": "Arm Length", "measurement_value": 25, "unit_of_measurement": "inches"},
                {"garment_type": "Trousers", "measurement_name": "Waist", "measurement_value": 34, "unit_of_measurement": "inches"},
                {"garment_type": "Trousers", "measurement_name": "Inseam", "measurement_value": 32, "unit_of_measurement": "inches"}
            ]
        },
        {
            "customer": "Demo Customer 2", 
            "measurements": [
                {"garment_type": "Suit Jacket", "measurement_name": "Chest", "measurement_value": 40, "unit_of_measurement": "inches"},
                {"garment_type": "Suit Jacket", "measurement_name": "Shoulder Width", "measurement_value": 18, "unit_of_measurement": "inches"},
                {"garment_type": "Dress", "measurement_name": "Bust", "measurement_value": 36, "unit_of_measurement": "inches"},
                {"garment_type": "Dress", "measurement_name": "Hip", "measurement_value": 38, "unit_of_measurement": "inches"}
            ]
        }
    ]
    
    created_profiles = []
    for profile_data in measurement_profiles:
        mp = frappe.new_doc("Measurement Profile")
        mp.customer = profile_data["customer"]
        mp.date = today()
        
        for measurement in profile_data["measurements"]:
            mp.append("measurements", measurement)
        
        mp.save()
        mp.submit()
        created_profiles.append(mp.name)
        print(f"Created measurement profile: {mp.name}")
    
    # Create tailoring jobs
    tailoring_jobs = [
        {
            "customer": "Demo Customer 1",
            "measurement_profile": created_profiles[0],
            "garment_type": "Shirt",
            "fabric_details": "Premium cotton fabric, light blue color",
            "rate": 150.00,
            "status": "In Production",
            "progress_percentage": 45,
            "current_stage": "Sewing",
            "priority": "Medium",
            "expected_delivery_date": add_days(today(), 14)
        },
        {
            "customer": "Demo Customer 2",
            "measurement_profile": created_profiles[1],
            "garment_type": "Suit Jacket", 
            "fabric_details": "Wool blend, charcoal grey",
            "rate": 350.00,
            "status": "Draft",
            "progress_percentage": 10,
            "current_stage": "Measurement",
            "priority": "High",
            "expected_delivery_date": add_days(today(), 21)
        },
        {
            "customer": "Demo Customer 1",
            "garment_type": "Trousers",
            "fabric_details": "Cotton blend, navy blue",
            "rate": 120.00,
            "status": "Completed",
            "progress_percentage": 100,
            "current_stage": "Delivery",
            "priority": "Low",
            "expected_delivery_date": add_days(today(), -5)
        }
    ]
    
    for job_data in tailoring_jobs:
        tj = frappe.new_doc("Tailoring Job")
        for key, value in job_data.items():
            tj.set(key, value)
        
        tj.order_date = today()
        tj.save()
        
        if job_data["status"] != "Draft":
            tj.submit()
            
        print(f"Created tailoring job: {tj.name}")
    
    # Create fitting appointments
    fitting_appointments = [
        {
            "customer": "Demo Customer 1",
            "appointment_type": "First Fitting",
            "appointment_date": add_days(today(), 3),
            "appointment_time": "10:00:00",
            "status": "Scheduled",
            "notes": "First fitting for blue shirt"
        },
        {
            "customer": "Demo Customer 2",
            "appointment_type": "Initial Fitting", 
            "appointment_date": add_days(today(), 7),
            "appointment_time": "14:30:00",
            "status": "Confirmed",
            "notes": "Initial consultation for suit jacket"
        }
    ]
    
    for appt_data in fitting_appointments:
        fa = frappe.new_doc("Fitting Appointment")
        for key, value in appt_data.items():
            fa.set(key, value)
        
        fa.save()
        fa.submit()
        print(f"Created fitting appointment: {fa.name}")
    
    frappe.db.commit()
    print("\n🎉 Demo data created successfully!")
    print("You can now explore the Tailor Management module with sample data.")

if __name__ == "__main__":
    create_demo_data()