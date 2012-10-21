"""
Functionality to import a plain text recipe into the system.

Assumes the format will be something like:

TITLE
Serves: x-y

Ingredients

a
b
...

Method

1
2

"""

import re

__all__ = ["extract_recipe_data"]


_METHOD_INSTRUCTION_RE = re.compile(r'^\d+\.\W+(.+)$')

_BULLETED_LINES_RE = re.compile(ur'^\u2022\W+(.+)$', re.UNICODE)

_SERVES_RE = re.compile(r'^serves\W+(\d+)')

_TEMPERATURE_RE = re.compile('(\d{3})([oO]{1})([CF]{1})')


def extract_recipe_data(recipe_text):
    raw_lines = recipe_text.split('\n')
    
    title = None
    serves = None
    ingredients_lines = []
    method_lines = []
    current_group = None
    
    for raw_line in raw_lines:
        # Clean up lines to extraneous information
        cleaned_line = raw_line.strip()
        
        bullet_match = _BULLETED_LINES_RE.match(cleaned_line)
        if bullet_match:
            cleaned_line = bullet_match.group(1)
        
        method_match = _METHOD_INSTRUCTION_RE.match(cleaned_line)
        if method_match:
            cleaned_line = method_match.group(1)
        
        # Look for markers which indicate key points in the text
        lower_line = cleaned_line.lower()
        
        serves_match = _SERVES_RE.match(lower_line)
        if cleaned_line and not title:
            title = lower_line.title()
        if serves_match:
            serves = serves_match.group(1)
        elif lower_line == "ingredients":
            current_group = ingredients_lines
        elif lower_line == "method":
            current_group = method_lines
        elif cleaned_line and current_group is not None:
            current_group.append(cleaned_line)
    
    return {
        'title': title,
        'serves': serves,
        'ingredients': u'\n'.join(ingredients_lines),
        'method': _build_method_text(method_lines),
        }


def _build_method_text(method_lines):
    method_text = u'\n'.join(method_lines)
    return _TEMPERATURE_RE.sub(u'\g<1>%s\g<3>' % unichr(186), method_text)
