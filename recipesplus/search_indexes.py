from haystack import site
from haystack.fields import CharField
from haystack import backend
from haystack.indexes import RealTimeSearchIndex

from recipesplus.models import Recipe


__all__ = ["RecipeIndex", "IndexManager"]


class RecipeIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    

site.register(Recipe, RecipeIndex)


class IndexManager(object):
    
    def __init__(self, model):
        self.model = model
        self.index = site.get_index(model)
    
    def update(self):
        queryset = self.model.objects.all()
        self.index.backend.update(self.index, queryset)
        return u"updated %d %s in the search index" % (
            queryset.count(), self.model._meta.verbose_name_plural)
    
    def clear(self):
        search_backend = backend.SearchBackend(site=site)
        search_backend.clear()
        return "Cleared search index"
    
    def rebuild(self):
        messages = []
        messages.append(self.clear())
        messages.append(self.update())
        return " and ".join(messages)