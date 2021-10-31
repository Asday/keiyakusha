from django.db import models


class Task(models.Model):
    external_reference = models.CharField(max_length=255)

    project = models.ForeignKey(
        'clients.Project',
        on_delete=models.CASCADE,
        related_name='tasks',
    )

    class Meta:
        unique_together = ('external_reference', 'project')

    def __str__(self):
        # TODO: Remove lookups from string methods.
        return f'{self.project} - {self.external_reference}'


class Project(models.Model):
    name = models.CharField(max_length=255)

    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.CASCADE,
        related_name='projects',
    )

    class Meta:
        unique_together = ('name', 'client')

    def __str__(self):
        # TODO: Remove lookups from string methods.
        return f'{self.client} - {self.name}'


class Client(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
