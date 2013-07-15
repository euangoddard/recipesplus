from haystack import connections
from haystack.fields import CharField
from haystack.indexes import Indexable
from haystack.indexes import SearchIndex

from recipesplus.models import Recipe


__all__ = ["RecipeIndex", "IndexManager"]


class RecipeIndex(SearchIndex, Indexable):
    text = CharField(document=True, use_template=True)
    
    def get_model(self):
        return Recipe
    


class IndexManager(object):
    
    def __init__(self, model):
        self.model = model
        self.backend = connections['default'].get_backend()
        self.index = RecipeIndex()
    
    def update(self):
        self.index.update()
        updated_items = self.index.index_queryset().count()
        return u"updated %d %s in the search index" % (
            updated_items, self.model._meta.verbose_name_plural)
    
    def clear(self):
        self.backend.clear()
        return "Cleared search index"
    
    def rebuild(self):
        messages = []
        messages.append(self.clear())
        messages.append(self.update())
        return " and ".join(messages)