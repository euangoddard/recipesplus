from django.template import Library
from django.core.urlresolvers import reverse


register = Library()


_MENU_ITEMS = (
    ("Home", "frontpage", "home"),
    (
        "Recipes",
        (
            ("All recipes", "recipe_listing", "list-alt"),
            ("Flagged recipes", "flagged_recipe_list", "flag"),
            ("Add a recipe", "recipe_creation", "plus"),
            ("Import a recipe", "recipe_import", "download-alt"),
            ),
        ),
    (
        "Categories",
        (
            ("Browse", "category_listing", "th-list"),
            ("Add a category", "category_creation", "plus"),
            ),
        ),
    )


@register.inclusion_tag("snippets/menu.html", takes_context=True)
def menu(context):
    current_url = context["request"].path
    active_link = {"url": None}
    processed_menu = _build_menu_level(_MENU_ITEMS, current_url, active_link)
    return {"menu": processed_menu, "active_url": active_link["url"]}


def _build_menu_level(menu_level, current_url, active_link):
    sub_menu = []
    for menu_item in menu_level:
        if len(menu_item) == 3:
            # This is a leaf node, so process this as a final option
            item_url = reverse(menu_item[1])
            if current_url.startswith(item_url):
                active_link["url"] = item_url
            sub_menu.append({
                "label": menu_item[0],
                "url": item_url,
                "icon": menu_item[2],
                })
        else:
            sub_menu.append({
                "label": menu_item[0],
                "children": _build_menu_level(
                    menu_item[1],
                    current_url,
                    active_link,
                    ),
                })
    
    return sub_menu
