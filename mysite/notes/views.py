from django.shortcuts import render, get_object_or_404, redirect
from .models import Note, Category
from rest_framework import viewsets
from .serializers import NoteSerializer, CategorySerializer

# View to list all notes
def note_list(request):
    notes = Note.objects.all().order_by('-created_at')
    return render(request, 'notes/note_list.html', {'notes': notes})

# View to see details of a specific note
def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    return render(request, 'notes/note_detail.html', {'note': note})

# View to create a new note
def note_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        category_id = request.POST.get("category")

        if title and content and category_id:
            category = Category.objects.get(id=category_id)
            Note.objects.create(title=title, content=content, category=category)
            return redirect('note_list')
        else:
            error_message = "All fields are required."
            categories = Category.objects.all()  # Pass categories to the template
            return render(request, 'notes/note_create.html', {
                'error_message': error_message,
                'categories': categories,
            })
    else:
        categories = Category.objects.all()  # Pass categories to the template
        return render(request, 'notes/note_create.html', {'categories': categories})

# View to update an existing note
def note_update(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        category_id = request.POST.get("category")

        if title and content and category_id:
            category = Category.objects.get(id=category_id)
            note.title = title
            note.content = content
            note.category = category
            note.save()
            return redirect('note_detail', note_id=note.id)
        else:
            error_message = "All fields are required."
            categories = Category.objects.all()  # Pass categories to the template
            return render(request, 'notes/note_update.html', {
                'note': note,
                'error_message': error_message,
                'categories': categories,
            })
    else:
        categories = Category.objects.all()  # Pass categories to the template
        return render(request, 'notes/note_update.html', {'note': note, 'categories': categories})


# View to delete a note
def note_delete(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if request.method == "POST":
        note.delete()
        return redirect('note_list')
    return render(request, 'notes/note_delete.html', {'note': note})

class NoteViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing notes.
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
