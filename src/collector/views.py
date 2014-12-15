from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt

from .models import Call


class HookView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(HookView, self).dispatch(*args, **kwargs)

    def post(self, request):
        headers = {
            k: v for (k, v) in request.META.items()
            if k.startswith('X')}
        data = self.request.POST
        Call.objects.create(headers=headers, data=data)
        return HttpResponse('', status=201)
