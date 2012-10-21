from csv import reader
from optparse import make_option
from os.path import expanduser

from django.core.management.base import BaseCommand

from recipesplus.models import Recipe
from recipesplus.models import Category
from django.db import IntegrityError


class Command(BaseCommand):
    
    option_list = BaseCommand.option_list + (
        make_option(
            "-d",
            "--delete-existing",
            action="store_true",
            help="Delete all existing recipes before running the import",
            ),
        )
    
    def handle(self, *args, **options):
        if options["delete_existing"]:
            user_choice = raw_input(
                "Are you sure you want to delete all recipe data? [y/N]",
                )
            
            if user_choice.lower() == "y":
                print "Deleting all recipes and categories..."
                Recipe.objects.all().delete()
                Category.objects.all().delete()
                print "All recipes and categories cleared from system."
            else:
                print "Not deleting recipes. Continuing with import."

        csv_file = open(expanduser("~/Desktop/recipes_dump.csv"))
        csv_reader = reader(csv_file)
        
        for recipe_line in csv_reader:
            _import_recipe(recipe_line)


def _import_recipe(recipe_data):
    try:
        recipe = Recipe.objects.create(
            title=recipe_data[0],
            serves=recipe_data[1],
            raw_ingredients=recipe_data[2],
            method=recipe_data[3],
            )
    except IntegrityError, exc:
        print u"!!! %s" % recipe_data[0], exc
        return
    
    print recipe.title
    
    for category_name in recipe_data[4:]:
        category = Category.objects.get_or_create(title=category_name)[0]
        recipe.categories.add(category)
    