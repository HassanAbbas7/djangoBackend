from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from scraper.views import UserViewSet
from rest_framework.routers import DefaultRouter
from scraper import views



urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('mainscraper.urls')),
    path('test/<str:keyword>', views.GetData.as_view(), name="test"),
    path('API', views.DataView.as_view(), name="API"),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('scraper/', views.index, name="scraper"),
    path('start_scrape/', views.start_scrape, name="start_scrape"),
    path('testing', views.test, name="testing"),
    path('clap_post/<int:id>', views.ClapPost.as_view(), name="clap"),
    path('fav_post/<int:id>', views.FavPost.as_view(), name="fav")
]

router = DefaultRouter()
router.register('user', UserViewSet, basename='user')
urlpatterns += router.urls


