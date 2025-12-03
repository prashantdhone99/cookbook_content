from django.contrib import admin

from .models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "prep_time", "cook_time", "servings")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "subtitle", "short_description")
