{
    'name': 'Travel',
    'description': 'Travel',
    'author': 'Team A1',
    'summary': "Manage travel vehicles, pool, and payment order",
    'depends': ['base', 'website', 'fleet', 'website_form','account'],
    'application': True,
    'data': ['views/odoo_page/travel_view.xml',
             'views/odoo_page/travel_menu.xml',
             'views/odoo_page/city_view.xml',
             'views/odoo_page/schedule_view.xml',
             'views/odoo_page/config_setting_travel.xml',
             'views/odoo_page/jalur_view.xml',
             'views/template/web_template.xml',
             'views/web_page/404.xml',
             'views/web_page/login.xml',
             'views/web_page/order.xml',
             'views/web_page/pool.xml',
             'views/web_page/schedule.xml',
             'views/web_page/schedule_item.xml',
             'views/web_page/order_success.xml',
             'views/web_page/cari_tiket.xml',
             'views/web_page/hasil_tiket.xml',
             'views/web_page/seat.xml',
             'views/web_page/ordertiket.xml',
             'security/ir.model.access.csv',
             'security/travel_access_rule.xml',
             'reports/travel_order_report.xml',
             'reports/travel_order_template.xml',
             'data/config_data.xml',
             'data/ir_sequence_data.xml',
             'demo/demo.xml',
             'views/web_page/web_menu.xml'],
}
