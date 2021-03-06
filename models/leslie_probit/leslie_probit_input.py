"""
.. module:: leslie_probit_input
   :synopsis: A useful module indeed.
"""

from django.template.loader import render_to_string


def leslie_probit_input_page(request, model='', header='', form_data=None):
    from . import leslie_probit_parameters

    html = render_to_string('04uberinput_jquery.html', {'model': model})
    html += render_to_string('04uberinput_start_tabbed_drupal.html', {
        'MODEL': model,
        'TITLE': header},
    	request=request)
    html += render_to_string('04uberinput_tabbed_nav.html', {
        'nav_dict': {
            'class_name': ['Chemical', 'DoseResponse', 'LeslieMatrix'],
            'tab_label': ['Chemical', 'DoseResponse', 'LeslieMatrix']
        }
    })
    html += """<br><table class="input_table tab tab_Chemical" border="0">"""
    html += str(leslie_probit_parameters.Leslie_probit_Chemical())
    html += """</table><table class="input_table tab tab_DoseResponse" border="0" style="display:none">"""
    html += str(leslie_probit_parameters.Leslie_probit_DoseResponse())
    html += """</table><table class="input_table tab tab_LeslieMatrix" border="0" style="display:none">"""
    html += str(leslie_probit_parameters.Leslie_probit_LeslieMatrix())

    html += """<table class="input_table tab tab_LeslieMatrix leslie" border="0" style="display:none">"""
    html += """<table class="input_table tab tab_LeslieMatrix no" border="0" style="display:none">"""
    html += render_to_string('leslie_probit_input_jquery.html', {})
    html += render_to_string('04uberinput_tabbed_end_drupal.html', {'sub_title': 'Submit'})
#    html += render_to_string('04uberinput_end_drupal.html', {})
    html += render_to_string('04ubertext_end_drupal.html', {})

    return html
