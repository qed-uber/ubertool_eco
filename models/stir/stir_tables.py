"""
.. module:: stir_tables
   :synopsis: A useful module indeed.
"""

import datetime
import logging

import numpy
# import django
from django.template import Context, Template

logger = logging.getLogger("StirTables")

def getheaderpvu():
	headings = ["Parameter", "Value", "Units"]
	return headings

def getheaderpvuqaqc():
    headings = ["Parameter", "Value", "Expected Value", "Units"]
    return headings

def getheaderpvr():
	headings = ["Parameter", "Value", "Results"]
	return headings

def getheaderpvrqaqc():
    headings = ["Parameter", "Value", "Expected Value", "Results", "Expected Results"]
    return headings

def getheadersum():
    headings = ["Parameter", "Mean", "Std", "Min", "Max", "Unit"]
    return headings

def getheadersum_5():
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
    <table class="out_">
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

def timestamp(stir_obj="", batch_jid=""):
    if stir_obj:
        st = datetime.datetime.strptime(stir_obj.jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    else:
        st = datetime.datetime.strptime(batch_jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div class="out_">
        <b>STIR <a href="http://www.epa.gov/oppefed1/models/terrestrial/stir/stir_user_guide.html">Version 1.0</a> (Beta)<br>
    """
    html = html + st
    html = html + " (EST)</b>"
    html = html + """
    </div>"""
    return html

def table_1(sm):
    #chemical_name, out_ar2, h, f_inhaled, ddsi, mw, vp
    #pre-table 1
    html = """
    <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs: Chemical</H3>        
    <div class="out_">
        <H4 class="out_1 collapsible" id="section2"><span></span>Table 1. Application and Chemical Information</H4>
            <div class="out_ container_output">
        """
    #table 1
    t1data = gett1data(sm)
    t1rows = gethtmlrowsfromcols(t1data,pvuheadings)
    html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
    html = html + """
            </div>
        """
    return html

def gett1data(sm):
    data = { 
        "Parameter": ['Chemical Name','Application Rate','Direct Spray Column Height',
            'Spray Fraction Inhaled','Direct Spray Inhalation Duration','Molecular Weight','Vapor Pressure',],
        "Value": [sm.chemical_name, sm.application_rate, sm.column_height, sm.spray_drift_fraction, sm.direct_spray_duration, 
            sm.molecular_weight, sm.vapor_pressure,],
        "Units": ['', 'lbs a.i./A', 'm','','minutes','g/mol','torr', ],
    }
    return data

def table_sum_1(i,application_rate,column_height,spray_drift_fraction,direct_spray_duration,molecular_weight,vapor_pressure):
        #pre-table sum_input_1
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>Batch Summary Statistics (Iterations={0!s})</H3>
        <div class="out_">
            <H4 class="out_1 collapsible" id="section4"><span></span>Chemical Properties</H4>
                <div class="out_ container_output">
        """.format((i-1))

        #table sum_input_1
        tsuminputdata_1 = gettsumdata_1(application_rate,column_height,spray_drift_fraction,direct_spray_duration,molecular_weight,vapor_pressure)
        tsuminputrows_1 = gethtmlrowsfromcols(tsuminputdata_1, sumheadings)
        html = html + tmpl.render(Context(dict(data=tsuminputrows_1, headings=sumheadings)))
        html = html + """
        </div>
        """
        return html

def gettsumdata_1(application_rate,column_height,spray_drift_fraction,direct_spray_duration,molecular_weight,vapor_pressure):

    data = { 
        "Parameter": ['Application Rate', 'Direct Spray Column Height', 'Spray Fraction Inhaled', 'Direct Spray Inhalation Duration', 
                      'Molecular Weight', 'Vapor Pressure', ],
        "Mean": ['{0:.2e}'.format(numpy.mean(application_rate)), '{0:.2e}'.format(numpy.mean(column_height)), '{0:.2e}'.format(numpy.mean(spray_drift_fraction)), '{0:.2e}'.format(numpy.mean(direct_spray_duration)), '{0:.2e}'.format(numpy.mean(molecular_weight)), '{0:.2e}'.format(numpy.mean(vapor_pressure)),],
        "Std":  ['{0:.2e}'.format(numpy.std(application_rate)), '{0:.2e}'.format(numpy.mean(column_height)), '{0:.2e}'.format(numpy.mean(spray_drift_fraction)), '{0:.2e}'.format(numpy.mean(direct_spray_duration)), '{0:.2e}'.format(numpy.std(molecular_weight)), '{0:.2e}'.format(numpy.std(vapor_pressure)),],
        "Min":  ['{0:.2e}'.format(numpy.min(application_rate)), '{0:.2e}'.format(numpy.mean(column_height)), '{0:.2e}'.format(numpy.mean(spray_drift_fraction)), '{0:.2e}'.format(numpy.mean(direct_spray_duration)), '{0:.2e}'.format(numpy.min(molecular_weight)), '{0:.2e}'.format(numpy.min(vapor_pressure)),],
        "Max":  ['{0:.2e}'.format(numpy.max(application_rate)), '{0:.2e}'.format(numpy.mean(column_height)), '{0:.2e}'.format(numpy.mean(spray_drift_fraction)), '{0:.2e}'.format(numpy.mean(direct_spray_duration)), '{0:.2e}'.format(numpy.max(molecular_weight)), '{0:.2e}'.format(numpy.max(vapor_pressure)),],
        "Unit": ['lbs a.i./A', 'm','','minutes','g/mol','torr',],
    }
    return data

def table_1qaqc(sm):
    #chemical_name, out_ar2, h, f_inhaled, ddsi, mw, vp
    #pre-table 1
    html = """
    <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs: Chemical</H3>
    <div class="out_">
        <H4 class="out_1 collapsible" id="section2"><span></span>Table 1. Application and Chemical Information</H4>
            <div class="out_ container_output">
        """
    #table 1
    t1data = gett1dataqaqc(sm)
    t1rows = gethtmlrowsfromcols(t1data,pvuheadings)
    html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
    html = html + """
            </div>
        """
    return html

def gett1dataqaqc(sm):
    data = { 
        "Parameter": ['Chemical Name','Application Rate','Direct Spray Column Height',
            'Spray Fraction Inhaled','Direct Spray Inhalation Duration','Molecular Weight','Vapor Pressure',],
        "Value": [sm.chemical_name, sm.application_rate, sm.column_height, sm.spray_drift_fraction, sm.direct_spray_duration, 
            sm.molecular_weight, sm.vapor_pressure,],
        "Units": ['', 'lbs a.i./A', 'm','','minutes','g/mol','torr', ],
    }
    return data

def table_2(sm):
    # #pre-table 2
    html = """
        <H4 class="out_2 collapsible" id="section3"><span></span>Toxicity Properties</H4>
            <div class="out_ container_output">
    """
    #table 2
    t2data = gett2data(sm)
    t2rows = gethtmlrowsfromcols(t2data,pvuheadings)
    html = html + tmpl.render(Context(dict(data=t2rows, headings=pvuheadings)))
    html = html + """
        </div>
    </div>
    """
    return html

def gett2data(sm):
    data = { 
        "Parameter": ['Avian Oral LD50','Assessed Bird Body Weight','Tested Bird Body Weight','Mineau Scaling Factor',
            'Mammalian Inhalation LC50','Rat Inhalation Study Duration','Assessed Mammal Body Weight','Tested Mammal Body Weight',
            'Mammal Oral LD50',],
        "Value": [sm.avian_oral_ld50, sm.body_weight_assessed_bird, sm.body_weight_tested_bird, sm.mineau_scaling_factor, 
            sm.mammal_inhalation_lc50, sm.duration_mammal_inhalation_study, sm.body_weight_assessed_mammal, sm.body_weight_tested_mammal,
            sm.mammal_oral_ld50,],
        "Units": ['mg/kg-bw','kg','kg','','mg/kg-bw','hours','kg','kg','mg/kg-bw',],
    }
    return data

def table_sum_2(avian_oral_ld50,body_weight_assessed_bird,body_weight_tested_bird,mineau_scaling_factor,mammal_inhalation_lc50,duration_mammal_inhalation_study,body_weight_assessed_mammal,body_weight_tested_mammal,mammal_oral_ld50):
    #pre-table sum_input_2
    html = """
        <H4 class="out_1 collapsible" id="section3"><span></span>Toxicity Properties</H4>
            <div class="out_ container_output">
    """

    #table sum_input_2
    tsuminputdata_2 = gettsumdata_2(avian_oral_ld50,body_weight_assessed_bird,body_weight_tested_bird,mineau_scaling_factor,mammal_inhalation_lc50,duration_mammal_inhalation_study,body_weight_assessed_mammal,body_weight_tested_mammal,mammal_oral_ld50)
    tsuminputrows_2 = gethtmlrowsfromcols(tsuminputdata_2, sumheadings)
    html = html + tmpl.render(Context(dict(data=tsuminputrows_2, headings=sumheadings)))
    html = html + """
            </div>
    </div>
    <br>
    """
    return html

def gettsumdata_2(avian_oral_ld50,body_weight_assessed_bird,body_weight_tested_bird,mineau_scaling_factor,mammal_inhalation_lc50,duration_mammal_inhalation_study,body_weight_assessed_mammal,body_weight_tested_mammal,mammal_oral_ld50):

    data = { 
        "Parameter": ['Avian Oral LD50','Assessed Bird Body Weight','Tested Bird Body Weight','Mineau Scaling Factor',
            'Mammalian Inhalation LC50','Rat Inhalation Study Duration','Assessed Mammal Body Weight','Tested Mammal Body Weight',
            'Mammal Oral LD50',],
        "Mean": ['{0:.2e}'.format(numpy.mean(avian_oral_ld50)), '{0:.2e}'.format(numpy.mean(body_weight_assessed_bird)), '{0:.2e}'.format(numpy.mean(body_weight_tested_bird)), '{0:.2e}'.format(numpy.mean(mineau_scaling_factor)), '{0:.2e}'.format(numpy.mean(mammal_inhalation_lc50)), '{0:.2e}'.format(numpy.mean(duration_mammal_inhalation_study)),'{0:.2e}'.format(numpy.mean(body_weight_assessed_mammal)), '{0:.2e}'.format(numpy.mean(body_weight_tested_mammal)), '{0:.2e}'.format(numpy.mean(mammal_oral_ld50)),],
        "Std":  ['{0:.2e}'.format(numpy.std(avian_oral_ld50)), '{0:.2e}'.format(numpy.mean(body_weight_assessed_bird)), '{0:.2e}'.format(numpy.mean(body_weight_tested_bird)), '{0:.2e}'.format(numpy.mean(mineau_scaling_factor)), '{0:.2e}'.format(numpy.std(mammal_inhalation_lc50)), '{0:.2e}'.format(numpy.std(duration_mammal_inhalation_study)),'{0:.2e}'.format(numpy.std(body_weight_assessed_mammal)), '{0:.2e}'.format(numpy.std(body_weight_tested_mammal)), '{0:.2e}'.format(numpy.std(mammal_oral_ld50)),],
        "Min":  ['{0:.2e}'.format(numpy.min(avian_oral_ld50)), '{0:.2e}'.format(numpy.mean(body_weight_assessed_bird)), '{0:.2e}'.format(numpy.mean(body_weight_tested_bird)), '{0:.2e}'.format(numpy.mean(mineau_scaling_factor)), '{0:.2e}'.format(numpy.min(mammal_inhalation_lc50)), '{0:.2e}'.format(numpy.min(duration_mammal_inhalation_study)),'{0:.2e}'.format(numpy.min(body_weight_assessed_mammal)), '{0:.2e}'.format(numpy.min(body_weight_tested_mammal)), '{0:.2e}'.format(numpy.min(mammal_oral_ld50)),],
        "Max":  ['{0:.2e}'.format(numpy.max(avian_oral_ld50)), '{0:.2e}'.format(numpy.mean(body_weight_assessed_bird)), '{0:.2e}'.format(numpy.mean(body_weight_tested_bird)), '{0:.2e}'.format(numpy.mean(mineau_scaling_factor)), '{0:.2e}'.format(numpy.max(mammal_inhalation_lc50)), '{0:.2e}'.format(numpy.max(duration_mammal_inhalation_study)),'{0:.2e}'.format(numpy.max(body_weight_assessed_mammal)), '{0:.2e}'.format(numpy.max(body_weight_tested_mammal)), '{0:.2e}'.format(numpy.max(mammal_oral_ld50)),],
        "Unit": ['mg/kg-bw','kg','kg','','mg/kg-bw','hours','kg','kg','mg/kg-bw',],
    }
    return data

def table_3(sm):
    # #pre-table 3
    html = """
    <br>
    <H3 class="out_3 collapsible" id="section4"><span></span>Calculated Estimates</H3>
    <div class="out_">
        <H4 class="out_3 collapsible" id="section5"><span></span>Table 3. Avian Calculated Outputs</H4>
            <div class="out_ container_output">
    """
    #table 3
    t3data = gett3data(sm)
    t3rows = gethtmlrowsfromcols(t3data,pvuheadings)
    html = html + tmpl.render(Context(dict(data=t3rows, headings=pvuheadings)))
    html = html + """
            </div>
    """
    return {'html':html, 'out_sat_air_conc':sm.out_sat_air_conc, 'out_inh_rate_avian':sm.out_inh_rate_avian, 'out_vid_avian':sm.out_vid_avian,
            'out_estimated_avian_inhalation_ld50':sm.out_estimated_avian_inhalation_ld50, 'out_adjusted_avian_inhalation_ld50':sm.out_adjusted_avian_inhalation_ld50, 'out_ratio_vid_avian':sm.out_ratio_vid_avian,
            'out_sid_avian':sm.out_sid_avian, 'out_ratio_sid_avian':sm.out_ratio_sid_avian}

def gett3data(sm):
    data = { 
        "Parameter": ['Saturated Air Concentration of Pesticide','Avian Inhalation Rate','Maximum 1-hour Avian Vapor Inhalation Dose',
          'Estimated Avian Inhalation LD50','Adjusted Avian Inhalation LD50','Ratio of Vapor Dose to Adjusted Inhalation LD50',
          'Spray Droplet Inhalation Dose of Assessed Bird','Ratio of Droplet Inhalation Dose to Adjusted Inhalation LD50',],
        #"Value": [cs,ir_avian,out_vid_avian,ld50est,ld50adj,ratio_vd_avian,out_sid_avian,out_ratio_sid_avian,],
        "Value": ['{0:.2e}'.format(sm.out_sat_air_conc),'{0:.2e}'.format(sm.out_inh_rate_avian),'{0:.2e}'.format(sm.out_vid_avian),
            '{0:.2e}'.format(sm.out_estimated_avian_inhalation_ld50),'{0:.2e}'.format(sm.out_adjusted_avian_inhalation_ld50),'{0:.2e}'.format(sm.out_ratio_vid_avian),
            '{0:.2e}'.format(sm.out_sid_avian),'{0:.2e}'.format(sm.out_ratio_sid_avian),],
        "Units": ['mg/m3','cm3/hr','mg/kg-bw','mg/kg-bw','mg/kg-bw','unitless','mg/kg-bw','unitless',],
    }
    return data

def table_sum_3(out_sat_air_conc,out_inh_rate_avian,out_vid_avian,out_estimated_avian_inhalation_ld50,out_adjusted_avian_inhalation_ld50,out_ratio_vid_avian,out_sid_avian,out_ratio_sid_avian):
    #pre-table sum_3
    html = """
    <H3 class="out_3 collapsible" id="section4"><span></span>Calculated Estimates</H3>
    <div class="out_">
        <H4 class="out_1 collapsible" id="section3"><span></span>Avian Calculated Outputs</H4>
            <div class="out_ container_output">
    """

    #table sum_output_3
    tsuminputdata_3 = gettsumdata_3(out_sat_air_conc,out_inh_rate_avian,out_vid_avian,out_estimated_avian_inhalation_ld50,out_adjusted_avian_inhalation_ld50,out_ratio_vid_avian,out_sid_avian,out_ratio_sid_avian)
    tsuminputrows_3 = gethtmlrowsfromcols(tsuminputdata_3,sumheadings)       
    html = html + tmpl.render(Context(dict(data=tsuminputrows_3, headings=sumheadings)))
    html = html + """
            </div>
    """
    return html

def gettsumdata_3(out_sat_air_conc,out_inh_rate_avian,out_vid_avian,out_estimated_avian_inhalation_ld50,out_adjusted_avian_inhalation_ld50,out_ratio_vid_avian,out_sid_avian,out_ratio_sid_avian):

    data = { 
        "Parameter": ['Saturated Air Concentration of Pesticide','Avian Inhalation Rate','Maximum 1-hour Avian Vapor Inhalation Dose',
          'Estimated Avian Inhalation LD50','Adjusted Avian Inhalation LD50','Ratio of Vapor Dose to Adjusted Inhalation LD50',
          'Spray Droplet Inhalation Dose of Assessed Bird','Ratio of Droplet Inhalation Dose to Adjusted Inhalation LD50',],
        "Mean": ['{0:.2e}'.format(numpy.mean(out_sat_air_conc)), '{0:.2e}'.format(numpy.mean(out_inh_rate_avian)), '{0:.2e}'.format(numpy.mean(out_vid_avian)), '{0:.2e}'.format(numpy.mean(out_estimated_avian_inhalation_ld50)), '{0:.2e}'.format(numpy.mean(out_adjusted_avian_inhalation_ld50)), '{0:.2e}'.format(numpy.mean(out_ratio_vid_avian)),'{0:.2e}'.format(numpy.mean(out_sid_avian)), '{0:.2e}'.format(numpy.mean(out_ratio_sid_avian)),],
        "Std":  ['{0:.2e}'.format(numpy.std(out_sat_air_conc)), '{0:.2e}'.format(numpy.mean(out_inh_rate_avian)), '{0:.2e}'.format(numpy.mean(out_vid_avian)), '{0:.2e}'.format(numpy.mean(out_estimated_avian_inhalation_ld50)), '{0:.2e}'.format(numpy.std(out_adjusted_avian_inhalation_ld50)), '{0:.2e}'.format(numpy.std(out_ratio_vid_avian)),'{0:.2e}'.format(numpy.std(out_sid_avian)), '{0:.2e}'.format(numpy.std(out_ratio_sid_avian)),],
        "Min":  ['{0:.2e}'.format(numpy.min(out_sat_air_conc)), '{0:.2e}'.format(numpy.mean(out_inh_rate_avian)), '{0:.2e}'.format(numpy.mean(out_vid_avian)), '{0:.2e}'.format(numpy.mean(out_estimated_avian_inhalation_ld50)), '{0:.2e}'.format(numpy.min(out_adjusted_avian_inhalation_ld50)), '{0:.2e}'.format(numpy.min(out_ratio_vid_avian)),'{0:.2e}'.format(numpy.min(out_sid_avian)), '{0:.2e}'.format(numpy.min(out_ratio_sid_avian)),],
        "Max":  ['{0:.2e}'.format(numpy.max(out_sat_air_conc)), '{0:.2e}'.format(numpy.mean(out_inh_rate_avian)), '{0:.2e}'.format(numpy.mean(out_vid_avian)), '{0:.2e}'.format(numpy.mean(out_estimated_avian_inhalation_ld50)), '{0:.2e}'.format(numpy.max(out_adjusted_avian_inhalation_ld50)), '{0:.2e}'.format(numpy.max(out_ratio_vid_avian)),'{0:.2e}'.format(numpy.max(out_sid_avian)), '{0:.2e}'.format(numpy.max(out_ratio_sid_avian)),],
        "Unit": ['mg/m3','cm3/hr','mg/kg-bw','mg/kg-bw','mg/kg-bw','unitless','mg/kg-bw','unitless',],
    }
    return data

def table_3qaqc(sm):
    # #pre-table 3
    html = """
    <br>
        <H3 class="out_3 collapsible" id="section4"><span></span>Calculated Estimates</H3>
        <div class="out_">
            <H4 class="out_3 collapsible" id="section5"><span></span>Table 3. Avian Calculated Outputs</H4>
                <div class="out_ container_output">
    """
    #table 3
    t3data = gett3dataqaqc(sm)
    t3rows = gethtmlrowsfromcols(t3data,pvuheadingsqaqc)
    html = html + tmpl.render(Context(dict(data=t3rows, headings=pvuheadingsqaqc)))
    html = html + """
        </div>
        """
    return html

def gett3dataqaqc(sm):
    data = { 
        "Parameter": ['Saturated Air Concentration of Pesticide','Avian Inhalation Rate','Maximum 1-hour Avian Vapor Inhalation Dose',
          'Estimated Avian Inhalation LD50','Adjusted Avian Inhalation LD50','Ratio of Vapor Dose to Adjusted Inhalation LD50',
          'Spray Droplet Inhalation Dose of Assessed Bird','Ratio of Droplet Inhalation Dose to Adjusted Inhalation LD50',],
        #"Value": [cs,ir_avian,out_vid_avian,ld50est,ld50adj,ratio_vd_avian,out_sid_avian,out_ratio_sid_avian,],
        "Value": ['{0:.2e}'.format(sm.out_sat_air_conc),'{0:.2e}'.format(sm.out_inh_rate_avian),'{0:.2e}'.format(sm.out_vid_avian),
            '{0:.2e}'.format(sm.out_estimated_avian_inhalation_ld50),'{0:.2e}'.format(sm.out_adjusted_avian_inhalation_ld50),'{0:.2e}'.format(sm.out_ratio_vid_avian),
            '{0:.2e}'.format(sm.out_sid_avian),'{0:.2e}'.format(sm.out_ratio_sid_avian),],
        "Expected Value": ['{0:.2e}'.format(sm.exp_out_sat_air_conc),'{0:.2e}'.format(sm.exp_out_inh_rate_avian),'{0:.2e}'.format(sm.exp_out_vid_avian),
            '{0:.2e}'.format(sm.exp_out_estimated_avian_inhalation_ld50),'{0:.2e}'.format(sm.exp_out_adjusted_avian_inhalation_ld50),'{0:.2e}'.format(sm.exp_out_ratio_vid_avian),
            '{0:.2e}'.format(sm.exp_out_sid_avian),'{0:.2e}'.format(sm.exp_out_ratio_sid_avian),],
        "Units": ['mg/m3','cm3/hr','mg/kg-bw','mg/kg-bw','mg/kg-bw','unitless','mg/kg-bw','unitless',],
    }
    return data

def table_4(sm):
    # #pre-table 3
    html = """
        <H4 class="out_4 collapsible" id="section6"><span></span>Table 4. Mammal Calculated Outputs</H4>
            <div class="out_ container_output">
    """
    #table 3
    t4data = gett4data(sm)
    t4rows = gethtmlrowsfromcols(t4data,pvuheadings)
    html = html + tmpl.render(Context(dict(data=t4rows, headings=pvuheadings)))
    html = html + """
        </div>
        """
    return {'html':html, 'out_sat_air_conc':sm.out_sat_air_conc, 'out_inh_rate_mammal':sm.out_inh_rate_mammal, 'out_vid_mammal':sm.out_vid_mammal,
            'out_mammal_inhalation_ld50':sm.out_mammal_inhalation_ld50, 'out_out_adjusted_mammal_inhalation_ld50':sm.out_adjusted_mammal_inhalation_ld50, 'out_ratio_vid_mammal':sm.out_ratio_vid_mammal,
            'out_sid_mammal':sm.out_sid_mammal, 'out_ratio_sid_mammal':sm.out_ratio_sid_mammal}

def gett4data(sm):
    data = { 
        "Parameter": ['Saturated Air Concentration of Pesticide','Mammal Inhalation Rate','Maximum 1-hour Mammal Vapor Inhalation Dose',
          'Mammal Inhalation LD50','Adjusted Mammal Inhalation LD50','Ratio of Vapor Dose to Adjusted Inhalation LD50',
          'Spray Droplet Inhalation Dose of Assessed Mammal','Ratio of Droplet Inhalation Dose to Adjusted Inhalation LD50',],
        "Value": ['{0:.2e}'.format(sm.out_sat_air_conc),'{0:.2e}'.format(sm.out_inh_rate_mammal),'{0:.2e}'.format(sm.out_vid_mammal),
            '{0:.2e}'.format(sm.out_mammal_inhalation_ld50),'{0:.2e}'.format(sm.out_adjusted_mammal_inhalation_ld50),'{0:.2e}'.format(sm.out_ratio_vid_mammal),
            '{0:.2e}'.format(sm.out_sid_mammal),'{0:.2e}'.format(sm.out_ratio_sid_mammal),],
        "Units": ['mg/m3','cm3/hr','mg/kg-bw','mg/kg-bw','mg/kg-bw','unitless','mg/kg-bw','unitless',],
    }
    return data

def table_sum_4(out_sat_air_conc,out_inh_rate_mammal,out_vid_mammal,out_mammal_inhalation_ld50,out_adjusted_mammal_inhalation_ld50,out_ratio_vid_mammal,out_sid_mammal,out_ratio_sid_mammal):
    #pre-table sum_4
    html = """
        <H4 class="out_4 collapsible" id="section6"><span></span>Table 4. Mammal Calculated Outputs</H4>
            <div class="out_ container_output">
    """

    #table sum_output_4
    tsuminputdata_4 = gettsumdata_4(out_sat_air_conc,out_inh_rate_mammal,out_vid_mammal,out_mammal_inhalation_ld50,out_adjusted_mammal_inhalation_ld50,out_ratio_vid_mammal,out_sid_mammal,out_ratio_sid_mammal)
    tsuminputrows_4 = gethtmlrowsfromcols(tsuminputdata_4,sumheadings)       
    html = html + tmpl.render(Context(dict(data=tsuminputrows_4, headings=sumheadings)))
    html = html + """
    </div>
    """
    return html

def gettsumdata_4(out_sat_air_conc,out_inh_rate_mammal,out_vid_mammal,out_mammal_inhalation_ld50,out_adjusted_mammal_inhalation_ld50,out_ratio_vid_mammal,out_sid_mammal,out_ratio_sid_mammal):

    data = { 
        "Parameter": ['Saturated Air Concentration of Pesticide','Mammal Inhalation Rate','Maximum 1-hour Mammal Vapor Inhalation Dose',
          'Mammal Inhalation LD50','Adjusted Mammal Inhalation LD50','Ratio of Vapor Dose to Adjusted Inhalation LD50',
          'Spray Droplet Inhalation Dose of Assessed Mammal','Ratio of Droplet Inhalation Dose to Adjusted Inhalation LD50'],
        "Mean": ['{0:.2e}'.format(numpy.mean(out_sat_air_conc)), '{0:.2e}'.format(numpy.mean(out_inh_rate_mammal)), '{0:.2e}'.format(numpy.mean(out_vid_mammal)), '{0:.2e}'.format(numpy.mean(out_mammal_inhalation_ld50)), '{0:.2e}'.format(numpy.mean(out_adjusted_mammal_inhalation_ld50)), '{0:.2e}'.format(numpy.mean(out_ratio_vid_mammal)),'{0:.2e}'.format(numpy.mean(out_sid_mammal)), '{0:.2e}'.format(numpy.mean(out_ratio_sid_mammal)),],
        "Std":  ['{0:.2e}'.format(numpy.std(out_sat_air_conc)), '{0:.2e}'.format(numpy.mean(out_inh_rate_mammal)), '{0:.2e}'.format(numpy.mean(out_vid_mammal)), '{0:.2e}'.format(numpy.mean(out_mammal_inhalation_ld50)), '{0:.2e}'.format(numpy.std(out_adjusted_mammal_inhalation_ld50)), '{0:.2e}'.format(numpy.std(out_ratio_vid_mammal)),'{0:.2e}'.format(numpy.std(out_sid_mammal)), '{0:.2e}'.format(numpy.std(out_ratio_sid_mammal)),],
        "Min":  ['{0:.2e}'.format(numpy.min(out_sat_air_conc)), '{0:.2e}'.format(numpy.mean(out_inh_rate_mammal)), '{0:.2e}'.format(numpy.mean(out_vid_mammal)), '{0:.2e}'.format(numpy.mean(out_mammal_inhalation_ld50)), '{0:.2e}'.format(numpy.min(out_adjusted_mammal_inhalation_ld50)), '{0:.2e}'.format(numpy.min(out_ratio_vid_mammal)),'{0:.2e}'.format(numpy.min(out_sid_mammal)), '{0:.2e}'.format(numpy.min(out_ratio_sid_mammal)),],
        "Max":  ['{0:.2e}'.format(numpy.max(out_sat_air_conc)), '{0:.2e}'.format(numpy.mean(out_inh_rate_mammal)), '{0:.2e}'.format(numpy.mean(out_vid_mammal)), '{0:.2e}'.format(numpy.mean(out_mammal_inhalation_ld50)), '{0:.2e}'.format(numpy.max(out_adjusted_mammal_inhalation_ld50)), '{0:.2e}'.format(numpy.max(out_ratio_vid_mammal)),'{0:.2e}'.format(numpy.max(out_sid_mammal)), '{0:.2e}'.format(numpy.max(out_ratio_sid_mammal)),],
        "Unit": ['mg/m3','cm3/hr','mg/kg-bw','mg/kg-bw','mg/kg-bw','unitless','mg/kg-bw','unitless',],
    }
    return data

def table_4qaqc(sm):
    # #pre-table 3
    html = """
        <H4 class="out_4 collapsible" id="section6"><span></span>Table 4. Mammal Calculated Outputs</H4>
            <div class="out_ container_output">
    """
    #table 3
    t4data = gett4dataqaqc(sm)
    t4rows = gethtmlrowsfromcols(t4data,pvuheadingsqaqc)
    html = html + tmpl.render(Context(dict(data=t4rows, headings=pvuheadingsqaqc)))
    html = html + """
        </div>
        """
    return html

def gett4dataqaqc(sm):
    data = { 
        "Parameter": ['Saturated Air Concentration of Pesticide','Mammal Inhalation Rate','Maximum 1-hour Mammal Vapor Inhalation Dose',
          'Mammal Inhalation LD50','Adjusted Mammal Inhalation LD50','Ratio of Vapor Dose to Adjusted Inhalation LD50',
          'Spray Droplet Inhalation Dose of Assessed Mammal','Ratio of Droplet Inhalation Dose to Adjusted Inhalation LD50',],
        "Value": ['{0:.2e}'.format(sm.out_sat_air_conc),'{0:.2e}'.format(sm.out_inh_rate_mammal),'{0:.2e}'.format(sm.out_vid_mammal),
            '{0:.2e}'.format(sm.out_mammal_inhalation_ld50),'{0:.2e}'.format(sm.out_adjusted_mammal_inhalation_ld50),'{0:.2e}'.format(sm.out_ratio_vid_mammal),
            '{0:.2e}'.format(sm.out_sid_mammal),'{0:.2e}'.format(sm.out_ratio_sid_mammal),],
        "Expected Value": ['{0:.2e}'.format(sm.exp_out_sat_air_conc),'{0:.2e}'.format(sm.exp_out_inh_rate_mammal),'{0:.2e}'.format(sm.exp_out_vid_mammal),
            '{0:.2e}'.format(sm.exp_out_mammal_inhalation_ld50),'{0:.2e}'.format(sm.exp_out_adjusted_mammal_inhalation_ld50),'{0:.2e}'.format(sm.exp_out_ratio_vid_mammal),
            '{0:.2e}'.format(sm.exp_sid_mammal),'{0:.2e}'.format(sm.exp_ratio_sid_mammal),],
        "Units": ['mg/m3','cm3/hr','mg/kg-bw','mg/kg-bw','mg/kg-bw','unitless','mg/kg-bw','unitless',],
    }
    return data

def table_5(sm):
    # #pre-table 5
    html = """
            <H4 class="out_5 collapsible" id="section5"><span></span>Table 5. Inference</H4>
                <div class="out_ container_output">
    """
    #table 3
    t5data = gett5data(sm)
    t5rows = gethtmlrowsfromcols(t5data,pvrheadings)
    html = html + tmpl.render(Context(dict(data=t5rows, headings=pvrheadings)))
    html = html + """
        </div>
    </div>
    """
    return {'html':html, 'out_ratio_vid_avian':sm.out_ratio_vid_avian, 'out_ratio_sid_avian':sm.out_ratio_sid_avian, 'out_ratio_vid_mammal':sm.out_ratio_vid_mammal,
            'out_ratio_sid_mammal':sm.out_ratio_sid_mammal}

def gett5data(sm):
    data = { 
        "Parameter": ['Avian: Ratio of Vapor Dose to Adjusted Inhalation LD50','Avian: Ratio of Droplet Dose to Adjusted Inhalation LD50',
          'Mammal: Ratio of Vapor Dose to Adjusted Inhalation LD50','Mammal: Ratio of Droplet Dose to Adjusted Inhalation LD50',],
        "Value": ['{0:.2e}'.format(sm.out_ratio_vid_avian),'{0:.2e}'.format(sm.out_ratio_sid_avian),'{0:.2e}'.format(sm.out_ratio_vid_mammal),'{0:.2e}'.format(sm.out_ratio_sid_mammal),],
        "Results": [sm.out_loc_vid_avian,sm.out_loc_sid_avian,sm.out_loc_vid_mammal,sm.out_loc_sid_mammal,],
    }
    return data

def table_sum_5(out_ratio_vid_avian, out_ratio_sid_avian, out_ratio_vid_mammal, out_ratio_sid_mammal):
    #pre-table sum_5
    html = """
        <H4 class="out_5 collapsible" id="section5"><span></span>Table 5. Inference</H4>
            <div class="out_ container_output">
    """

    #table sum_output_5
    tsuminputdata_5 = gettsumdata_5(out_ratio_vid_avian, out_ratio_sid_avian, out_ratio_vid_mammal, out_ratio_sid_mammal)
    tsuminputrows_5 = gethtmlrowsfromcols(tsuminputdata_5,sumheadings_5)       
    html = html + tmpl.render(Context(dict(data=tsuminputrows_5, headings=sumheadings_5)))
    html = html + """
        </div>
    </div>
    """
    return html

def gettsumdata_5(out_ratio_vid_avian, out_ratio_sid_avian, out_ratio_vid_mammal, out_ratio_sid_mammal):

    data = { 
        "Parameter": ['Avian: Ratio of Vapor Dose to Adjusted Inhalation LD50','Avian: Ratio of Droplet Dose to Adjusted Inhalation LD50',
          'Mammal: Ratio of Vapor Dose to Adjusted Inhalation LD50','Mammal: Ratio of Droplet Dose to Adjusted Inhalation LD50'],
        "Mean": ['{0:.2e}'.format(numpy.mean(out_ratio_vid_avian)), '{0:.2e}'.format(numpy.mean(out_ratio_sid_avian)), '{0:.2e}'.format(numpy.mean(out_ratio_vid_mammal)), '{0:.2e}'.format(numpy.mean(out_ratio_sid_mammal)),],
        "Std":  ['{0:.2e}'.format(numpy.std(out_ratio_vid_avian)), '{0:.2e}'.format(numpy.mean(out_ratio_sid_avian)), '{0:.2e}'.format(numpy.mean(out_ratio_vid_mammal)), '{0:.2e}'.format(numpy.mean(out_ratio_sid_mammal)),],
        "Min":  ['{0:.2e}'.format(numpy.min(out_ratio_vid_avian)), '{0:.2e}'.format(numpy.mean(out_ratio_sid_avian)), '{0:.2e}'.format(numpy.mean(out_ratio_vid_mammal)), '{0:.2e}'.format(numpy.mean(out_ratio_sid_mammal)),],
        "Max":  ['{0:.2e}'.format(numpy.max(out_ratio_vid_avian)), '{0:.2e}'.format(numpy.mean(out_ratio_sid_avian)), '{0:.2e}'.format(numpy.mean(out_ratio_vid_mammal)), '{0:.2e}'.format(numpy.mean(out_ratio_sid_mammal)),],
    }
    return data

def table_5qaqc(sm):
    # #pre-table 5
    html = """
            <H4 class="out_5 collapsible" id="section5"><span></span>Table 5. Inference</H4>
                <div class="out_ container_output">
    """
    #table 3
    t5data = gett5dataqaqc(sm)
    t5rows = gethtmlrowsfromcols(t5data,pvrheadingsqaqc)
    html = html + tmpl.render(Context(dict(data=t5rows, headings=pvrheadingsqaqc)))
    html = html + """
        </div>
    </div>
    """
    return html

def gett5dataqaqc(sm):
    data = { 
        "Parameter": ['Avian: Ratio of Vapor Dose to Adjusted Inhalation LD50','Avian: Ratio of Droplet Dose to Adjusted Inhalation LD50',
          'Mammal: Ratio of Vapor Dose to Adjusted Inhalation LD50','Mammal: Ratio of Droplet Dose to Adjusted Inhalation LD50',],
        "Value": ['{0:.2e}'.format(sm.out_ratio_vid_avian),'{0:.2e}'.format(sm.out_ratio_sid_avian),'{0:.2e}'.format(sm.out_ratio_vid_mammal),'{0:.2e}'.format(sm.out_ratio_sid_mammal),],
        "Expected Value": ['{0:.2e}'.format(sm.exp_out_ratio_vid_avian),'{0:.2e}'.format(sm.exp_out_ratio_sid_avian),'{0:.2e}'.format(sm.exp_out_ratio_vid_mammal),'{0:.2e}'.format(sm.exp_ratio_sid_mammal),],
        "Results": [sm.out_loc_vid_avian,sm.out_loc_sid_avian,sm.out_loc_vid_mammal,sm.out_loc_sid_mammal,],
        "Expected Results": [sm.exp_loc_out_vid_avian,sm.exp_loc_out_sid_avian,sm.exp_loc_out_vid_mammal,sm.exp_loc_sid_mammal,],
    }
    return data

pvuheadings = getheaderpvu()
pvrheadings = getheaderpvr()
pvuheadingsqaqc = getheaderpvuqaqc()
pvrheadingsqaqc = getheaderpvrqaqc()
sumheadings = getheadersum()
sumheadings_5 = getheadersum_5()
djtemplate = getdjtemplate()
tmpl = Template(djtemplate)




def table_all(sm):
    html = table_1(sm)
    html = html + table_2(sm)
    html = html + table_3(sm)['html']
    html = html + table_4(sm)['html']
    html = html + table_5(sm)['html']
    return html


def table_all_batch(sm):
    html = table_1(sm)
    html = html + table_2(sm)
    html = html + table_3(sm)['html']
    html = html + table_4(sm)['html']
    html = html + table_5(sm)['html']
    return html

def table_all_qaqc(sm):
    html = table_1qaqc(sm)
    html = html + table_2(sm)
    html = html + table_3qaqc(sm)
    html = html + table_4qaqc(sm)
    html = html + table_5qaqc(sm)
    return html