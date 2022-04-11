import mongoengine as me
from bson import ObjectId


class User(me.Document):
    _id = me.ObjectIdField(default=ObjectId)
    firstName = me.StringField(required=True)
    lastName = me.StringField(required=True)
    username = me.StringField(required=True, unique=True, min_length=3)
    password = me.StringField(required=True, min_length=6)
    email = me.EmailField(required=True, unique=True)
    photo = me.URLField()
    following = me.ListField(me.ReferenceField('self'), default=[])
    followers = me.ListField(me.ReferenceField('self'), default=[])
    created_at = me.DateTimeField(required=True)
    updated_at = me.DateTimeField(required=True)

    def to_json(self):
        return {
            "_id": str(self._id),
            "firstName": self.firstName,
            "lastName": self.lastName,
            "username": self.username,
            "email": self.email,
            "photo": self.photo,
            "following": [str(f._id) for f in self.following],
            "followers": [str(f._id) for f in self.followers]
        }
