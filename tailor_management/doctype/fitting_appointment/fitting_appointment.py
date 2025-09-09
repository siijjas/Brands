# Copyright (c) 2025, siijjas and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, now_datetime

class FittingAppointment(Document):
	def validate(self):
		"""Validate fitting appointment data"""
		self.validate_appointment_date()
		self.validate_tailoring_job()
		
	def validate_appointment_date(self):
		"""Ensure appointment date is not in the past"""
		if getdate(self.appointment_date) < getdate():
			frappe.throw("Appointment date cannot be in the past")
			
	def validate_tailoring_job(self):
		"""Validate tailoring job if provided"""
		if self.tailoring_job:
			job_doc = frappe.get_doc("Tailoring Job", self.tailoring_job)
			if job_doc.customer != self.customer:
				frappe.throw("Customer mismatch with Tailoring Job")
				
	def on_submit(self):
		"""Actions to perform when appointment is submitted"""
		self.status = "Confirmed"
		
	def on_cancel(self):
		"""Actions to perform when appointment is cancelled"""
		self.status = "Cancelled"
		
	def mark_completed(self):
		"""Mark the appointment as completed"""
		self.status = "Completed"
		self.save()
		frappe.msgprint("Appointment marked as completed")