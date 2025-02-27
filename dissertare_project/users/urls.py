""" users url """
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path("register/", views.register, name="register"),
    # activate view url
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    # password reset
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='users/password_reset.html'
        ),
        name='password_reset'
    ),
    # password reset done
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    # password reset confirm
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    # password reset complete
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
    path(
        'user_shipping_address/',
        views.user_shipping_address,
        name='user-shipping-address'
    ),
    path(
        'profile/',
        views.profile,
        name='profile'
    ),
    path(
        'update_user_shipping_address/',
        views.update_user_shipping_address,
        name='update-user-shipping-address'
    ),
    path(
        'user_books/',
        views.user_books,
        name='user-books'
    ),
    path(
        'staff_profile/',
        views.staff_profile,
        name='staff-profile'
    ),
    path(
        'upload_announcement/',
        views.upload_announcement,
        name='upload-announcement'
    ),
    path(
        'user_books_details/<int:book_id>',
        views.user_books_details,
        name='user-books-details'
    ),
]
