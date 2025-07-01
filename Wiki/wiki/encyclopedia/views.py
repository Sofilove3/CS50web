from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
'''
def title(request, title):
    if title.capitalize() in util.list_entries():
        return render(request, "encyclopedia/title.html", {
            "content": util.get_entry(title),
            "title": title
        })
    else:
        return render(request, "encyclopedia/error.html", {
        })
'''
def title(request, title):
    #logic is not working...
    if title.casefold() not in (x.casefold() for x in util.list_entries()):
        return render(request, "encyclopedia/error.html", {
        })
    else:
        return render(request, "encyclopedia/title.html", {
            "content": util.get_entry(title),
            "title": title
        })

# if 'MICHAEL89'.casefold() in (name.casefold() for name in USERNAMES):