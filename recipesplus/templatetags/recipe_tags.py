from django.template import Library


register = Library()

@register.inclusion_tag("snippets/category_badges.html")
def category_badges(recipe):
    return {"categories": recipe.categories.all()}
