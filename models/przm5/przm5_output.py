# -*- coding: utf-8 -*-
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
import logging

@require_POST
def przm5OutputPage(request):
    import przm5_model
    args={}
    for key in request.POST:
        args[key] = request.POST.get(key)
    args["run_type"] = "single"
    logging.info(args)
    przm5_obj = przm5_model.przm5(args)
    return przm5_obj
