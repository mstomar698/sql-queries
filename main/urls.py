"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.shortcuts import redirect
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	path("", lambda request : redirect('auth/login/') , name="redirect_login"),
    path('admin/', admin.site.urls),
    path('auth/', include('user_onboarding.urls')),
    path('table/v1/', include('table.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# from django.conf.urls import (
# handler400, handler403, handler404, handler500
# )

# handler404 = 'main.views.handler404'
# handler403 = 'my_app.views.permission_denied'
# handler404 = 'my_app.views.page_not_found'
# handler500 = 'main.views.server_error'