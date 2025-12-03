from django.urls import path

from . import views

app_name = "recipes"

urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search_recipes, name="search"),
    path("api/voice-assistant/", views.voice_assistant, name="voice_assistant"),
    path("recipes/new/", views.create_recipe, name="create"),
    path("recipes/<slug:slug>/", views.recipe_detail, name="detail"),
]

