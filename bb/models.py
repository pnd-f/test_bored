from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q


class Activity(models.Model):
    activity = models.CharField(max_length=255)
    activity_type = models.CharField(max_length=120)
    participants = models.IntegerField()
    price = models.FloatField()
    link = models.URLField(blank=True, null=True)
    key = models.CharField(max_length=50)
    accessibility = models.CharField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )
    # new fields
    availability = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    duration = models.CharField(blank=True, null=True)
    kidFriendly = models.BooleanField(default=False)

    class Meta:
        constraints = (
            # for checking in the DB
            CheckConstraint(
                check=Q(availability__gte=0.0) &
                      Q(availability__lte=1.0),
                name='myfloat_range'),
        )

    def __str__(self):
        return f'{self.activity_type}: {self.activity}'

    def __repr__(self):
        return self.__str__()
