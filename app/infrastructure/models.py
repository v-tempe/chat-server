from tortoise import fields, models


class DBUser(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True, index=True)
    password_hash = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "users"

    def __str__(self):
        return self.username


class DBChat(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, null=True)
    is_group = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    participants = fields.ManyToManyField(DBUser, related_name="chats", through="chat_users")

    class Meta:
        table = "chats"


class DBMessage(models.Model):
    id = fields.IntField(pk=True)
    chat = fields.ForeignKeyField(DBChat, related_name="messages", on_delete=fields.CASCADE)
    sender = fields.ForeignKeyField(DBUser, related_name="messages", on_delete=fields.CASCADE)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "messages"
        ordering = ["created_at"]
