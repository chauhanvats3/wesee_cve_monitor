import json
from django_celery_beat.models import PeriodicTask, IntervalSchedule


scheduleTwoHours, createdTwoHours = IntervalSchedule.objects.get_or_create(
    every=2,
    period=IntervalSchedule.HOURS,
)
scheduleFourHours, createdFourHours = IntervalSchedule.objects.get_or_create(
    every=4,
    period=IntervalSchedule.HOURS,
)
scheduleSixHours, createdSixHours = IntervalSchedule.objects.get_or_create(
    every=6,
    period=IntervalSchedule.HOURS,
)
scheduleEightHours, createdEightHours = IntervalSchedule.objects.get_or_create(
    every=8,
    period=IntervalSchedule.HOURS,
)
scheduleTenHours, createdTenHours = IntervalSchedule.objects.get_or_create(
    every=10,
    period=IntervalSchedule.HOURS,
)
scheduleTwelveHours, createdTwelveHours = IntervalSchedule.objects.get_or_create(
    every=12,
    period=IntervalSchedule.HOURS,
)


def periodic_update_domain_CVEs(domainId, time, domainName):
    newInterval = None
    if time == 2:
        newInterval = scheduleTwoHours
    elif time == 4:
        newInterval = scheduleFourHours
    elif time == 6:
        newInterval = scheduleSixHours
    elif time == 8:
        newInterval = scheduleEightHours
    elif time == 10:
        newInterval = scheduleTenHours
    elif time == 12:
        newInterval = scheduleTwelveHours

    taskName = f"Updating {str(domainId)} : {domainName}  CVEs"

    PeriodicTask.objects.create(
        interval=newInterval,
        name=taskName,
        task="core.tasks.async_update_domain_cve",
        args=json.dumps([domainId]),
    )

    print("Task Added for : " + str(domainId))
