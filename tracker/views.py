import datetime

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response


# local app imports
import forms
import models


def start_tracker(request):
    misc = models.Task.objects.get(name='misc')
    chunk = models.Chunk.objects.create(task=misc,
                                              start=datetime.datetime.now())
    return HttpResponseRedirect(reverse('tracker-track',
                                        args=(chunk.pk,)))


def tracker(request, chunk_id):
    chunk = get_object_or_404(models.Chunk, pk=chunk_id)
    if request.method == 'POST':
        task_form = forms.ProjectTaskForm(request.POST)
        notes_form = forms.ChunkNotesForm(request.POST)
        if request.POST.has_key('save') and notes_form.is_valid():
            chunk.notes = notes_form.cleaned_data['notes']
            chunk.save()
            return HttpResponseRedirect(reverse('tracker-track',
                                                args=(chunk.pk,)))
        elif request.POST.has_key('new') and notes_form.is_valid():
            chunk.notes = notes_form.cleaned_data['notes']
            chunk.finish()
            new_chunk = models.Chunk.objects.create(
                start=datetime.datetime.now(),
                task=chunk.task)
            return HttpResponseRedirect(reverse('tracker-track',
                                                args=(new_chunk.pk,)))
        elif request.POST.has_key('stop') and notes_form.is_valid():
            chunk.notes = notes_form.cleaned_data['notes']
            chunk.finish()
            misc_task = models.Task.objects.get(name='misc')
            new_chunk = models.Chunk.objects.create(
                start=datetime.datetime.now(),
                task=misc_task)
            return HttpResponseRedirect(reverse('tracker-track',
                                                args=(new_chunk.pk,)))
        elif request.POST.has_key('finish') and notes_form.is_valid():
            chunk.notes = notes_form.cleaned_data['notes']
            chunk.finish()
            chunk.task.finished = True
            timeslow.task.save()
            misc_task = models.Task.objects.get(name='misc')
            new_chunk = models.Chunk.objects.create(
                start=datetime.datetime.now(),
                task=misc.task)
            return HttpResponseRedirect(reverse('tracker-track',
                                                args=(new_chunk.pk,)))
        elif (request.POST.has_key('switch') and 
              task_form.is_valid() and 
              notes_form.is_valid()):
            chunk.notes = notes_form.cleaned_data['notes']
            chunk.end = datetime.datetime.now()
            chunk.save()
            new_task = task_form.cleaned_data['task']
            new_chunk = models.Chunk.objects.create(
                start=datetime.datetime.now(),
                task=new_task)
            return HttpResponseRedirect(reverse('tracker-track',
                                                args=(new_chunk.pk,)))
    else:
        task_form = forms.ProjectTaskForm()
        notes_form = forms.ChunkNotesForm(initial={'notes': chunk.notes})
    print chunk.task.cumulative_time()
    return render_to_response(
        'tracker/tracker.html',
        {'task_form': task_form,
         'chunk': chunk,
         'chunks': models.Chunk.objects.
             exclude(pk=chunk.pk).
             order_by('-start'),
         'notes_form': notes_form})
