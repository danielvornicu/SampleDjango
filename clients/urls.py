from django.urls import path, include

from . import views

from rest_framework import routers

#The REST Framework router 
router = routers.DefaultRouter()
router.register(r'clients', views.ClientViewSet)

urlpatterns = [
    #
    path('client/', views.index, name="index"),
    path('client/<int:id>', views.show, name="show"),
    path('client/new', views.create, name="create"),
    path('client/<int:id>/edit', views.edit, name="edit"),
    path('client/<int:id>/delete', views.delete, name="delete"),
    #REST API(without Django Rest Framework)
    path('clients', views.api_index, name="api_index"),
    path('clients/<int:id>', views.api_show, name="api_show"),
    path('clients/new', views.api_create, name="api_create"),
    path('clients/<int:id>/edit', views.api_edit, name="api_edit"),
    path('clients/<int:id>/delete', views.api_delete, name="api_delete"),

    #Django Rest Framework API
    # Wire up our API using automatic URL routing.
    # Additionally, we include login URLs for the browsable API.
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]