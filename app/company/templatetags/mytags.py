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

# get accurate numbers for pagination pages
@register.filter
def get_num_by_page(counter, page_number, page_size=20):
    try:
        page_number = int(page_number)
        counter = int(counter)
        return (page_number - 1) * page_size + counter
    except (ValueError, TypeError):
        return counter  # fallback if something goes wrong

@register.filter
def has_perm(user, perm_name):
    if not user or not user.is_authenticated:
        return False
    return user.has_cperm(perm_name)
