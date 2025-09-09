# Copyright (c) 2025, siijjas and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MeasurementProfile(Document):
	def validate(self):
		"""Validate measurement profile data"""
		self.validate_measurements()
		
	def validate_measurements(self):
		"""Ensure measurements are valid"""
		if not self.measurements:
			frappe.throw("At least one measurement is required")
			
		# Check for duplicate measurements for same garment type
		seen = set()
		for measurement in self.measurements:
			key = (measurement.garment_type, measurement.measurement_name)
			if key in seen:
				frappe.throw(f"Duplicate measurement found: {measurement.measurement_name} for {measurement.garment_type}")
			seen.add(key)
			
	def on_submit(self):
		"""Actions to perform when measurement profile is submitted"""
		self.status = "Active"
		
	def on_cancel(self):
		"""Actions to perform when measurement profile is cancelled"""
		self.status = "Inactive"