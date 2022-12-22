import json

from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from users.models import User, Location


class UserView(ListView):
    model = User
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list. \
            prefetch_related('location'). \
            filter(ads__is_published=True). \
            annotate(total_ads=Count('ads'))
        paginator = Paginator(self.object_list, 10)
        num_pages = request.GET.get('page')
        pat_obj = paginator.get_page(num_pages)
        us = []
        for i in pat_obj:
            us.append({

                "id": i.id,
                "username": i.username,
                "first_name": i.first_name,
                "last_name": i.last_name,
                "role": i.role,
                "age": i.age,
                'total_ads': i.total_ads,
                "locations": list(map(str, i.location.all())),
            })

        response = {
            'total': paginator.count,
            'num_pages': paginator.num_pages,
            'fields': us
        }
        return JsonResponse(response, safe=False)


class UserDetail(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object = self.get_object()

        return JsonResponse({"id": self.object.id,
                             "username": self.object.username,
                             "first_name": self.object.first_name,
                             "last_name": self.object.last_name,
                             "role": self.object.role,
                             "age": self.object.age,
                             "locations": list(map(str, self.object.location.all()))
                             }, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class UserCreateView(CreateView):
    model = User
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        new_user = User.objects.create(
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            username=user_data.get('username'),
            password=user_data.get('password'),
            age=user_data.get('age'),
            role=user_data.get('role')

        )

        for loc in user_data.get('location'):
            locations, _ = Location.objects.get_or_create(name=loc)
            new_user.location.add(locations)

        return JsonResponse({"id": new_user.id,
                             "username": new_user.username,
                             "first_name": new_user.first_name,
                             "last_name": new_user.last_name,
                             "role": new_user.role,
                             "age": new_user.age,
                             "locations": list(map(str, new_user.location.all()))
                             }, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(UpdateView):
    model = User
    fields = '__all__'

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        user_data = json.loads(request.body)

        self.object.username = user_data["username"]
        self.object.password = user_data["password"]
        self.object.first_name = user_data["first_name"]
        self.object.last_name = user_data["last_name"]
        self.object.age = user_data["age"]

        for loc in user_data['location']:
            locations, _ = Location.objects.get_or_create(name=loc)
            self.object.location.add(locations)
        self.object.save()
        return JsonResponse({"id": self.object.id,
                             "username": self.object.username,
                             "first_name": self.object.first_name,
                             "last_name": self.object.last_name,
                             "role": self.object.role,
                             "age": self.object.age,
                             "locations": list(map(str, self.object.location.all()))
                             }, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({'status': 'ok'}, safe=False)
