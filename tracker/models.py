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
        return sum([s.end - s.start for s in self.timeslots.all()])


class Timeslot(models.Model):
    task = models.ForeignKey(Task, related_name="timeslots")
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    notes = models.TextField()

    def __unicode__(self):
        return u'%s: %s' % (self.task.name, end - start)
    
    def ordinal(self):
        return self.task.timeslots.filter(start__lte=self.start).count()
