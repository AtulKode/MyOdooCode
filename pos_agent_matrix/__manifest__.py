{
	'name':"POS AGENT MATRIX",
	'version': '16.0.0.0',
	'category':'point_of_sale',
	'depends':['base', 'point_of_sale','web','product'],
	'data':[
		"security/ir.model.access.csv",
		"views/res_config_view.xml",
		"views/agent_views.xml",
		"views/pos_config_views.xml",
		"views/product_views.xml",
		"views/pos_order_line_views.xml",
	],

	'assets':{
		'point_of_sale.assets':[
		'pos_agent_matrix/static/src/js/productscreen.js',
		'pos_agent_matrix/static/src/xml/agent_popup_template.xml',
		'pos_agent_matrix/static/src/js/models.js',
		'pos_agent_matrix/static/src/js/product_agent_popup.js',
		
		
		],

	},
	
	'installable':True,
	'auto_install': False,
	'application':True,
	'license': 'LGPL-3',


}