from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from .models import Recipe
from .forms import RecipeForm


def home(request):
    recipes = Recipe.objects.all()
    featured = recipes[:3]
    latest_recipes = Recipe.objects.order_by("-created_at")[:4]
    return render(
        request,
        "recipes/home.html",
        {
            "recipes": recipes,
            "featured": featured,
            "latest_recipes": latest_recipes,
        },
    )


def recipe_detail(request, slug: str):
    recipe = get_object_or_404(Recipe, slug=slug)
    return render(
        request,
        "recipes/recipe_detail.html",
        {
            "recipe": recipe,
        },
    )


def create_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save()
            return redirect("recipes:detail", slug=recipe.slug)
    else:
        form = RecipeForm()

    return render(
        request,
        "recipes/recipe_form.html",
        {
            "form": form,
        },
    )


def search_recipes(request):
    query = request.GET.get("q", "").strip()
    recipes = Recipe.objects.none()
    
    if query:
        recipes = Recipe.objects.filter(
            Q(title__icontains=query) |
            Q(subtitle__icontains=query) |
            Q(short_description__icontains=query) |
            Q(ingredients__icontains=query) |
            Q(directions__icontains=query)
        ).distinct()
    
    return render(
        request,
        "recipes/search_results.html",
        {
            "query": query,
            "recipes": recipes,
            "results_count": recipes.count(),
        },
    )


# Ingredient knowledge base
INGREDIENT_INFO = {
    "tomato": {
        "name": "Tomato",
        "description": "Tomatoes are rich in vitamin C, potassium, and lycopene. They add acidity and umami to dishes.",
        "storage": "Store at room temperature until ripe, then refrigerate.",
        "uses": "Great in salads, sauces, soups, and as a base for many dishes.",
    },
    "garlic": {
        "name": "Garlic",
        "description": "Garlic is a powerful flavor enhancer with antimicrobial properties. It contains allicin, which provides health benefits.",
        "storage": "Keep in a cool, dry place with good air circulation.",
        "uses": "Essential in many cuisines. Use minced, crushed, or sliced for different flavor intensities.",
    },
    "onion": {
        "name": "Onion",
        "description": "Onions add sweetness and depth when cooked. They're rich in antioxidants and vitamin C.",
        "storage": "Store in a cool, dry, well-ventilated area away from potatoes.",
        "uses": "Base for many dishes. Can be caramelized, sautéed, or used raw in salads.",
    },
    "bell pepper": {
        "name": "Bell Pepper",
        "description": "Bell peppers are rich in vitamin C and come in various colors. They add crunch and sweetness.",
        "storage": "Refrigerate in the crisper drawer for up to a week.",
        "uses": "Great raw in salads, roasted, stuffed, or sautéed in stir-fries.",
    },
    "zucchini": {
        "name": "Zucchini",
        "description": "Zucchini is a summer squash low in calories and high in water content. It's rich in vitamin A and C.",
        "storage": "Refrigerate in a plastic bag for up to a week.",
        "uses": "Can be grilled, sautéed, baked, or spiralized into noodles.",
    },
    "salmon": {
        "name": "Salmon",
        "description": "Salmon is rich in omega-3 fatty acids, protein, and vitamin D. It's a heart-healthy fish.",
        "storage": "Keep refrigerated and cook within 1-2 days of purchase.",
        "uses": "Can be baked, grilled, pan-seared, or poached. Pairs well with citrus and herbs.",
    },
    "chicken": {
        "name": "Chicken",
        "description": "Chicken is a lean protein source rich in B vitamins and selenium. It's versatile and widely used.",
        "storage": "Refrigerate and use within 1-2 days, or freeze for longer storage.",
        "uses": "Can be roasted, grilled, sautéed, or braised. Works with many flavor profiles.",
    },
    "pasta": {
        "name": "Pasta",
        "description": "Pasta is a carbohydrate-rich food made from wheat. Whole grain versions offer more fiber.",
        "storage": "Store in a cool, dry place in an airtight container.",
        "uses": "Base for many dishes. Cook al dente for best texture.",
    },
    "basil": {
        "name": "Basil",
        "description": "Basil is an aromatic herb with a sweet, slightly peppery flavor. It's rich in antioxidants.",
        "storage": "Keep fresh basil in water like flowers, or store in the refrigerator wrapped in damp paper towels.",
        "uses": "Essential in Italian cuisine. Use fresh in salads, pesto, or as a garnish.",
    },
    "mango": {
        "name": "Mango",
        "description": "Mangoes are tropical fruits rich in vitamin C, vitamin A, and fiber. They're sweet and juicy.",
        "storage": "Ripen at room temperature, then refrigerate to slow further ripening.",
        "uses": "Great in smoothies, salads, desserts, or eaten fresh.",
    },
    "coconut": {
        "name": "Coconut",
        "description": "Coconut provides healthy fats, fiber, and minerals. Coconut milk adds creaminess to dishes.",
        "storage": "Store coconut milk in the refrigerator after opening. Fresh coconut should be refrigerated.",
        "uses": "Used in curries, desserts, smoothies, and as a dairy alternative.",
    },
    "yogurt": {
        "name": "Yogurt",
        "description": "Yogurt is rich in probiotics, protein, and calcium. Greek yogurt has more protein.",
        "storage": "Keep refrigerated and check expiration date.",
        "uses": "Great in smoothies, as a marinade, in dips, or eaten plain with fruit.",
    },
    "lemon": {
        "name": "Lemon",
        "description": "Lemons are rich in vitamin C and add bright acidity to dishes. The zest contains aromatic oils.",
        "storage": "Store at room temperature or in the refrigerator for longer storage.",
        "uses": "Adds flavor to dressings, marinades, desserts, and beverages.",
    },
    "butter": {
        "name": "Butter",
        "description": "Butter adds richness and flavor. It's made from cream and contains saturated fats.",
        "storage": "Refrigerate butter, but let it soften at room temperature for baking.",
        "uses": "Used for sautéing, baking, spreading, and finishing dishes.",
    },
    "olive oil": {
        "name": "Olive Oil",
        "description": "Olive oil is rich in monounsaturated fats and antioxidants. Extra virgin is the highest quality.",
        "storage": "Store in a cool, dark place away from heat and light.",
        "uses": "Used for cooking, dressings, marinades, and finishing dishes.",
    },
}


