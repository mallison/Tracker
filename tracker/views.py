import datetime

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response


# local app imports
import forms
import models


def start_tracker(request):
    misc = models.Task.objects.get(name='misc')
    timeslot = models.Timeslot.objects.create(task=misc,
                                              start=datetime.datetime.now())
    return HttpResponseRedirect(reverse('tracker-track',
                                        args=(timeslot.pk,)))


def tracker(request, timeslot_id):
    timeslot = get_object_or_404(models.Timeslot, pk=timeslot_id)
    if request.method == 'POST':
        task_form = forms.ProjectTaskForm(request.POST)
        notes_form = forms.TimeslotNotesForm(request.POST)
        if request.POST.has_key('save') and notes_form.is_valid():
            timeslot.notes = notes_form.cleaned_data['notes']
            timeslot.save()
            return HttpResponseRedirect(reverse('tracker-track',
                                                args=(timeslot.pk,)))
        elif request.POST.has_key('new') and notes_form.is_valid():
            timeslot.notes = notes_form.cleaned_data['notes']
            timeslot.finish()
            new_timeslot = models.Timeslot.objects.create(
                start=datetime.datetime.now(),
                task=timeslot.task)
            return HttpResponseRedirect(reverse('tracker-track',
                                                args=(new_timeslot.pk,)))
        elif request.POST.has_key('stop') and notes_form.is_valid():
            timeslot.notes = notes_form.cleaned_data['notes']
            timeslot.finish()
            misc_task = models.Task.objects.get(name='misc')
            new_timeslot = models.Timeslot.objects.create(
                start=datetime.datetime.now(),
                task=misc_task)
            return HttpResponseRedirect(reverse('tracker-track',
                                                args=(new_timeslot.pk,)))
        elif request.POST.has_key('finish') and notes_form.is_valid():
            timeslot.notes = notes_form.cleaned_data['notes']
            timeslot.finish()
            timeslot.task.finished = True
            timeslow.task.save()
            misc_task = models.Task.objects.get(name='misc')
            new_timeslot = models.Timeslot.objects.create(
                start=datetime.datetime.now(),
                task=misc.task)
            return HttpResponseRedirect(reverse('tracker-track',
                                                args=(new_timeslot.pk,)))
        elif (request.POST.has_key('switch') and 
              task_form.is_valid() and 
              notes_form.is_valid()):
            timeslot.notes = notes_form.cleaned_data['notes']
            timeslot.end = datetime.datetime.now()
            timeslot.save()
            new_task = task_form.cleaned_data['task']
            new_timeslot = models.Timeslot.objects.create(
                start=datetime.datetime.now(),
                task=new_task)
            return HttpResponseRedirect(reverse('tracker-track',
                                                args=(new_timeslot.pk,)))
    else:
        task_form = forms.ProjectTaskForm()
        notes_form = forms.TimeslotNotesForm(initial={'notes': timeslot.notes})
    print timeslot.task.cumulative_time()
    return render_to_response(
        'tracker/tracker.html',
        {'task_form': task_form,
         'timeslot': timeslot,
         'timeslots': models.Timeslot.objects.
             exclude(pk=timeslot.pk).
             order_by('-start'),
         'notes_form': notes_form})
