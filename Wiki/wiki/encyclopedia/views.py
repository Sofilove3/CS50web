from django.shortcuts import render

from . import util

from django import forms

import random

class NewPageForm(forms.Form):
    page = forms.CharField(label="Name Page")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    if request.method == "POST":
        return render(request, "encyclopedia/edit.html", {
            "title": request.POST["title"],
            "content": request.POST["content"],
        })
        
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
                return render(request, "encyclopedia/title.html", {
                    "content": util.get_entry(page),
                    "title": page
                })

    return render(request, "encyclopedia/new.html", {
        "form": NewPageForm()
    })

def edit(request):
    if request.method == "POST":
        content = request.POST["content"]
        title = request.POST["title"]
        util.save_entry(title, content)
        return render(request, "encyclopedia/title.html", {
            "content": util.get_entry(title),
            "title": title
        })
 
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content,
    })

def random_page(request):
    all_entries = util.list_entries()
    max_len = len(all_entries)
    number_entry = random.randint(0, max_len -1)
    print(number_entry)
    entry = all_entries[number_entry]
    return render(request, "encyclopedia/title.html", {
        "content": util.get_entry(entry),
        "title": entry
    })