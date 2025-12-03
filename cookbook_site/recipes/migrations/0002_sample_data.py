from django.db import migrations


def create_sample_recipes(apps, schema_editor):
    Recipe = apps.get_model("recipes", "Recipe")

    sample_recipes = [
        {
            "title": "Hearty Veggie Pasta",
            "subtitle": "A rainbow of roasted vegetables with herbed tomato sauce",
            "slug": "hearty-veggie-pasta",
            "hero_image": "recipes/images/hearty_veggie_pasta.svg",
            "prep_time": 20,
            "cook_time": 25,
            "servings": 4,
            "short_description": "A comforting pasta bowl packed with colorful veggies and fresh basil.",
            "ingredients": "\n".join(
                [
                    "12 oz whole-wheat penne",
                    "1 zucchini, sliced",
                    "1 bell pepper, sliced",
                    "1 cup cherry tomatoes",
                    "2 cups marinara sauce",
                    "Fresh basil leaves",
                ]
            ),
            "directions": "\n".join(
                [
                    "Roast vegetables with olive oil, salt, and pepper at 400°F (200°C) for 15 minutes.",
                    "Cook pasta according to package instructions until al dente.",
                    "Warm marinara sauce in a saucepan and stir in roasted vegetables.",
                    "Toss cooked pasta with the sauce and garnish with fresh basil.",
                ]
            ),
        },
        {
            "title": "Citrus Herb Salmon",
            "subtitle": "Bright flavors with a buttery finish",
            "slug": "citrus-herb-salmon",
            "hero_image": "recipes/images/citrus_herb_salmon.svg",
            "prep_time": 15,
            "cook_time": 18,
            "servings": 2,
            "short_description": "Oven-baked salmon with zesty citrus butter and fragrant herbs.",
            "ingredients": "\n".join(
                [
                    "2 salmon fillets",
                    "1 lemon, sliced",
                    "2 tbsp butter, melted",
                    "2 cloves garlic, minced",
                    "Fresh dill and parsley",
                    "Salt and pepper",
                ]
            ),
            "directions": "\n".join(
                [
                    "Preheat oven to 375°F (190°C) and line a baking sheet with parchment.",
                    "Arrange salmon on the sheet, drizzle with melted butter, garlic, salt, and pepper.",
                    "Top with lemon slices and herbs; bake for 15-18 minutes until flaky.",
                ]
            ),
        },
        {
            "title": "Golden Mango Smoothie Bowl",
            "subtitle": "Sunshine in a bowl with crunchy toppings",
            "slug": "golden-mango-smoothie-bowl",
            "hero_image": "recipes/images/golden_mango_smoothie_bowl.svg",
            "prep_time": 10,
            "cook_time": 0,
            "servings": 1,
            "short_description": "Creamy mango smoothie topped with toasted coconut and granola.",
            "ingredients": "\n".join(
                [
                    "1 cup frozen mango chunks",
                    "1/2 banana",
                    "1/2 cup coconut milk",
                    "1/4 cup Greek yogurt",
                    "Granola, coconut flakes, and chia seeds for topping",
                ]
            ),
            "directions": "\n".join(
                [
                    "Blend mango, banana, coconut milk, and yogurt until thick and smooth.",
                    "Pour into a bowl and arrange toppings to your liking.",
                ]
            ),
        },
    ]

    Recipe.objects.bulk_create(Recipe(**recipe) for recipe in sample_recipes)


def remove_sample_recipes(apps, schema_editor):
    Recipe = apps.get_model("recipes", "Recipe")
    Recipe.objects.filter(
        slug__in=[
            "hearty-veggie-pasta",
            "citrus-herb-salmon",
            "golden-mango-smoothie-bowl",
        ]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_sample_recipes, remove_sample_recipes),
    ]



