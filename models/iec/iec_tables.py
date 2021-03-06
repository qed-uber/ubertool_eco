"""
.. module:: iec_tables
   :synopsis: A useful module indeed.
"""

import datetime
import logging

import numpy
# import django
from django.template import Context, Template

logger = logging.getLogger("IecTables")

def getheaderiv():
  headings = ["Parameter", "Value"]
  return headings

def getheaderov():
  headings = ["Parameter", "Value"]
  return headings

def getheaderovqaqc():
  headings = ["Parameter", "Value", "Expected Value"]
  return headings

def getheadersum():
    headings = ["Parameter", "Mean", "Std", "Min", "Max", "Unit"]
    return headings

def getheadersum_un():
    headings = ["Parameter", "Mean", "Std", "Min", "Max"]
    return headings

def gethtmlrowsfromcols(data, headings):
    columns = [data[heading] for heading in headings]

    # get the length of the longest column
    max_len = len(max(columns, key=len))

    for col in columns:
        # padding the short columns with None
        col += [None,] * (max_len - len(col))

    # Then rotate the structure...
    rows = [[col[i] for col in columns] for i in range(max_len)]
    return rows

def getdjtemplate():
    dj_template ="""
    <table class="out_" >
    {# headings #}
        <tr>
        {% for heading in headings %}
            <th>{{ heading }}</th>
        {% endfor %}
        </tr>
    {# data #}
    {% for row in data %}
    <tr>
        {% for val in row %}
        <td>{{ val|default:'' }}</td>
        {% endfor %}
    </tr>
    {% endfor %}
    </table>
    """
    return dj_template



def gett1data(iec_obj):
    data = { 
        "Parameter": ['lc50 or LD50', 'Threshold', 'Slope',],
        "Value": [iec_obj.lc50, iec_obj.threshold, iec_obj.dose_response,],
    }
    return data

def gettsumdata_1(lc50_pool, threshold_pool, dose_response_pool):
    data = { 
        "Parameter": ['lc50 or LD50', 'Threshold', 'Slope',],
        "Mean": ['{0:.2e}'.format(numpy.mean(lc50_pool)),'{0:.2e}'.format(numpy.mean(threshold_pool)),'{0:.2e}'.format(numpy.mean(dose_response_pool))],
        "Std": ['{0:.2e}'.format(numpy.std(lc50_pool)),'{0:.2e}'.format(numpy.std(threshold_pool)),'{0:.2e}'.format(numpy.std(dose_response_pool))],
        "Min": ['{0:.2e}'.format(numpy.min(lc50_pool)),'{0:.2e}'.format(numpy.min(threshold_pool)),'{0:.2e}'.format(numpy.min(dose_response_pool))],
        "Max": ['{0:.2e}'.format(numpy.max(lc50_pool)),'{0:.2e}'.format(numpy.max(threshold_pool)),'{0:.2e}'.format(numpy.max(dose_response_pool))],
    }
    return data

def gett2data(iec_obj):
    #logger.info(vars(iec_obj))
    data = { 
        "Parameter": ['Z Score', '"f8"', 'Chance of Individual Effect',],
        "Value": ['{0:.2f}'.format(iec_obj.out_z_score_f),'{0:.2e}'.format(iec_obj.out_f8_f),'{0:.2f}'.format(iec_obj.out_chance_f), ],
    }
    return data

def gettsumdata_2_un(z_score_f_pool, f8_f_pool, chance_f_pool):
    data = { 
        "Parameter": ['Z Score', '"f8"', 'Chance of Individual Effect',],
        "Mean": ['{0:.2e}'.format(numpy.mean(z_score_f_pool)),'{0:.2e}'.format(numpy.mean(f8_f_pool)),'{0:.2e}'.format(numpy.mean(chance_f_pool))],
        "Std": ['{0:.2e}'.format(numpy.std(z_score_f_pool)),'{0:.2e}'.format(numpy.std(f8_f_pool)),'{0:.2e}'.format(numpy.std(chance_f_pool))],
        "Min": ['{0:.2e}'.format(numpy.min(z_score_f_pool)),'{0:.2e}'.format(numpy.min(f8_f_pool)),'{0:.2e}'.format(numpy.min(chance_f_pool))],
        "Max": ['{0:.2e}'.format(numpy.max(z_score_f_pool)),'{0:.2e}'.format(numpy.max(f8_f_pool)),'{0:.2e}'.format(numpy.max(chance_f_pool))],
    }
    return data

