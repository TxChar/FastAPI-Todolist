from mongoengine import Document, StringField, DateTimeField, ListField, ReferenceField
import datetime


# โมเดลสำหรับ Sub-Task (เป็นเอกเทศ)
class SubTask(Document):
    name = StringField(required=True, max_length=200)
    status = StringField(
        required=True, choices=["Pending", "In Progress", "Done"], default="Pending"
    )
    created_date = DateTimeField(default=datetime.datetime.now(datetime.timezone.utc))
    updated_date = DateTimeField(default=datetime.datetime.now(datetime.timezone.utc))
    expected_date = DateTimeField()

    meta = {"collection": "sub_tasks"}


# โมเดลสำหรับ Main Task (อ้างอิง Sub-Tasks)
class MainTask(Document):
    name = StringField(required=True, max_length=200)
    status = StringField(
        required=True, choices=["Pending", "In Progress", "Done"], default="Pending"
    )
    created_date = DateTimeField(default=datetime.datetime.now(datetime.timezone.utc))
    updated_date = DateTimeField(default=datetime.datetime.now(datetime.timezone.utc))
    expected_date = DateTimeField()

    # ใช้ ReferenceField เพื่อเชื่อมโยงกับ Sub-Task (1 Main Task มีหลาย Sub-Tasks)
    sub_tasks = ListField(
        ReferenceField(SubTask, reverse_delete_rule=2)
    )  # CASCADE delete

    meta = {"collection": "tasks"}
