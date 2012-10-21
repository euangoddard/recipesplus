from urllib import urlencode

from django.template import Library


register = Library()


PAGE_NUMBER_KEY = "page"


@register.inclusion_tag("snippets/paginator.html", takes_context=True)
def paginator(context, adjacent_pages=3):
    """Render the list pagination controls (first, adjacent and last pages)."""
    
    # Get the base query string to be used in the pagination
    request = context["request"]
    base_query_string_data = {}
    for (arg_key, arg_value) in request.GET.items():
        if arg_key != PAGE_NUMBER_KEY:
            arg_key_encoded = arg_key.encode("utf8")
            arg_value_encoded = arg_value.encode("utf8")
            base_query_string_data[arg_key_encoded] = arg_value_encoded

    paginator_object = context["paginator"]
    page_count = paginator_object.num_pages
    current_page = int(request.GET.get(PAGE_NUMBER_KEY, 1))

    # Get the links to the pages surrounding the current one
    bottom_page = max(current_page - adjacent_pages, 1)
    top_page = min(current_page + adjacent_pages, page_count) 
    page_numbers = range(bottom_page, top_page + 1)

    return {
        "current_page": current_page,
        "page_count": page_count,
        "page_numbers": page_numbers,
        "show_first": 1 not in page_numbers,
        "show_last": page_count not in page_numbers,
        "previous_page_number": current_page - 1,
        "next_page_number": current_page + 1,
        "base_query_string_data": base_query_string_data,
        }


@register.simple_tag(takes_context=True)
def make_page_query_string(context, page_number):
    base_query_string_data = context["base_query_string_data"].copy()
    base_query_string_data[PAGE_NUMBER_KEY] = str(page_number)
    
    return urlencode(base_query_string_data)
