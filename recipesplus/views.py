from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models.aggregates import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils import simplejson
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from recipesplus.forms import CategoryForm
from recipesplus.forms import RecipeForm
from recipesplus.models import Category
from recipesplus.models import Recipe
from recipesplus.search_indexes import IndexManager
from recipesplus.importing import extract_recipe_data
from django.template.loader import render_to_string


_HTTP_METHOD_POST = "POST"


_IMPORTED_DATA_KEY = "imported_recipe_data"


_RECIPE_INDEX_MANAGER = IndexManager(Recipe)


class _JSONResponse(HttpResponse):
    
    def __init__(self, data, **extra):
        super(_JSONResponse, self).__init__(
            simplejson.dumps(data),
            content_type="application/json",
            **extra
            )


def view_frontpage(request):
    recency_limit = 5
    recently_created_recipes = \
        Recipe.objects.order_by('-creation_date')[:recency_limit]
    recently_updated_recipes = \
        Recipe.objects.order_by('-last_updated_date')[:recency_limit]
    recently_viewed_recipes = \
        Recipe.objects.order_by('-last_viewed_date')[:recency_limit]
    
    context = {
       'recently_created_recipes': recently_created_recipes,
       'recently_updated_recipes': recently_updated_recipes,
       'recently_viewed_recipes': recently_viewed_recipes,
       }
    return TemplateResponse(request, "frontpage.html", context)


def list_categories(request):
    
    categories = Category.objects.annotate(recipes_count=Count("recipes"))
    
    return TemplateResponse(
        request, "categories/list.html", {"categories": categories})


