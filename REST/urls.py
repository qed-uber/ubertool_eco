from REST import rest_funcs
from django.conf.urls import url

urlpatterns = [
    url(r'ubertool/(?P<model>.*)/(?P<jid>.*)/?$', rest_funcs.rest_proxy),
    url(r'hwbi/locations/(?P<resource>.*)/?$', rest_funcs.rest_proxy_hwbi),
    url(r'hwbi/calc/run/?$', rest_funcs.rest_proxy_hwbi_calc),
    url(r'hwbi/calc/?$', rest_funcs.rest_proxy_hwbi_calc),
    url(r'^$', rest_funcs.self_documentation)
    # url(r'ubertool/(?P<model>.*?/?$)', rest_funcs.rest_proxy),
]
