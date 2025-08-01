from celery_worker import celery
@celery.task
def send_email(request):
    print(f"data: {request}")
    print(f"Sending email for order {request}")
    return "sending email"

