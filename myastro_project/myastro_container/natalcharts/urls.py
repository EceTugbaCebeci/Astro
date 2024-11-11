from django.urls import path
from . import views 


urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('natal_chart/', views.NatalChartView.as_view(), name='natal_chart'),
    path('compatibility_analysis/', views.CompatibilityAnalysisView.as_view(), name='compatibility_analysis'),
    path('delete_relative/<int:relative_id>/', views.DeleteRelativeView.as_view(), name='delete_relative'),
    path('load_countries/', views.LoadCountriesView.as_view(), name='load_countries'),
    path('load_cities/', views.LoadCitiesView.as_view(), name='load_cities'),
    path('personalized_probabilities/', views.PersonalizedProbabilityView.as_view(), name='personalized_probabilities'),
    path('astrofun/', views.AstroFunView.as_view(), name='astrofun'),
    path('ask_astro/', views.AskAstroView.as_view(), name='ask_astro'),
    path('profile/update/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('profile/send-verification-code/', views.SendVerificationCodeView.as_view(), name='send_verification_code'),
    path('profile/verify-code/', views.VerifyCodeView.as_view(), name='verify_code'),
    path('profile/change-password/', views.ChangePasswordView.as_view(), name='change_password'),
]

