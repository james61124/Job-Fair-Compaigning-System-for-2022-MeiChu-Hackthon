from django.urls import include, re_path
from . import views
# 用來串接callback主程式
urlpatterns = [
    re_path('^callback/', views.callback),
]