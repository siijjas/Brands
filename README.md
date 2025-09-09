# Tailor Management App for ERPNext v15

A comprehensive ERPNext application designed for managing bespoke tailoring businesses. This app provides a complete workflow from customer measurements to garment delivery, with automated document creation and Kanban-based production tracking.

## Features

### 🏗️ Core DocTypes

1. **Measurement Profile** - Store detailed customer measurements with child table for multiple garments
2. **Tailoring Job** - Central workflow hub for managing production process
3. **Fitting Appointment** - Schedule and track customer fittings
4. **Garment Measurement** - Child table for structured measurement data

### 🚀 Key Capabilities

- **Automated Document Creation**: Auto-generate Sales Orders and Sales Invoices from Tailoring Jobs
- **Kanban Production View**: Visual status tracking with drag-and-drop workflow management
- **Customer Measurement Profiles**: Reusable measurement templates for repeat customers  
- **Fitting Appointment Scheduling**: Integrated appointment management with status tracking
- **Progress Tracking**: Real-time progress updates with percentage completion and stage tracking
- **Email Notifications**: Automatic customer notifications for status updates

### 📊 Workflow Management

- **Status Tracking**: Draft → Confirmed → In Production → Fitting Required → Completed → Delivered
- **Progress Stages**: Measurement → Cutting → Sewing → Fitting → Final Touches → Delivery  
- **Priority Management**: Low, Medium, High, Urgent priority levels
- **Kanban Board**: Visual workflow management with status-based columns

## Installation

### Prerequisites
- ERPNext v15.x
- Frappe Framework v15.x

### Install Steps

1. **Get the App**
   ```bash
   bench get-app https://github.com/siijjas/Brands
   ```

2. **Install on Site**
   ```bash
   bench --site [sitename] install-app tailor_management
   ```

3. **Run Migrations**
   ```bash
   bench --site [sitename] migrate
   ```

4. **Build Assets**
   ```bash
   bench build --app tailor_management
   ```

## Usage Guide

### Setting Up Your First Customer

1. **Create Measurement Profile**
   - Navigate to Tailor Management > Measurement Profile > New
   - Select customer and add garment measurements
   - Submit the profile for use in tailoring jobs

2. **Create Tailoring Job**
   - Go to Tailor Management > Tailoring Job > New  
   - Link measurement profile and set garment details
   - Configure pricing and delivery dates
   - Enable auto-creation of Sales Order if needed

3. **Schedule Fitting Appointment**
   - Create from Tailoring Job or directly
   - Set appointment type (Initial, First Fitting, Final, etc.)
   - Track completion and amendments

### Using the Kanban Board

1. Access via **List View > Kanban** button on Tailoring Job list
2. Drag jobs between status columns:
   - Draft (Red)
   - Confirmed (Blue)  
   - In Production (Orange)
   - Fitting Required (Yellow)
   - Completed (Green)
   - Delivered (Green)

### Automation Features

- **Sales Order Creation**: Automatically generated when Tailoring Job is submitted (if enabled)
- **Sales Invoice Creation**: Can be created manually or automatically based on settings
- **Email Notifications**: Customers receive updates when job status changes
- **Progress Updates**: Use the "Update Progress" button to track completion percentage

## Configuration

### Custom Fields & Settings

The app creates several custom fields and configurations. Key settings include:

- **Naming Series**: Customizable prefixes (MP- for Measurement Profiles, TJ- for Tailoring Jobs, FA- for Fitting Appointments)
- **Status Options**: Configurable status workflows for each DocType
- **Measurement Types**: Pre-defined measurement categories (expandable)
- **Garment Types**: Standard garment categories (customizable)

### Permissions

Default permissions are set for:
- **System Manager**: Full access to all DocTypes
- **Sales User**: Create, read, write, submit access

Additional roles can be configured as needed.

## API Integration

### Whitelisted Methods

Key methods available via API:
- `create_sales_order()` - Generate Sales Order from Tailoring Job
- `create_sales_invoice()` - Generate Sales Invoice from Tailoring Job  
- `update_progress(percentage, stage)` - Update job progress
- `create_fitting_appointment()` - Schedule new appointment

### Webhook Support

Document events trigger notifications:
- `on_submit` - Tailoring Job submission
- `on_update_after_submit` - Status change notifications

## Development

### Project Structure
```
tailor_management/
├── doctype/
│   ├── measurement_profile/
│   ├── tailoring_job/
│   ├── fitting_appointment/
│   └── garment_measurement/
├── public/
│   ├── css/
│   ├── js/  
│   └── build.json
├── workspace/
├── fixtures/
└── hooks.py
```

### Extending the App

1. **Custom Fields**: Add via ERPNext Customize Form
2. **Custom Scripts**: Modify JavaScript files in respective DocType folders
3. **Additional Workflows**: Create via Workflow DocType
4. **Custom Reports**: Use ERPNext Report Builder or custom queries

## Support

For support, feature requests, or contributions:
- GitHub Issues: [Brands Repository](https://github.com/siijjas/Brands/issues)
- ERPNext Community Forum
- Custom Development Services Available

## License

MIT License - See LICENSE file for details.

---

**Built for ERPNext v15** | **Tailor Management App v0.0.1**
