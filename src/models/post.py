from datetime import datetime
import mongoengine as me
from bson import ObjectId

from src.models.user import User


class Comments(me.Document):
    """
    Comments class
    """
    user_id = me.ObjectIdField(required=True)
    comment = me.StringField(required=True)
    created_at = me.DateTimeField(required=True)
    updated_at = me.DateTimeField(required=True)


class Post(me.Document):
    _id = me.ObjectIdField(default=ObjectId)
    content = me.StringField(required=True)
    photo = me.URLField()
    creator = me.ReferenceField(User)
    likes = me.ListField(me.ReferenceField(User), default=[])
    comments = me.ListField(Comments, default=[])
    created_at = me.DateTimeField(default=datetime.utcnow)
    updated_at = me.DateTimeField(default=datetime.utcnow)

    def to_json(self):
        return {
            "_id": str(self._id),
            "content": self.content,
            "photo": self.photo,
            "creator": str(self.creator._id),
            "photo": self.photo,
            "likes": [str(l._id) for l in self.likes],
            "comments": [str(c._id) for c in self.comments]
        }
