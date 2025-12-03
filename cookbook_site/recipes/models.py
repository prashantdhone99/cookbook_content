from django.db import models


class Recipe(models.Model):
    """Represents a cookbook entry."""

    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(unique=True)
    hero_image = models.CharField(
        max_length=255,
        help_text="Relative path to a hero image stored under recipes static files.",
        blank=True,
    )
    uploaded_image = models.ImageField(
        upload_to="recipes/uploads/", blank=True, null=True
    )
    prep_time = models.PositiveIntegerField(help_text="Preparation time in minutes")
    cook_time = models.PositiveIntegerField(help_text="Cooking time in minutes")
    servings = models.PositiveIntegerField(default=1)
    short_description = models.TextField()
    ingredients = models.TextField(help_text="One ingredient per line")
    directions = models.TextField(help_text="One step per line")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title
