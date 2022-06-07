import json
from django_celery_beat.models import PeriodicTask, IntervalSchedule


scheduleTwoHours, createdTwoHours = IntervalSchedule.objects.get_or_create(
    every=5,
    period=IntervalSchedule.MINUTES,
)


def update_domain_two_hours(domainId):
    taskName = "Updating " + str(domainId) + " CVEs"
    PeriodicTask.objects.create(
        interval=scheduleTwoHours,  # we created this above.
        name=taskName,  # simply describes this periodic task.
        task="core.tasks.async_update_domain_cve",  # name of task.
        args=json.dumps([domainId]),
    )
    print("Task Added for : " + str(domainId))
