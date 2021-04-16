from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('blog', views.BlogListView.as_view(), name='blog'),
    path('blog/<int:pk>', views.BlogDetailView.as_view(), name='blog-detail'),
]
