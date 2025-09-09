# Copyright (c) 2025, siijjas and contributors
# For license information, please see license.txt

import frappe

def on_submit_handler(doc, method):
	"""Handle actions when Tailoring Job is submitted"""
	pass  # Already handled in the doctype's on_submit method

def on_update_after_submit_handler(doc, method):
	"""Handle actions when Tailoring Job is updated after submit"""
	# Send notifications for status changes
	if doc.has_value_changed("status"):
		send_status_notification(doc)
		
def send_status_notification(doc):
	"""Send notification when status changes"""
	try:
		# Get customer email
		customer_doc = frappe.get_doc("Customer", doc.customer)
		if customer_doc.email_id:
			subject = f"Update on your Tailoring Job {doc.name}"
			message = f"""
			Dear {doc.customer_name},
			
			Your tailoring job has been updated:
			
			Garment: {doc.garment_type}
			Status: {doc.status}
			Progress: {doc.progress_percentage}%
			Current Stage: {doc.current_stage}
			Expected Delivery: {doc.expected_delivery_date}
			
			Thank you for choosing our tailoring services.
			
			Best regards,
			Tailor Management Team
			"""
			
			frappe.sendmail(
				recipients=[customer_doc.email_id],
				subject=subject,
				message=message,
				reference_doctype=doc.doctype,
				reference_name=doc.name
			)
	except Exception as e:
		frappe.log_error(f"Failed to send notification: {str(e)}")
		pass  # Don't fail the transaction for notification errors