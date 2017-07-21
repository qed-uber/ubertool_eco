"""
.. module:: pat_input
   :synopsis: A useful module indeed.
"""

from django.template.loader import render_to_string


def pat_input_page(request, model='', header='', form_data=None):
    from . import pat_parameters

    html = render_to_string('04uberinput_start_drupal.html', {
        'MODEL': model,
        'TITLE': header})
    html += render_to_string('04uberinput_form.html', {
        'FORM': pat_parameters.PatInp(form_data)})
    html += render_to_string('04uberinput_end_drupal.html', {})
    html += render_to_string('04ubertext_end_drupal.html', {})
    # Check if tooltips dictionary exists
    # try:
    #     import pat_tooltips
    #     hasattr(pat_tooltips, 'tooltips')
    #     tooltips = pat_tooltips.tooltips
    # except:
    #     tooltips = {}
    # html += render_to_string('05ubertext_tooltips_right.html', {'tooltips': tooltips})

    return html
