from recipesplus.models import Recipe

_all__ = ["add_flagged_recipes_to_context"]


def add_flagged_recipes_to_context(request):
    flagged_recipe_queryset = Recipe.objects.filter(is_flagged=True)
    
    return {
        "flagged_recipe_count": flagged_recipe_queryset.count(),
        "flagged_recipes":
            flagged_recipe_queryset.order_by("title")[:10],
        }