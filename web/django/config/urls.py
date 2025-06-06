"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.intro),
    path('generate', core_views.generate_view ),
    path('stream-response/', core_views.stream_chat_response, name='stream_response'),
    path('embed/', core_views.embed_view, name='embed'),
    path('documents_list', core_views.document_list, name='documents_list'),
    path('delete/<int:pk>/', core_views.document_delete, name='delete'),

    path('semantic', core_views.semantic_search, name='semantic'),
    path("chat/", core_views.chat_page, name="chat_page"),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
