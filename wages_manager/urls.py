from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'wages_manager'

# We use default router to route urls to the correct ViewSet view
router = DefaultRouter()
router.register(r'courier', views.CourierViewSet, basename='courier')
router.register(r'trip', views.TripViewSet, basename='trip')
router.register(r'wage_reduction', views.WageReductionViewSet, basename='wage_reduction')
router.register(r'wage_increment', views.WageIncrementViewSet, basename='wage_increment')
router.register(r'daily_wage', views.DailyWageViewSet, basename='daily_wage')

urlpatterns = [
    path('', include(router.urls)),
    path('weekly_wage/', views.WeeklyWageView.as_view())
]