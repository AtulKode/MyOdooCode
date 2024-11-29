{
	'name': 'pos customer note',
	
	'version': '16.0.0.0',
	'summary':'adding customer note button',
	'category':'point_of_sale',
	'depends':['base', 'point_of_sale','web'],
	'data':[
		"views/pos_config_views.xml",
		"views/pos_view_form.xml",
	],
	
	'installable':True,
	'auto_install': False,
	'application':True,

	'assets':{
		'point_of_sale.assets':[
		'pos_customer_note/static/src/js/models.js',
		'pos_customer_note/static/src/xml/customer_note_template.xml',
		'pos_customer_note/static/src/xml/pos_date_popup.xml',
		'pos_customer_note/static/src/xml/pos_date_template.xml',
		'pos_customer_note/static/src/js/pos_customer_note.js',
		'pos_customer_note/static/src/js/custom_date_popup.js',
		'pos_customer_note/static/src/js/pos_order_date.js',
		
		],

	},
	'license': 'LGPL-3',

}