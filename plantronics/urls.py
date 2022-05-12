from baton.autodiscover import admin
from django.urls import include, path
from rest_framework import routers
from backend import views
from django_otp.admin import OTPAdminSite

admin.site.__class__ = OTPAdminSite

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='users')
router.register(r'groups', views.GroupViewSet)
router.register(r'plants', views.PlantViewSet)
router.register(r'family', views.FamilyViewSet)
router.register(r'info', views.InfoViewSet)
router.register(r'soilpreference', views.SoilPreferenceViewSet)
router.register(r'userplant', views.UserPlantViewSet)
router.register(r'genus', views.GenusViewSet, basename='genus')
router.register(r'edible', views.EdibleViewSet, basename='edible')


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
# And for baton which controls the styling for the admin interface
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('backend/', admin.site.urls),
    path('baton/', include('baton.urls')),
    path('login/', views.login),
    path('signup/', views.signup),
    path('user/', views.user),
    path('plantinfo/', views.plantInfo),
    path('plantsoil/', views.plantSoil),
    path('plantedible/', views.plantEdibles),
    path('getplants/', views.getPlants),
]
