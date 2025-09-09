// Tailoring Job Form Script
frappe.ui.form.on('Tailoring Job', {
	refresh: function(frm) {
		// Add custom buttons
		if (frm.doc.docstatus === 1) {
			frm.add_custom_button(__('Create Sales Invoice'), function() {
				frm.call('create_sales_invoice');
			});
			
			frm.add_custom_button(__('Create Fitting Appointment'), function() {
				frm.call('create_fitting_appointment').then(r => {
					if (r.message) {
						frappe.new_doc('Fitting Appointment', r.message);
					}
				});
			});
			
			frm.add_custom_button(__('Update Progress'), function() {
				let d = new frappe.ui.Dialog({
					title: 'Update Progress',
					fields: [
						{
							label: 'Progress Percentage',
							fieldname: 'progress',
							fieldtype: 'Percent',
							reqd: 1,
							default: frm.doc.progress_percentage
						},
						{
							label: 'Current Stage',
							fieldname: 'stage',
							fieldtype: 'Select',
							options: 'Measurement\nCutting\nSewing\nFitting\nFinal Touches\nDelivery',
							default: frm.doc.current_stage
						}
					],
					primary_action_label: 'Update',
					primary_action(values) {
						frm.call('update_progress', {
							percentage: values.progress,
							stage: values.stage
						});
						d.hide();
					}
				});
				d.show();
			});
		}
	},
	
	quantity: function(frm) {
		calculate_total(frm);
	},
	
	rate: function(frm) {
		calculate_total(frm);
	}
});

function calculate_total(frm) {
	frm.set_value('total_amount', frm.doc.quantity * frm.doc.rate);
}