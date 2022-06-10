from django.urls import path
from html_management.views import html_templates_list, html_template_activate, html_template_delete

urlpatterns = [
    path('list/', html_templates_list, name="html_templates_list"),
    path('activate/<int:pk>/', html_template_activate, name="html_template_activate"),
    path('delete/<int:pk>/', html_template_delete, name="html_template_delete"),
       
]
