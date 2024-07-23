from django.urls import path, include

from rest_framework.routers import SimpleRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from .views import site
from .views import api

app_name = 'recipes'

recipe_api_v2_router = SimpleRouter()
recipe_api_v2_router.register('recipes/api/v2', api.RecipeAPIv2ViewSet, basename='recipes-api') # recipes:basename(recipe-api-list ou detail)

urlpatterns = [
    path(
        '',
        site.RecipeListViewHome.as_view(),
        name="home"
    ),
    path(
        'recipes/search/',
        site.RecipeListViewSearch.as_view(),
        name="search"
    ),
    path(
        'recipes/tags/<slug:slug>/',
        site.RecipeListViewTag.as_view(),
        name="tag"
    ),
    path(
        'recipes/category/<int:category_id>/',
        site.RecipeListViewCategory.as_view(),
        name="category"
    ),
    path(
        'recipes/<int:pk>/',
        site.RecipeDetail.as_view(),
        name="recipe"
    ),
    path(
        'recipes/theory/',
        site.theory,
        name='theory',
    ),

    # API
    path('recipes/api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('recipes/api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('recipes/api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('', include(recipe_api_v2_router.urls)),
    # path('recipes/api/v2/',
    #     api.RecipeAPIv2ViewSet.as_view({
    #         'get': 'list',
    #         'post': 'create'
    #     }),
    #     name='recipes_api_v2'
    # ),
    # path('recipes/api/v2/<int:pk>/',
    #     api.RecipeAPIv2ViewSet.as_view({
    #         'get': 'retrieve',
    #         'patch': 'partial_update',
    #         'delete': 'destroy'
    #     }),
    #     name='recipe_api_v2_detail'
    # ),
    path('recipes/api/v2/tag/<int:pk>/',
        api.tag_api_detail,
        name='recipe_api_v2_tag'
    ),
]

# urlpatterns += recipe_api_v2_router.urls