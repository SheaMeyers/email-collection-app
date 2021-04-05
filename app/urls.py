"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    # TODO Do this later, get website up and running first
    # sign up  path('sign-up', views.Detail.as_view(), name='_detail'),
    # Admin seems to have a password-change function but no endpoint

    # Specific url path    path('<slug:url_path>', views.Detail.as_view(), name='_detail'),
    path('', TemplateView.as_view(template_name="base.html")),
]