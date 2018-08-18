from django.db import models


class Task(models.Model):
    external_reference = models.CharField(max_length=255)

    project = models.ForeignKey(
        'clients.Project',
        on_delete=models.CASCADE,
        related_name='tasks',
    )

    def __str__(self):
        return f'{self.project} - {self.external_reference}'


class Project(models.Model):
    name = models.CharField(max_length=255)

    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.CASCADE,
        related_name='projects',
    )

    def __str__(self):
        return f'{self.client} - {self.name}'


class Client(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
