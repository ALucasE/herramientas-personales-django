from django.urls import path
from .views import (
    create_recipe,
    RecipeDetailView,
    RecipeListView,
    RecipeEditView,
    ingredient_detail,
    IngredientDetailEditView,
    IngredientDetailDeleteView,
    RecipeDeleteView,
)

urlpatterns = [
    path('', RecipeListView.as_view(), name='cookbook'),
    path('create/', create_recipe, name='create_recipe'),
    path('detail/<int:pk>', RecipeDetailView.as_view(), name='detail_recipe'),
    path('edit/<int:pk>', RecipeEditView.as_view(), name='edit_recipe'),
    path('delete/<int:pk>', RecipeDeleteView.as_view(), name='delete_recipe'),
    path('detail/<int:pk>/ingredient_detail/', ingredient_detail, name='ingredient_detail'),
    path('detail/ingredient_detail_edit/<int:pk>/', IngredientDetailEditView.as_view(), name='ingredient_detail_edit'),
    path('detail/ingredient_detail_detele/<int:pk>/', IngredientDetailDeleteView.as_view(), name='ingredient_detail_detele'),
]
