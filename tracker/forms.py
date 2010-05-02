from django import forms

import models


class ProjectTaskForm(forms.Form):
    project = forms.ModelChoiceField(
        queryset=models.Project.objects.order_by('name'))
    task = forms.ModelChoiceField(
        queryset=models.Task.objects.filter(finished=False).
                     order_by('project__name', 'name'),
        required=False)
    new_task = forms.CharField(required=False)

    def clean(self):
        project = self.cleaned_data.get('project')
        task = self.cleaned_data.get('task')
        if project and task and task.project != project:
            raise forms.ValidationError("Task is not valid for project")
        return self.cleaned_data


class ChunkNotesForm(forms.Form):
    notes = forms.CharField(widget=forms.Textarea, required=False)
