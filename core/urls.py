from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
# from drf_spectacular.views import (
#     SpectacularAPIView,
#     SpectacularSwaggerView,
# )
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
#     TokenVerifyView,
#     TokenBlacklistView,
# )

from core.schema import swagger_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('cars/', include('apps.cars.urls')),
    path('users/', include('apps.users.urls')),

] + swagger_urlpatterns

# Wrapper
# urlpatterns += [
#     # OpenAPI schema
#     path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
#
#     # Swagger UI
#     path('', SpectacularSwaggerView.as_view(url_name='schema')),
#     path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
# ]

if settings.DEBUG:
    # Статические файлы (CSS, JS, иконки)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # Медиафайлы ()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




# # Authenticate API
# urlpatterns += [
#     # Получение access и refresh токена
#     path('api/token/', TokenObtainPairView.as_view(), name='token_pair_obtain'),
#
#     # Обновление access токена по refresh
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#
#     # Проверка токена на валидность
#     path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
#
#     # Черный список токена (для logout)
#     path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
# ]