import datetime

from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Task(models.Model):
    project = models.ForeignKey(Project, related_name="tasks")
    name = models.CharField(max_length=50)
    finished = models.BooleanField()

    def __unicode__(self):
        return u'%s: %s' % (self.project.name, self.name)

    def cumulative_time(self):
        time = 0
        for chunk in self.chunks.filter(end__isnull=False):
            time += chunk.duration()
        return time


class Chunk(models.Model):
    task = models.ForeignKey(Task, related_name="chunks")
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    notes = models.TextField()

    def __unicode__(self):
        return u'%s: %s' % (self.task.name, self.duration())
    
    def finish(self):
        self.end = datetime.datetime.now()
        self.save()

    def ordinal(self):
        return self.task.chunks.filter(start__lte=self.start).count()

    def duration(self):
        return self.end and (self.end - self.start).seconds / 60
