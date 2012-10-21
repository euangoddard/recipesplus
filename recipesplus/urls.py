from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",

    url(r"^admin/", include(admin.site.urls)),
    url(r"^search/", include("haystack.urls")),
)

urlpatterns += patterns("recipesplus.views",
    url(r"^categories/add/$", "create_category", name="category_creation"),
    url(r"^categories/(?P<category_slug>[\w-]+)/delete/$", "delete_category", name="category_deletion"),
    url(r"^categories/(?P<category_slug>[\w-]+)/edit/$", "update_category", name="category_updating"),
    url(r"^categories/(?P<category_slug>[\w-]+)/$", "list_category_recipes", name="category_recipes_listing"),
    url(r"^categories/$", "list_categories", name="category_listing"),
    
    url(r"^recipes/add/$", "create_recipe", name="recipe_creation"),
    url(r"^recipes/import/$", "import_recipe", name="recipe_import"),
    url(r"^recipes/delete-multiple/$", "delete_multiple_recipes", name="recipes_bulk_deletion"),
    url(r"^recipes/flagged/$", "view_flagged_recipes", name="flagged_recipe_list"),
    url(r"^recipes/flagged/clear/$", "unflag_all_recipes", name="flagged_recipe_clearing"),
    url(r"^recipes/flagged/dropdown/$", "get_flagged_recipes_dropdown", name="flagged_recipe_dropdown"),
    url(r"^recipes/(?P<recipe_slug>[\w-]+)/delete/$", "delete_recipe", name="recipe_deletion"),
    url(r"^recipes/(?P<recipe_slug>[\w-]+)/edit/$", "update_recipe", name="recipe_updating"),
    url(r"^recipes/(?P<recipe_slug>[\w-]+)/flag/$", "flag_recipe", name="recipe_flagging"),
    url(r"^recipes/(?P<recipe_slug>[\w-]+)/unflag/$", "unflag_recipe", name="recipe_unflagging"),
    url(r"^recipes/(?P<recipe_slug>[\w-]+)/$", "view_recipe", name="recipe_detail"),
    url(r"^recipes/$", "list_recipes", name="recipe_listing"),
    
    url(r"^indexing/$", "control_index", name="indexing"),
    
    url(r"^$", "view_frontpage", name="frontpage"),
    )
