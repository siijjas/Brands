# Copyright (c) 2025, siijjas and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt, today, add_days

class TailoringJob(Document):
	def validate(self):
		"""Validate tailoring job data"""
		self.calculate_total_amount()
		self.validate_dates()
		self.validate_measurement_profile()
		
	def calculate_total_amount(self):
		"""Calculate total amount based on quantity and rate"""
		self.total_amount = flt(self.quantity) * flt(self.rate)
		
	def validate_dates(self):
		"""Validate order and delivery dates"""
		if self.expected_delivery_date and self.order_date:
			if self.expected_delivery_date < self.order_date:
				frappe.throw("Expected delivery date cannot be before order date")
				
	def validate_measurement_profile(self):
		"""Validate measurement profile if provided"""
		if self.measurement_profile:
			profile_doc = frappe.get_doc("Measurement Profile", self.measurement_profile)
			if profile_doc.customer != self.customer:
				frappe.throw("Customer mismatch with Measurement Profile")
				
	def on_submit(self):
		"""Actions to perform when tailoring job is submitted"""
		self.status = "Confirmed"
		if self.auto_create_sales_order:
			self.create_sales_order()
			
	def on_cancel(self):
		"""Actions to perform when tailoring job is cancelled"""
		self.status = "Cancelled"
		
	def create_sales_order(self):
		"""Create Sales Order from Tailoring Job"""
		if self.sales_order:
			frappe.throw("Sales Order already exists for this Tailoring Job")
			
		sales_order = frappe.new_doc("Sales Order")
		sales_order.customer = self.customer
		sales_order.delivery_date = self.expected_delivery_date
		sales_order.transaction_date = self.order_date
		
		# Add item row
		sales_order.append("items", {
			"item_code": self.get_or_create_item_code(),
			"item_name": f"{self.garment_type} - {self.customer_name}",
			"description": f"Custom {self.garment_type} for {self.customer_name}",
			"qty": self.quantity,
			"rate": self.rate,
			"amount": self.total_amount,
			"delivery_date": self.expected_delivery_date
		})
		
		sales_order.flags.ignore_permissions = True
		sales_order.save()
		sales_order.submit()
		
		# Link back to tailoring job
		self.sales_order = sales_order.name
		self.save()
		
		frappe.msgprint(f"Sales Order {sales_order.name} created successfully")
		
	def create_sales_invoice(self):
		"""Create Sales Invoice from Tailoring Job"""
		if self.sales_invoice:
			frappe.throw("Sales Invoice already exists for this Tailoring Job")
			
		sales_invoice = frappe.new_doc("Sales Invoice")
		sales_invoice.customer = self.customer
		sales_invoice.posting_date = today()
		
		# Add item row
		sales_invoice.append("items", {
			"item_code": self.get_or_create_item_code(),
			"item_name": f"{self.garment_type} - {self.customer_name}",
			"description": f"Custom {self.garment_type} for {self.customer_name}",
			"qty": self.quantity,
			"rate": self.rate,
			"amount": self.total_amount
		})
		
		sales_invoice.flags.ignore_permissions = True
		sales_invoice.save()
		if self.auto_create_sales_invoice:
			sales_invoice.submit()
		
		# Link back to tailoring job
		self.sales_invoice = sales_invoice.name
		self.save()
		
		frappe.msgprint(f"Sales Invoice {sales_invoice.name} created successfully")
		
	def get_or_create_item_code(self):
		"""Get or create item code for the garment"""
		item_code = f"CUSTOM-{self.garment_type.upper().replace(' ', '-')}"
		
		if not frappe.db.exists("Item", item_code):
			item = frappe.new_doc("Item")
			item.item_code = item_code
			item.item_name = f"Custom {self.garment_type}"
			item.item_group = "Services"  # or create a specific item group
			item.stock_uom = "Nos"
			item.is_stock_item = 0
			item.is_sales_item = 1
			item.is_purchase_item = 0
			item.flags.ignore_permissions = True
			item.save()
			
		return item_code
		
	def update_progress(self, percentage, stage=None):
		"""Update progress percentage and stage"""
		self.progress_percentage = percentage
		if stage:
			self.current_stage = stage
			
		# Update status based on progress
		if percentage == 100:
			self.status = "Completed"
		elif percentage > 0:
			self.status = "In Production"
			
		self.save()
		frappe.msgprint(f"Progress updated to {percentage}%")
		
	@frappe.whitelist()
	def create_fitting_appointment(self):
		"""Create a fitting appointment for this job"""
		appointment = frappe.new_doc("Fitting Appointment")
		appointment.customer = self.customer
		appointment.tailoring_job = self.name
		appointment.appointment_type = "Initial Fitting"
		appointment.appointment_date = add_days(today(), 7)  # Default to 7 days from now
		
		return appointment