import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

from ad.models import Ads


class AdsView(ListView):
    model = Ads
    queryset = Ads.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.select_related('author').order_by(
            "-price")
        cat = request.GET.getlist('cat')
        if cat:
            self.object_list = self.object_list.filter(category__in=cat)
        text = request.GET.get('text')
        if text:
            self.object_list = self.object_list.filter(description__icontains=text)
        loc = request.GET.get('location')
        if loc:
            self.object_list = self.object_list.filter(author__location__name__icontains=loc)
        min = request.GET.get('price_from')
        max = request.GET.get('price_to')
        if min and max:
            self.object_list = self.object_list.filter(price__range=(min, max))
        paginator = Paginator(self.object_list, 10)
        num_pages = request.GET.get('page')
        pat_obj = paginator.get_page(num_pages)
        ads = []
        for ad in pat_obj:
            ads.append({"id": ad.id,
                        "name": ad.name,
                        "author_id": ad.author_id,
                        "author": ad.author.first_name,
                        "price": ad.price,
                        "description": ad.description,
                        "is_published": ad.is_published,
                        "category_id": ad.category_id,
                        "image": ad.image.url if ad.image else None})

        response = {
            'total': pat_obj.paginator.count,
            'num_pages': pat_obj.paginator.num_pages,
            'fields': ads
        }
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdsViewDetail(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        super().get(self, request, *args, **kwargs)
        self.object = self.get_object()
        return JsonResponse({'id': self.object.id,
                             'name': self.object.name,
                             'author': self.object.author.first_name,
                             'price': self.object.price,
                             'description': self.object.description,
                             'is_published': self.object.is_published}, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdUpadeteView(UpdateView):
    model = Ads
    fields = '__all__'

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ad_data = json.loads(request.body)
        if 'name' in ad_data:
            self.object.name = ad_data['name']
        if 'price' in ad_data:
            self.object.price = ad_data['price']
        if 'description' in ad_data:
            self.object.description = ad_data['description']

        self.object.save()
        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "author": self.object.author.first_name,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
            "image": self.object.image.url if self.object.image else None,
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdDeleteView(DeleteView):
    model = Ads
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({'status': 'ok'}, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdUploadImageView(UpdateView):
    model = Ads
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES.get("image", None)
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "author": self.object.author.first_name,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
            "image": self.object.image.url if self.object.image else None,
        })
