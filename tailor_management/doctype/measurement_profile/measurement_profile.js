// Measurement Profile Form Script
frappe.ui.form.on('Measurement Profile', {
	refresh: function(frm) {
		if (frm.doc.docstatus === 1) {
			frm.add_custom_button(__('Create Tailoring Job'), function() {
				frappe.new_doc('Tailoring Job', {
					'customer': frm.doc.customer,
					'measurement_profile': frm.doc.name
				});
			});
		}
	},
	
	customer: function(frm) {
		// Clear measurements when customer changes
		frm.clear_table("measurements");
		frm.refresh_field("measurements");
	}
});

frappe.ui.form.on('Garment Measurement', {
	measurement_value: function(frm, cdt, cdn) {
		// Could add validation for measurement values here
		let row = locals[cdt][cdn];
		if (row.measurement_value < 0) {
			frappe.msgprint(__('Measurement value cannot be negative'));
			frappe.model.set_value(cdt, cdn, 'measurement_value', 0);
		}
	}
});