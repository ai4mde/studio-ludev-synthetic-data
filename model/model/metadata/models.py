from django.db import models

class Project(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

class System(models.Model):
    id = models.UUIDField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()

class Classifier(models.Model):
    id = models.UUIDField(primary_key=True)
    system = models.ForeignKey(System, on_delete=models.CASCADE)
    type = models.CharField()
    data = models.JSONField()

class Relation(models.Model):
    id = models.UUIDField(primary_key=True)
    data = models.JSONField()
    type = models.CharField()
    source = models.ForeignKey(Classifier, related_name="relations_to", on_delete=models.CASCADE)
    target = models.ForeignKey(Classifier, related_name="relations_from", on_delete=models.CASCADE)
