from django.urls import path, include

app_name = 'accounts'

urlpatterns = [
    path('api/', include('apps.accounts.api.urls')),
] 