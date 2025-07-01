from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    if title.casefold() not in (x.casefold() for x in util.list_entries()):
        return render(request, "encyclopedia/error.html", {
        })
    else:
        return render(request, "encyclopedia/title.html", {
            "content": util.get_entry(title),
            "title": title
        })
    
def search(request):
    query = str(request.GET.get("q", "Did not work"))
    entries = util.list_entries()

    if query.casefold() in (x.casefold() for x in entries):
        return render(request, "encyclopedia/title.html", {
            "content": util.get_entry(query),
            "title": query
    })

    entries_result = []
    for x in entries:
        if query.casefold() in x.casefold():
            entries_result.append(x)

    return render(request, "encyclopedia/search.html", {
        "entries": entries_result,
        "search": query
    })

        