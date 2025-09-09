// Fitting Appointment Form Script
frappe.ui.form.on('Fitting Appointment', {
	refresh: function(frm) {
		if (frm.doc.docstatus === 1 && frm.doc.status !== 'Completed' && frm.doc.status !== 'Cancelled') {
			frm.add_custom_button(__('Mark as Completed'), function() {
				frm.call('mark_completed');
			});
		}
		
		// Set color coding based on appointment status
		if (frm.doc.status) {
			let color_map = {
				'Scheduled': 'blue',
				'Confirmed': 'green', 
				'Completed': 'green',
				'Rescheduled': 'orange',
				'Cancelled': 'red',
				'No Show': 'red'
			};
			
			frm.dashboard.set_headline_alert(
				frm.doc.status,
				color_map[frm.doc.status] || 'blue'
			);
		}
	},
	
	customer: function(frm) {
		// Filter tailoring jobs by customer
		if (frm.doc.customer) {
			frm.set_query('tailoring_job', function() {
				return {
					filters: {
						'customer': frm.doc.customer,
						'docstatus': 1
					}
				};
			});
		}
	},
	
	tailoring_job: function(frm) {
		// Auto-fill customer when tailoring job is selected
		if (frm.doc.tailoring_job) {
			frappe.db.get_value('Tailoring Job', frm.doc.tailoring_job, 'customer')
				.then(r => {
					if (r.message && r.message.customer) {
						frm.set_value('customer', r.message.customer);
					}
				});
		}
	}
});