def gett2dataqaqc(iec_obj):
    data = { 
        "Parameter": ['Z Score', '"f8"', 'Chance of Individual Effect',],
        "Value": ['{0:.2f}'.format(iec_obj.out_z_score_f),'{0:.2e}'.format(iec_obj.out_f8_f),'{0:.2f}'.format(iec_obj.out_chance_f), ],
        "Expected Value": ['{0:.2f}'.format(iec_obj.z_score_f_out_expected),'{0:.2e}'.format(iec_obj.f8_f_out_expected),'{0:.2f}'.format(iec_obj.chance_f_out_expected), ],
    }
    return data

# def gettsumdata(dose_response,lc50,threshold)
def gettsumdata(dose_response,lc50,threshold):
    data = { 
        "Parameter": ['Dose Response', 'lc50', 'Threshold'],
        "Mean": ['{0:.2e}'.format(numpy.mean(dose_response)), '{0:.2e}'.format(numpy.mean(lc50)),'{0:.2e}'.format(numpy.mean(threshold)),],
        "Std": ['{0:.2e}'.format(numpy.std(dose_response)),'{0:.2e}'.format(numpy.std(lc50)),'{0:.2e}'.format(numpy.std(threshold)),],
        "Min": ['{0:.2e}'.format(numpy.min(dose_response)),'{0:.2e}'.format(numpy.min(lc50)),'{0:.2e}'.format(numpy.min(threshold)),],
         "Max": ['{0:.2e}'.format(numpy.max(dose_response)),'{0:.2e}'.format(numpy.max(lc50)),'{0:.2e}'.format(numpy.max(threshold)),],
        "Unit": ['','mg/kg-bw', '',],
    }
    return data

# def gettsumdata_out(dose_response,lc50,threshold):
def gettsumdata_out(out_z_score_f, out_f8_f, out_chance_f):
    data = {
        "Parameter": ['Z Score F', 'f8', 'Chance F',],
        "Mean": ['{0:.2e}'.format(numpy.mean(out_z_score_f)),'{0:.2e}'.format(numpy.mean(out_f8_f)),'{0:.2e}'.format(numpy.mean(out_chance_f)),],
        "Std": ['{0:.2e}'.format(numpy.std(out_z_score_f)),'{0:.2e}'.format(numpy.std(out_f8_f)),'{0:.2e}'.format(numpy.std(out_chance_f)),],
        "Min": ['{0:.2e}'.format(numpy.min(out_z_score_f)),'{0:.2e}'.format(numpy.min(out_f8_f)),'{0:.2e}'.format(numpy.min(out_chance_f)),],
         "Max": ['{0:.2e}'.format(numpy.max(out_z_score_f)),'{0:.2e}'.format(numpy.max(out_f8_f)),'{0:.2e}'.format(numpy.max(out_chance_f)),],
        "Unit": ['','mg/kg-bw', '',],
    }
    return data

ivheadings = getheaderiv()
ovheadings = getheaderov()
ivheadings_un = getheadersum_un()
ovheadingsqaqc = getheaderovqaqc()
sumheadings = getheadersum()
djtemplate = getdjtemplate()
tmpl = Template(djtemplate)

def table_all(iec_obj):
    html_all = table_1(iec_obj)
    html_all = html_all + table_2(iec_obj)
    return html_all

def table_all_qaqc(iec_obj):
    html_all = table_1(iec_obj)
    html_all = html_all + table_2_qaqc(iec_obj)
    return html_all

