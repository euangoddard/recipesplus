from django.test import TestCase

from recipesplus.models import Recipe
from recipesplus.views import _group_ingredients_by_heading


class TestRecipeMethodInstructions(TestCase):
    
    def test_empty_method(self):
        recipe = Recipe(method=None)
        self.assertEqual([], recipe.instructions)
        
        recipe = Recipe(method="")
        self.assertEqual([], recipe.instructions)
        
        recipe = Recipe(method="\n\n\n")
        self.assertEqual([], recipe.instructions)
    
    def test_populated_method(self):
        instructions = ["Do this", "Do that", "Do the other"]
        
        recipe = Recipe(method="\n".join(instructions))
        self.assertEqual(instructions, recipe.instructions)
    
    def test_extraneous_whitespace(self):
        instructions = ["Do this", "Do that", "Do the other"]
        padded_instructions = [" Do this", "Do that ", " Do the other "]
        
        recipe = Recipe(method="\n".join(padded_instructions))
        self.assertEqual(instructions, recipe.instructions)
    
    def test_blank_lines(self):
        instructions = ["Do this", "Do that", "Do the other"]
        padded_instructions = ["Do this", "", "Do that", "   ", "Do the other"]
        
        recipe = Recipe(method="\n".join(padded_instructions))
        self.assertEqual(instructions, recipe.instructions)


class TestRecipeIngredients(TestCase):
    
    def test_get_empty_ingredients(self):
        recipe = Recipe()
        self.assertEqual([], recipe.ingredients)
        
        recipe = Recipe(raw_ingredients="")
        self.assertEqual([], recipe.ingredients)
    
    def test_get_no_grouping_markers(self):
        recipe = Recipe(raw_ingredients="Sugar\nButter\nMilk")
        
        expected_ingredients = [
            {"heading": False, "text": "Sugar"},
            {"heading": False, "text": "Butter"},
            {"heading": False, "text": "Milk"},
            ]
        self.assertEqual(expected_ingredients, recipe.ingredients)
    
    def test_get_grouping_markers(self):
        recipe = Recipe(raw_ingredients="|For the batter\nButter\nMilk\n|Another")
        
        expected_ingredients = [
            {"heading": True, "text": "For the batter"},
            {"heading": False, "text": "Butter"},
            {"heading": False, "text": "Milk"},
            {"heading": True, "text": "Another"},
            ]
        self.assertEqual(expected_ingredients, recipe.ingredients)
    
    def test_get_grouping_marker_in_text(self):
        recipe = Recipe(raw_ingredients="Sugar|Treacle\nButter\nMilk")
        
        expected_ingredients = [
            {"heading": False, "text": "Sugar|Treacle"},
            {"heading": False, "text": "Butter"},
            {"heading": False, "text": "Milk"},
            ]
        self.assertEqual(expected_ingredients, recipe.ingredients)
    
    def test_set_empty(self):
        recipe = Recipe()
        recipe.ingredients = []
        self.assertEqual("", recipe.raw_ingredients)
    
    def test_set_all_ingredients(self):
        recipe = Recipe()
        recipe.ingredients = [
            {"heading": False, "text": "Sugar"},
            {"heading": False, "text": "Butter"},
            {"heading": False, "text": "Milk"},
            ]
        self.assertEqual("Sugar\nButter\nMilk", recipe.raw_ingredients)
    
    def test_set_heading(self):
        recipe = Recipe()
        recipe.ingredients = [
            {"heading": True, "text": "For the batter"},
            {"heading": False, "text": "Butter"},
            {"heading": False, "text": "Milk"},
            {"heading": True, "text": "Another"},
            ]
        self.assertEqual(
            "|For the batter\nButter\nMilk\n|Another", recipe.raw_ingredients)
    
    def test_set_with_heading_marker_in_text(self):
        recipe = Recipe()
        
        recipe.ingredients = [
            {"heading": False, "text": "Sugar|Treacle"},
            {"heading": False, "text": "Butter"},
            {"heading": False, "text": "Milk"},
            ]
        self.assertEqual("Sugar|Treacle\nButter\nMilk", recipe.raw_ingredients)


class TestGroupIngredientsByHeading(TestCase):
    
    def test_no_headings(self):
        recipe = Recipe(raw_ingredients="Sugar\nButter\nMilk")
        
        expected_groupings = [
            {"heading": None, "ingredients": ["Sugar", "Butter", "Milk"]},
            ]
        found_groupings = _group_ingredients_by_heading(recipe.ingredients)
        self.assertEqual(expected_groupings, found_groupings)
    
    def test_single_heading(self):
        recipe = Recipe(raw_ingredients="|Batter\nSugar\nButter\nMilk")
        
        expected_groupings = [
            {"heading": "Batter", "ingredients": ["Sugar", "Butter", "Milk"]},
            ]
        found_groupings = _group_ingredients_by_heading(recipe.ingredients)
        self.assertEqual(expected_groupings, found_groupings)
    
    def test_empty_headings(self):
        recipe = Recipe(raw_ingredients="|One\n|Two")
        
        expected_groupings = [
            {"heading": "One", "ingredients": []},
            {"heading": "Two", "ingredients": []},
            ]
        found_groupings = _group_ingredients_by_heading(recipe.ingredients)
        self.assertEqual(expected_groupings, found_groupings)
    
    def test_mixture(self):
        recipe = Recipe(raw_ingredients="Sugar\nButter\nMilk\n|Other\nWater")
        
        expected_groupings = [
            {"heading": None, "ingredients": ["Sugar", "Butter", "Milk"]},
            {"heading": "Other", "ingredients": ["Water"]},
            ]
        found_groupings = _group_ingredients_by_heading(recipe.ingredients)
        self.assertEqual(expected_groupings, found_groupings)
    