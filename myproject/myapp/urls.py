
from django.urls import path

from myapp import views

urlpatterns = [
    path('search/', views.normal_paper_search),
    path('advancedSearch/', views.advanced_paper_search),
]