import json

from django.views.generic import View
from django.http import HttpResponse

from .models import Call


class HookView(View):

    def post(self, request):
        headers = {k:v for (k,v) in request.META.items()
            if k.startswith('X')}
        data = self.request.POST
        Call.objects.create(headers=headers, data=data)
        return HttpResponse('', status=201)
