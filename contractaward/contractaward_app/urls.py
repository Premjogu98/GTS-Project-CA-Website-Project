from django.urls import path
from . import views
urlpatterns = [
    path('Home', views.home, name="Home"),
    path('Login', views.login_page, name="Login-Page"),
    path('Register', views.register_page, name="Register-Page"),
    path('Contact-us', views.conactus_page, name="Contact-Us-Page"),
    path('Tenders', views.Tenders_page, name="Tenders-page"),
    path('contract-award-detail/<tender_title>', views.view_tender_details, name="Tenders-detail"),
    path('<data>', views.view_tender_details, name="region-search"),
]