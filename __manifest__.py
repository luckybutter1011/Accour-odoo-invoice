{
    'name': 'Accour Report',
    'version': '1.0',
    'description': "Custom PDF Report",
    'depends': [
        'base',
        'website',
    ],
    'data':[
        "security/ir.model.access.csv",
        "report/custom_pdf_report.xml",
        "report/custom_pdf_template.xml",
        "views/accour_report_views.xml",
        "views/accour_menus.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}