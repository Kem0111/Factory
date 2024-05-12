import os

from django.core.mail import send_mail
from django.db.models.signals import pre_save
from django.dispatch import receiver
from dotenv import load_dotenv

from .models import Application

load_dotenv()


@receiver(pre_save, sender=Application)
def send_status_update(sender, instance, **kwargs):
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        pass
    else:
        if not obj.status == instance.status:
            send_mail(
                'Статус вашей заявки был обновлен',
                f'Статус вашей заявки теперь: {instance.status} '
                f'\n\nПодробнее по ссылке: http://127.0.0.1:8000/application/{obj.pk}/',
                os.getenv('EMAIL_HOST_USER'),
                [instance.user.email],
                fail_silently=False,
            )
        elif not obj.overdue and obj.overdue != instance.overdue and instance.production_time:
            send_mail(
                'Срок изготовления задерживается',
                f'Срок изготовления для заявки: http://127.0.0.1:8000/application/{obj.pk}/ задерживается до'
                f' {instance.production_time.strftime("%d.%m.%Y")}',
                os.getenv('EMAIL_HOST_USER'),
                [instance.user.email],
                fail_silently=False,
            )
