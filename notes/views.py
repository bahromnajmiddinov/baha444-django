from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Note, Folder, Tag, Idea, Reminder

@login_required
def note_list(request):
    notes = Note.objects.filter(user=request.user, is_archived=False)
    folders = Folder.objects.filter(user=request.user)
    
    context = {
        'notes': notes,
        'folders': folders,
    }
    return render(request, 'notes/list.html', context)

@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    return render(request, 'notes/detail.html', {'note': note})

@login_required
def note_create(request):
    if request.method == 'POST':
        note = Note.objects.create(
            user=request.user,
            title=request.POST.get('title'),
            content=request.POST.get('content', ''),
        )
        return redirect('note_detail', pk=note.pk)
    return render(request, 'notes/create.html')
