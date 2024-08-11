from .views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    DeleteUserAccountView,
    LogoutView,
    CustomProviderAuthView,
    SingleUser,
    UpdateUserAccountView,
    UsersWithRoleUserView,
    user_role_distribution,
    UsersWithRoleEmployeeView,
    CreateEmployeeAccountView,
    employee
)
from django.urls import path, re_path


urlpatterns = [
    path('jwt/create/', CustomTokenObtainPairView.as_view()),
    path('jwt/refresh/', CustomTokenRefreshView.as_view()),
    path('jwt/verify/', CustomTokenVerifyView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('getsingleuser/', SingleUser.as_view()),
    path('registration/', employee, name='registration-role-based'),
    path('users_with_role_user/', UsersWithRoleUserView.as_view(),
         name='users_with_role_user'),
    path('users_with_role_employee/', UsersWithRoleEmployeeView.as_view(),
         name='users_with_role_employee'),
    path('user_role_distribution/', user_role_distribution,
         name='user_role_distribution'),
    path('users/<int:pk>/update/', UpdateUserAccountView.as_view(),
         name='update_user_account'),
    path('users/<int:pk>/delete/', DeleteUserAccountView.as_view(),
         name='delete_user_account'),
    re_path(r'o/(?P<provider>\S+)/$',
            CustomProviderAuthView.as_view(), name='provider-auth')
]
