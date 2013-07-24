from django.db.models import permalink
from django.db.models.base import Model
from django.db.models.fields import BooleanField
from django.db.models.fields import CharField
from django.db.models.fields import DateTimeField
from django.db.models.fields import SlugField
from django.db.models.fields import TextField
from django.db.models.fields.related import ManyToManyField
from django.template.defaultfilters import slugify


__all__ = ["Category", "Recipe", "INGREDIENT_HEADING_MARKER"]


INGREDIENT_HEADING_MARKER = "|"


class Category(Model):
    title = CharField(max_length=128, unique=True)
    slug = SlugField(max_length=128, unique=True)
    
    class Meta:
        ordering = ("title",)
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return self.title
    
    @permalink
    def get_absolute_url(self):
        return ("category_recipes_listing", (), {"category_slug": self.slug})


class _RecipeIngredientDescriptor(property):
    def __get__(self, instance, owner):
        if not instance:
            return self
        
        if not instance.raw_ingredients:
            return []
        
        ingredients = []
        for line in instance.raw_ingredients.splitlines():
            stripped_line = line.strip()
            
            if stripped_line.startswith(INGREDIENT_HEADING_MARKER):
                ingredients.append({
                    "heading": True,
                    "text": stripped_line[1:],
                    })
            else:
                ingredients.append({
                    "heading": False,
                    "text": stripped_line,
                    })
        
        return ingredients
    
    def __set__(self, instance, ingredients):
        if not ingredients:
            instance.raw_ingredients = ""
            return
        
        raw_ingredient_components = []
        for ingredient in ingredients:
            if ingredient["heading"]:
                text = u"%s%s" % (INGREDIENT_HEADING_MARKER, ingredient["text"])
            else:
                text = ingredient["text"]
            raw_ingredient_components.append(text)
        
        instance.raw_ingredients = u"\n".join(raw_ingredient_components)


class Recipe(Model):
    title = CharField(max_length=128, unique=True)
    slug = SlugField(max_length=128, unique=True)
    
    serves = CharField(max_length=5)
    raw_ingredients = TextField()
    method = TextField()
    categories = ManyToManyField(Category, blank=False, related_name="recipes")
    
    ingredients = _RecipeIngredientDescriptor()
    
    is_flagged = BooleanField(default=False)
    
    creation_date = DateTimeField(auto_now_add=True)
    last_updated_date = DateTimeField(auto_now=True)
    last_viewed_date = DateTimeField(editable=False, blank=True, null=True)
    
    @property
    def instructions(self):
        cleaned_instructions = []
        if self.method:
            for line in self.method.splitlines():
                stripped_line = line.strip()
                if stripped_line:
                    cleaned_instructions.append(stripped_line)
        
        return cleaned_instructions
    
    class Meta:
        ordering = ("title",)
        
    def __unicode__(self):
        return self.title
    
    @permalink
    def get_absolute_url(self):
        return ("recipe_detail", (), {"recipe_slug": self.slug})
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Recipe, self).save(*args, **kwargs)