@csrf_exempt
@require_http_methods(["GET", "POST"])
def voice_assistant(request):
    """Handle voice assistant queries about ingredients and recipe ingredients."""
    if request.method == "POST":
        import json
        try:
            data = json.loads(request.body)
            query = data.get("query", "").strip().lower()
        except:
            query = ""
    else:
        query = request.GET.get("q", "").strip().lower()
    
    if not query:
        return JsonResponse({
            "success": False,
            "message": "I didn't catch that. Could you please repeat your question?",
            "type": "error",
        })
    
    query_lower = query.lower()
    
    # Check if this is a recipe ingredients query
    recipe_patterns = [
        "what are the ingredients for",
        "what ingredients for",
        "ingredients for",
        "what do i need for",
        "what do you need for",
        "ingredients needed for",
        "ingredients required for",
        "what are the ingredients to make",
        "ingredients to make",
        "what ingredients to make",
    ]
    
    is_recipe_query = any(pattern in query_lower for pattern in recipe_patterns)
    
    if is_recipe_query:
        # Extract recipe name
        recipe_name = None
        for pattern in recipe_patterns:
            if pattern in query_lower:
                recipe_name = query_lower.replace(pattern, "").strip()
                break
        
        # Remove common words
        common_words = ["the", "a", "an", "making", "to make", "recipe"]
        words = recipe_name.split()
        recipe_name = " ".join([w for w in words if w not in common_words]).strip()
        
        # Search for recipe
        recipes = Recipe.objects.filter(
            Q(title__icontains=recipe_name) |
            Q(slug__icontains=recipe_name.replace(" ", "-"))
        )[:1]
        
        if recipes.exists():
            recipe = recipes.first()
            ingredients_list = [ing.strip() for ing in recipe.ingredients.splitlines() if ing.strip()]
            
            if ingredients_list:
                ingredients_text = ", ".join(ingredients_list)
                response_text = (
                    f"To make {recipe.title}, you'll need: {ingredients_text}."
                )
                return JsonResponse({
                    "success": True,
                    "type": "recipe_ingredients",
                    "recipe": recipe.title,
                    "recipe_slug": recipe.slug,
                    "message": response_text,
                    "ingredients": ingredients_list,
                })
            else:
                return JsonResponse({
                    "success": False,
                    "type": "error",
                    "message": f"I found {recipe.title}, but it doesn't have ingredients listed yet.",
                })
        else:
            return JsonResponse({
                "success": False,
                "type": "error",
                "message": f"I couldn't find a recipe called '{recipe_name}'. Try asking about recipes like 'Hearty Veggie Pasta', 'Citrus Herb Salmon', or 'Golden Mango Smoothie Bowl'.",
            })
    
    # Otherwise, treat as ingredient information query
    ingredient_name = None
    question_patterns = [
        "what is", "tell me about", "information about", "what about",
        "explain", "describe", "know about", "learn about"
    ]
    
    for pattern in question_patterns:
        if pattern in query_lower:
            ingredient_name = query_lower.replace(pattern, "").strip()
            break
    
    # If no pattern found, try to find ingredient directly
    if not ingredient_name:
        ingredient_name = query_lower
    
    # Remove common words
    common_words = ["the", "a", "an", "ingredient", "food"]
    words = ingredient_name.split()
    ingredient_name = " ".join([w for w in words if w not in common_words]).strip()
    
    # Search for ingredient in knowledge base
    found_ingredient = None
    for key, info in INGREDIENT_INFO.items():
        if key in ingredient_name or ingredient_name in key:
            found_ingredient = info
            break
        # Also check if any word matches
        if any(word in key for word in ingredient_name.split() if len(word) > 3):
            found_ingredient = info
            break
    
    if found_ingredient:
        response_text = (
            f"{found_ingredient['name']}. {found_ingredient['description']} "
            f"Storage tip: {found_ingredient['storage']} "
            f"Common uses: {found_ingredient['uses']}"
        )
        return JsonResponse({
            "success": True,
            "type": "ingredient_info",
            "ingredient": found_ingredient['name'],
            "message": response_text,
            "description": found_ingredient['description'],
            "storage": found_ingredient['storage'],
            "uses": found_ingredient['uses'],
        })
    else:
        return JsonResponse({
            "success": False,
            "type": "error",
            "message": f"I don't have information about '{ingredient_name}' yet. You can ask about ingredients like tomato, garlic, onion, or chicken. Or ask 'What are the ingredients for [recipe name]?' to get recipe ingredients.",
        })
