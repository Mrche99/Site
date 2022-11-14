
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views
from users import views as UserView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('reg', include('users.urls')),
    path('user/', views.LoginView.as_view(template_name='users/user.html'), name='user'),
    path('exit/', views.LogoutView.as_view(template_name='users/exit.html'), name='exit'),
    path('profile', UserView.profile, name='profile'),
    path('pass-reset/', views.PasswordResetView.as_view(template_name='main/pass_reset.html'), name='pass_reset'),
path('pass_reset_confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(template_name='main/password_reset_confirm.html'), name='password_reset_confirm'),
path('pass_reset_done/', views.PasswordResetDoneView.as_view(template_name='main/pass_reset_done.html'), name='pass_reset_done'),
path('password_reset_complete/', views.PasswordResetCompleteView.as_view(template_name='main/password_reset_complete.html'), name='pass_reset_complete'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)