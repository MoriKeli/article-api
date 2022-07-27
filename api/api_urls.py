from django.urls import path
from api import views

urlpatterns = [
    path('', views.ArticleAPIView.as_view()),
    path('<int:pk>', views.ArticleDetails.as_view()),
    path('generic/article/<int:id>', views.ArticleGenericAPIView.as_view(),),
    
]