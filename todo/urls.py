from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('', views.TodosViewSetApiView)

urlpatterns = [
    # functino base view
    path('', views.all_todos, name='all_todos'),
    path('<int:todo_id>', views.todo_detail, name='todo_detail'),

    # class base view
    path('cbv/', views.TodosListApiView.as_view(), name='all_todos_cbv'),
    path('cbv/<int:todo_id>', views.TodosDetailApiView.as_view(), name='todo_detail'),

    # mixins
    path('mix/', views.TodosListMixinApiView.as_view(), name='all_todos_mix'),
    path('mix/<int:pk>', views.TodosDetailMixinApiView.as_view(), name='todo_detail_mix'),

    # generics
    path('gen/', views.TodosListGenericApiView.as_view(), name='all_todos_gen'),
    path('gen/<int:pk>', views.TodosDetailGenericApiView.as_view(), name='todo_detail_gen'),

    # viewsets
    path('viewset/', include(router.urls), name='todos_viewset'),

    # users
    path('users/', views.UsersGenericApiView.as_view(), name='all_users')
]

