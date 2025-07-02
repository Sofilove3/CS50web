from django.shortcuts import render

from . import util

from django import forms

from django.urls import reverse

from django.http import HttpResponseRedirect

class NewPageForm(forms.Form):
    page = forms.CharField(label="Name Page")

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

def new(request):
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = NewPageForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the task from the 'cleaned' version of form data
            page = form.cleaned_data["page"]
            content = request.POST["body_text"]

            if util.get_entry(page):
                return render(request, "encyclopedia/page_already_exsist.html", {
                    "page": page
            })
            else:
                util.save_entry(page, content)
                return render(request, "encyclopedia/index.html", {
                    "entries": util.list_entries()
                })

    return render(request, "encyclopedia/new.html", {
        "form": NewPageForm()
    })