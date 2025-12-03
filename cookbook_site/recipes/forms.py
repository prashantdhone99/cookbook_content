from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            "title",
            "subtitle",
            "slug",
            "short_description",
            "prep_time",
            "cook_time",
            "servings",
            "ingredients",
            "directions",
            "uploaded_image",
        ]
        widgets = {
            "short_description": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Describe the recipe in a few lines"}
            ),
            "ingredients": forms.Textarea(
                attrs={
                    "rows": 6,
                    "placeholder": "List each ingredient on a new line",
                }
            ),
            "directions": forms.Textarea(
                attrs={
                    "rows": 6,
                    "placeholder": "Provide step-by-step directions, one per line",
                }
            ),
        }

    def save(self, commit=True):
        recipe = super().save(commit=False)
        if not recipe.hero_image:
            recipe.hero_image = "recipes/images/hearty_veggie_pasta.svg"
        if commit:
            recipe.save()
        return recipe



