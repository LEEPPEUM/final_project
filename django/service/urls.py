from service import views
from django.urls import path

urlpatterns = [
    path("",views.home,name = "test-home"),
    path("form/",views.form, name="form"),
]