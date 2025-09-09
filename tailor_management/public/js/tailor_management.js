// Tailor Management App JavaScript
frappe.provide("tailor_management");

tailor_management.utils = {
	get_status_color: function(status) {
		const color_map = {
			'Draft': 'red',
			'Confirmed': 'blue', 
			'In Production': 'orange',
			'Fitting Required': 'yellow',
			'Completed': 'green',
			'Delivered': 'green',
			'Cancelled': 'red'
		};
		return color_map[status] || 'grey';
	},
	
	get_priority_indicator: function(priority) {
		const indicators = {
			'Low': 'blue',
			'Medium': 'orange',
			'High': 'red',
			'Urgent': 'red blink'
		};
		return indicators[priority] || 'grey';
	},
	
	format_measurement_display: function(measurements) {
		if (!measurements || !measurements.length) return '';
		
		let display = '';
		measurements.forEach(m => {
			display += `${m.garment_type}: ${m.measurement_name} = ${m.measurement_value} ${m.unit_of_measurement}\n`;
		});
		return display.trim();
	}
};

// Global functions
window.tailor_management = tailor_management;