def timestamp(iec_obj="", batch_jid=""):
    #ts = time.time()
    #st = datetime.datetime.fromtimestamp(ts).strftime('%A, %Y-%B-%d %H:%M:%S')
    if iec_obj:
        st = datetime.datetime.strptime(iec_obj.jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    else:
        st = datetime.datetime.strptime(batch_jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div class="out_">
    <b>IEC Version 1.0 (Beta)<br>
    """
    html = html + st
    html = html + " (EST)</b>"
    html = html + """
    </div>"""
    return html

# def timestamp():
#     ts = time.time()
#     st = datetime.datetime.fromtimestamp(ts).strftime('%A, %Y-%B-%d %H:%M:%S')
#     html="""
#     <div class="out_">
#         <b>IEC Version 1.0</a> (Beta)<br>
#     """
#     html = html + st
#     html = html + " (UTC)</b>"
#     html = html + """
#     </div>"""
#     return html

def table_all_un(lc50_pool, threshold_pool, dose_response_pool, z_score_f_pool, f8_f_pool, chance_f_pool):
    html_all = table_1_un(lc50_pool, f8_f_pool, dose_response_pool)
    html_all = html_all + table_2_un(z_score_f_pool, threshold_pool, chance_f_pool)
    return html_all

def table_1(iec_obj):
        html = """
        <H4 class="out_1 collapsible" id="section1"><span></span>User Inputs</H4>
            <div class="out_ container_output">
        """
        t1data = gett1data(iec_obj)
        t1rows = gethtmlrowsfromcols(t1data,ivheadings)
        html = html + tmpl.render(Context(dict(data=t1rows, headings=ivheadings)))
        html = html + """
            </div>
        """
        return html

def table_2(iec_obj):
        html = """
        <H4 class="out_2 collapsible" id="section2"><span></span>Model Output</H4>
            <div class="out_ container_output">
        """
        t2data = gett2data(iec_obj)
        t2rows = gethtmlrowsfromcols(t2data,ovheadings)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=ovheadings)))
        html = html + """
            </div>
        """
        return html

def table_2_qaqc(iec_obj):
        html = """
        <H4 class="out_2 collapsible" id="section2"><span></span>Model Output</H4>
            <div class="out_ container_output">
        """
        t2data = gett2dataqaqc(iec_obj)
        t2rows = gethtmlrowsfromcols(t2data,ovheadingsqaqc)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=ovheadingsqaqc)))
        html = html + """
            </div>
        """
        return html


def table_all_sum(dose_response,lc50,threshold,out_z_score_f, out_f8_f, out_chance_f):
    html_all_sum = table_sum_input(dose_response,lc50,threshold)
    html_all_sum += table_sum_output(out_z_score_f, out_f8_f, out_chance_f)
    return html_all_sum

def table_sum_input(dose_response,lc50,threshold):
        #pre-table sum_input
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>Summary Statistics</H3>
        <div class="out_">
            <H4 class="out_1 collapsible" id="section4"><span></span>Batch Inputs</H4>
                <div class="out_ container_output">
        """
        #table sum_input
        tsuminputdata = gettsumdata(dose_response,lc50,threshold)
        tsuminputrows = gethtmlrowsfromcols(tsuminputdata, sumheadings)
        html = html + tmpl.render(Context(dict(data=tsuminputrows, headings=sumheadings)))
        html = html + """
        </div>
        """
        return html

def table_sum_output(out_z_score_f, out_f8_f, out_chance_f):
        #pre-table sum_input
        html = """
            <H4 class="out_1 collapsible" id="section3"><span></span>IEC Outputs</H4>
                <div class="out_ container_output">
        """
        #table sum_input
        tsumoutputdata = gettsumdata_out(out_z_score_f, out_f8_f, out_chance_f)
        tsumoutputrows = gethtmlrowsfromcols(tsumoutputdata, sumheadings)
        html = html + tmpl.render(Context(dict(data=tsumoutputrows, headings=sumheadings)))
        html = html + """
                </div>
        </div>
        <br>"""
        return html
        
def table_1_un(lc50_pool, threshold_pool, dose_response_pool):
        html = """
        <H4 class="out_1 collapsible" id="section1"><span></span>User Inputs</H4>
            <div class="out_ container_output">
        """
        t1data_un = gettsumdata_1(lc50_pool, threshold_pool, dose_response_pool)
        t1rows_un = gethtmlrowsfromcols(t1data_un,ivheadings_un)
        html = html + tmpl.render(Context(dict(data=t1rows_un, headings=ivheadings_un)))
        html = html + """
            </div>
        """
        return html

def table_2_un(z_score_f_pool, f8_f_pool, chance_f_pool):
        html = """
        <H4 class="out_2 collapsible" id="section1"><span></span>Outputs</H4>
            <div class="out_ container_output">
        """
        t2data_un = gettsumdata_2_un(z_score_f_pool, f8_f_pool, chance_f_pool)
        t2rows_un = gethtmlrowsfromcols(t2data_un,ivheadings_un)
        html = html + tmpl.render(Context(dict(data=t2rows_un, headings=ivheadings_un)))
        html = html + """
            </div>
        """
        return html

