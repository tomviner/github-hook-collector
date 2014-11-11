import json

from django.views.generic import View
from django.http import HttpResponse


class HookView(View):
    def post(self, request):
        return HttpResponse(json.dumps(request.POST))

    def get(self, request):
        headers = {k:v for (k,v) in request.META.items()
            if k.startswith('X')}
        return HttpResponse(json.dumps(headers))
