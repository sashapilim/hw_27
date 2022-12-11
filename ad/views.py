import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse

from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from .models import Categories, Ads


def index(request):
    return JsonResponse({'status': 'ok'}, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoriesView(View):

    def get(self, request):
        cat = Categories.objects.all()
        response = []
        for c in cat:
            response.append({
                "id": c.id,
                "name": c.name,
            })

        return JsonResponse(response, safe=False)

    def post(self, request):
        cat_data = json.loads(request.body)
        res = Categories(**cat_data)
        try:
            res.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        res.save()

        return JsonResponse({'name': res.name}, safe=False)


# id,name,author,price,description,address,is_published
@method_decorator(csrf_exempt, name='dispatch')
class AdsView(View):

    def get(self, request):
        ads = Ads.objects.all()
        response = []
        for a in ads:
            response.append({'id': a.id,
                             'name': a.name,
                             'author': a.author,
                             'price': a.price
                             })
        return JsonResponse(response, safe=False)

    def post(self, request):
        ad_data = json.loads(request.body)
        ad = Ads(**ad_data)

        try:
            ad.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)
        ad.save()
        return JsonResponse({'status': "save"})


class CategoryViewDetail(DetailView):
    model = Categories

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object = self.get_object()

        return JsonResponse({"name": self.object.name
                             }, safe=False)


class AdsViewDetail(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        super().get(self, request, *args, **kwargs)
        self.object = self.get_object()
        return JsonResponse({'id': self.object.id,
                             'name': self.object.name,
                             'author': self.object.author,
                             'price': self.object.price,
                             'description': self.object.description,
                             'is_published': self.object.is_published}, safe=False)
