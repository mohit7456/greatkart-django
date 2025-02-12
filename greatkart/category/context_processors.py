from .models import Category

def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)

# Context_processors are those in which it accepts the arguments and return dictionary values.
# we use this when wew click in store button then there is 'All category' option where our ll categories are dsplayed.
# We want that every category we setup links so when user click on it it go that category page easily.
# And tell the settings.py in templates section.