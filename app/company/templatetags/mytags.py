from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def index(list_, index):
    try:
        return list_[index]
    except (IndexError, TypeError):
        return None

@register.filter
def add_commas(value):
    return f"{value:,}"

@register.filter
def get_grade(mark):
    if mark >= 90:
        return 'A'
    elif mark >= 75:
        return 'B'
    elif mark >= 60:
        return 'C'
    elif mark >= 40:
        return 'D'
    else:
        return 'E'

# get accurate numbers for pagination pages
@register.filter
def get_num_by_page(counter, page_number, page_size=20):
    try:
        page_number = int(page_number)
        counter = int(counter)
        return (page_number - 1) * page_size + counter
    except (ValueError, TypeError):
        return counter  # fallback if something goes wrong
    
