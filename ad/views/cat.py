import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

from ad.models import Categories


class CategoriesView(ListView):
    model = Categories
    queryset = Categories.objects.all().order_by('name')

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        paginator = Paginator(self.object_list, 10)
        num_pages = request.GET.get('page')
        pat_obj = paginator.get_page(num_pages)
        cities = []
        for i in pat_obj:
            cities.append({
                "id": i.id,
                "name": i.name,

            })

        response = {
            'total': paginator.count,
            'num_pages': paginator.num_pages,
            'fields': cities
        }
        return JsonResponse(response, safe=False)


class CategoryViewDetail(DetailView):
    model = Categories

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object = self.get_object()

        return JsonResponse({"name": self.object.name
                             }, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpadeteView(UpdateView):
    model = Categories
    fields = '__all__'

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        cat_data = json.loads(request.body)
        self.object.name = cat_data['name']
        self.object.save()

        return JsonResponse({'id': self.object.id,
                             'name': self.object.name})


@method_decorator(csrf_exempt, name="dispatch")
class CategoryDeleteView(DeleteView):
    model = Categories
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({'status': 'ok'}, safe=False)
