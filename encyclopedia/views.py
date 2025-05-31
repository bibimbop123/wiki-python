from django.shortcuts import render, redirect
from django.http import Http404
from . import util
import markdown2
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        raise Http404("Entry not found")
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": {
                    "title": title,
                    "content": content
    }
})
def search(request):
    query = request.GET.get('q', '')
    entries = util.list_entries()
    if query in entries:
        return redirect('entry', title=query)
    else:
        return render(request, "encyclopedia/search.html", {
            "entries": [entry for entry in entries if query in entry]
        })

def new_page(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()

        # Check if title or content is empty
        if not title or not content:
            return render(request, "encyclopedia/new_page.html", {
                "error": "Title and content cannot be empty."
            })

        # Check if an entry with the same title already exists
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "An entry with this title already exists."
            })

        # Save the new entry
        util.save_entry(title, content)
        return redirect('entry', title=title)
    else:
        return render(request, "encyclopedia/new_page.html")

def edit_page(request, title):
    if request.method == 'POST':
        content = request.POST.get('content')
        util.save_entry(title, content)
        return redirect('entry', title=title)
    else:
        return render(request, "encyclopedia/edit_page.html", {
            "title": title,
            "content": util.get_entry(title)
        })
    
def random_page(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return redirect('entry', title=title)