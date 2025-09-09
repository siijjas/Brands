// Tailoring Job List Script for Kanban View
frappe.listview_settings['Tailoring Job'] = {
	add_fields: ["status", "priority", "progress_percentage", "current_stage", "expected_delivery_date"],
	
	get_indicator: function(doc) {
		var status_colors = {
			"Draft": "red",
			"Confirmed": "blue", 
			"In Production": "orange",
			"Fitting Required": "yellow",
			"Completed": "green",
			"Delivered": "green",
			"Cancelled": "red"
		};
		
		return [__(doc.status), status_colors[doc.status], "status,=," + doc.status];
	},
	
	onload: function(listview) {
		// Add Kanban view
		listview.page.add_menu_item(__("Kanban"), function() {
			frappe.set_route('List', 'Tailoring Job', 'Kanban');
		});
	}
};