def list_category_recipes(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    
    recipes = category.recipes.all()
    
    return TemplateResponse(
        request,
        "categories/detail.html",
        {"recipes": recipes, "category": category},
        )


def delete_category(request, category_slug):
    
    category = get_object_or_404(Category, slug=category_slug)
    
    if request.method == _HTTP_METHOD_POST:
        category.delete()
        messages.success(request, "Category has been deleted")
        response = redirect("category_listing")
    else:
        response = TemplateResponse(
            request, "categories/delete.html", {"category": category})
    
    return response


def _modify_category(request, category=None):
    
    if request.method == _HTTP_METHOD_POST:
        form = CategoryForm(request.POST, instance=category)
        
        if form.is_valid():
            category = form.save()
            messages.success(request, "Your category has been saved")
            return redirect(category)
    else:
        form = CategoryForm(instance=category)
    
    if category:
        back_link = category.get_absolute_url()
    else:
        back_link = reverse("category_listing")
    
    return TemplateResponse(
        request, 
        "categories/category_form.html", 
        {"form": form, "category": category, "back_link": back_link},
        )


def create_category(request):
    return _modify_category(request)


def update_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    
    return _modify_category(request, category)


class ListRecipesView(ListView):
    
    model = Recipe
    
    template_name = "recipes/list.html"
    
    paginate_by = 10
    
    context_object_name = "recipes"


list_recipes = ListRecipesView.as_view()


class EmptyIngredientGroup(dict):
    
    def __init__(self):
        super(EmptyIngredientGroup, self).__init__()
        self["heading"] = None
        self["ingredients"] = []
    
    def __nonzero__(self):
        return any(self.values())


def _group_ingredients_by_heading(ingredients):
    groups = []
    current_group = EmptyIngredientGroup()

    for ingredient in ingredients:
        if ingredient["heading"]:
            if current_group:
                groups.append(current_group)
            current_group = EmptyIngredientGroup()
            current_group["heading"] = ingredient["text"]
        else:
            current_group["ingredients"].append(ingredient["text"])
    
    if any(current_group.values()):
        groups.append(current_group)
    
    return groups


def view_recipe(request, recipe_slug):
    
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    Recipe.objects.filter(slug=recipe_slug).update(last_viewed_date=now())
    
    grouped_ingredients = _group_ingredients_by_heading(recipe.ingredients)
    
    recipe_has_categories = recipe.categories.exists()
    
    return TemplateResponse(
        request,
        "recipes/detail.html", 
        {
            "recipe": recipe,
            "grouped_ingredients": grouped_ingredients,
            "recipe_has_categories": recipe_has_categories,
            },
        )


def delete_recipe(request, recipe_slug):
    
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    
    if request.method == _HTTP_METHOD_POST:
        recipe.delete()
        messages.success(request, "Recipe has been deleted")
        response = redirect("recipe_listing")
    else:
        response = TemplateResponse(
            request, "recipes/delete.html", {"recipe": recipe})
    
    return response


def import_recipe(request):
    if request.method == _HTTP_METHOD_POST:
        raw_recipe_data = request.POST.get("input", "")
        request.session[_IMPORTED_DATA_KEY] = extract_recipe_data(raw_recipe_data)
        messages.info(request, "Import complete")
        response = redirect("recipe_creation")
    else:
        response = TemplateResponse(request, "recipes/import.html", {})
    
    return response


def _modify_recipe(request, recipe=None):
    
    if request.method == _HTTP_METHOD_POST:
        form = RecipeForm(request.POST, instance=recipe)
        
        if form.is_valid():
            recipe = form.save()
            messages.success(request, "Your recipe has been saved successfully")
            return redirect(recipe)
    else:
        if recipe is None and _IMPORTED_DATA_KEY in request.session:
            initial_data = request.session.pop(_IMPORTED_DATA_KEY)
            raw_ingredients = initial_data.pop("ingredients", "")
            form_recipe = Recipe(**initial_data)
            form_recipe.raw_ingredients = raw_ingredients
            
            form = RecipeForm(instance=form_recipe)
        else:
            form = RecipeForm(instance=recipe)
    
    if recipe:
        back_link = recipe.get_absolute_url()
    else:
        back_link = reverse("recipe_listing")
    
    context = {"form": form, "recipe": recipe, "back_link": back_link}
    
    return TemplateResponse(
        request, "recipes/recipe_form.html", context)


def create_recipe(request):
    return _modify_recipe(request)


def update_recipe(request, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    
    return _modify_recipe(request, recipe)


def delete_multiple_recipes(request):
    recipes = Recipe.objects.filter(
        pk__in=request.REQUEST.getlist("recipe_ids"),
        )
    recipes_count = recipes.count()
    if not recipes_count:
        messages.error(
                request, "You must select at least one recipe to delete")
        response = redirect("recipe_listing")
    elif request.method == _HTTP_METHOD_POST:
        recipes.delete()
        messages.success(
            request, "%d recipes have been deleted" % recipes_count)
        response = redirect("recipe_listing")
    else:
        context = {"recipes": recipes, "recipes_count": recipes_count}
        response = TemplateResponse(
            request,
            "recipes/delete_multiple.html",
            context,
            )
    
    return response


def view_flagged_recipes(request):
    context = {
        "recipes": Recipe.objects.filter(is_flagged=True)
            .order_by("title"),
        }
    
    return TemplateResponse(
        request,
        "recipes/flagged_recipes_list.html",
        context,
        )


def get_flagged_recipes_dropdown(request):
    # The flagged recipes are calculated in a context processor so there's no
    # need to recalculate these
    return TemplateResponse(request, "snippets/flagged_recipes_dropdown.html")


@csrf_exempt
@require_POST
def unflag_all_recipes(request):
    Recipe.objects.filter(is_flagged=True).update(is_flagged=False)
    return _JSONResponse(_get_flagged_recipe_count())


@csrf_exempt
@require_POST
def flag_recipe(request, recipe_slug):
    return _alter_recipe_flagged_state(recipe_slug, True)


def _alter_recipe_flagged_state(recipe_slug, flag_state):
    Recipe.objects.filter(slug=recipe_slug).update(is_flagged=flag_state)
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    return _JSONResponse({
        "recipe_count": _get_flagged_recipe_count(),
        "new_html": render_to_string(
            "snippets/flag_control.html",
            {"recipe": recipe},
            ),
        })


@csrf_exempt
@require_POST
def unflag_recipe(request, recipe_slug):
    return _alter_recipe_flagged_state(recipe_slug, False)


def _get_flagged_recipe_count():
    return Recipe.objects.filter(is_flagged=True).count()


def control_index(request):
    if request.method == _HTTP_METHOD_POST:
        action = request.POST.get("action")
        manager_action_method = getattr(_RECIPE_INDEX_MANAGER, action, None)
        if action:
            message = manager_action_method()
            messages.info(request, message)
        else:
            messages.error(request, "You must select an indexing action")
        response = redirect("indexing")
    else:
        response = TemplateResponse(request, "search/index_control.html")
    
    return response
