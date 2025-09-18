from mongoengine import Document, StringField, IntField, FloatField, URLField, BooleanField


class Activity(Document):
    activity = StringField(max_length=255, required=True)
    activity_type = StringField(max_length=120, required=True)
    participants = IntField(required=True)
    price = FloatField(required=True)
    link = URLField()
    key = StringField(max_length=50, required=True)
    accessibility = FloatField(min_value=0.0, max_value=1.0, required=True)
    # new fields
    availability = FloatField(min_value=0.0, max_value=1.0)
    duration = StringField()
    kidFriendly = BooleanField(default=False)

    meta = {
        'collection': 'activities',
        'indexes': ['activity_type', 'participants']
    }

    def __str__(self):
        return f'{self.activity_type}: {self.activity}'

    def __repr__(self):
        return self.__str__()
