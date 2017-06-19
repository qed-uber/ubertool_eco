"""
.. module:: agdrift_input
   :synopsis: A useful module indeed.
"""

from django.template.loader import render_to_string

from . import agdrift_parameters


def agdrift_input_page(request, model='', header='', form_data=None):
    html = render_to_string('04uberinput_jquery.html', {'model': model})
    html += render_to_string('04uberinput_start_drupal.html', {
        'MODEL': model,
        'TITLE': header})
    html += render_to_string('04uberinput_form.html', {
        'FORM': agdrift_parameters.AgdriftInp(form_data)})
    html += render_to_string('04uberinput_end_drupal.html', {})
    html += render_to_string('04ubertext_end_drupal.html', {})
    # Check if tooltips dictionary exists
    # try:
    #     import agdrift_tooltips
    #     hasattr(agdrift_tooltips, 'tooltips')
    #     tooltips = agdrift_tooltips.tooltips
    # except:
    #     tooltips = {}
    # html += render_to_string('05ubertext_tooltips_right.html', {'tooltips': tooltips})

    return html
