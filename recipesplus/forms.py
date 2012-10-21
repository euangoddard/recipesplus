from django.forms.fields import CharField
from django.forms.models import ModelForm
from django.forms.widgets import TextInput
from django.forms.widgets import Textarea

from recipesplus.models import Category
from recipesplus.models import Recipe
from django.utils import simplejson
from django.forms.widgets import SelectMultiple


__all__ = ["CategoryForm", "ReceipeForm"]


class IngredientsWidget(Textarea):
    
    def __init__(self, attrs=None):
        default_attrs = {"class": "ingredients-widget"}
        
        if attrs:
            default_attrs.update(attrs)
            
        super(IngredientsWidget, self).__init__(attrs=default_attrs)
    
    class Media:
        js = ("js/handlebars.js", "js/widgets/ingredients.js")


class MethodWidget(Textarea):
    
    def __init__(self, attrs=None):
        default_attrs = {"class": "method-widget"}
        
        if attrs:
            default_attrs.update(attrs)
            
        super(MethodWidget, self).__init__(attrs=default_attrs)
    
    class Media:
        js = ("js/widgets/method.js", )


class CategoriesWidget(SelectMultiple):
    
    def __init__(self, attrs=None):
        default_attrs = {"class": "use-selectmore"}
        
        if attrs:
            default_attrs.update(attrs)
            
        super(CategoriesWidget, self).__init__(attrs=default_attrs)
    
    class Media:
        js = ("js/widgets/jquery.selectmore.js", )


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        exclude = ["slug"]
        widgets = {
            "title": TextInput(attrs={"class": "input-xxlarge"}),
            }


class RecipeForm(ModelForm):
    
    ingredients = CharField(widget=IngredientsWidget)
    
    class Meta:
        model = Recipe
        exclude = ["slug", "raw_ingredients", "is_flagged"]
        widgets = {
            "title": TextInput(attrs={"class": "input-xxlarge"}),
            "serves": TextInput(attrs={"class": "input-mini"}),
            "method": MethodWidget,
            "categories": CategoriesWidget,
            }
    
    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.fields["ingredients"].initial = \
            simplejson.dumps(self.instance.ingredients)
        
        self.fields["categories"].help_text = None
    
    def save(self, commit=True):
        raw_ingredient_data = self.cleaned_data["ingredients"]
        self.instance.ingredients = simplejson.loads(raw_ingredient_data)
        
        return super(RecipeForm, self).save(commit)

RecipeForm.base_fields.keyOrder = [
    "title",
    "serves",
    "ingredients",
    "method", 
    "categories",
    ]