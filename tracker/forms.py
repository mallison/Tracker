from django import forms

import models


class ProjectTaskForm(forms.Form):
    project = forms.ModelChoiceField(queryset=models.Project.objects.all())
    task = forms.ModelChoiceField(queryset=models.Task.objects.filter(finished=False))

    def clean(self):
        project = self.cleaned_data.get('project')
        task = self.cleaned_data.get('task')
        if project and task and task.project != project:
            raise forms.ValidationErro("Task is not valid for project")
        return self.cleaned_data


class TimeslotNotesForm(forms.Form):
    notes = forms.CharField(widget=forms.Textarea)
