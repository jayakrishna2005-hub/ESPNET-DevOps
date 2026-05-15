from django.db.models.signals import post_save
from django.dispatch import receiver
from teams.models import Application
from scrims.models import Scrim
from .models import Notification

@receiver(post_save, sender=Application)
def notify_application_update(sender, instance, created, **kwargs):
    if created:
        # Notify team admins
        team = instance.post.team
        for membership in team.members.filter(role__in=['captain', 'coach']):
            Notification.objects.create(
                user=membership.player.user,
                message=f"New application for {instance.post.title}: {instance.player.user.username}",
                link=f"/teams/{team.pk}/dashboard/"
            )
    else:
        # Status changed (accepted/rejected)
        if instance.status in ['accepted', 'rejected']:
            Notification.objects.create(
                user=instance.player.user,
                message=f"Your application to {instance.post.team.name} was {instance.status}."
            )

@receiver(post_save, sender=Scrim)
def notify_scrim_update(sender, instance, created, **kwargs):
    if not created:
        if instance.status == 'scheduled':
            for membership in instance.requester.members.all():
                Notification.objects.create(
                    user=membership.player.user,
                    message=f"Scrim scheduled against {instance.opponent.name} on {instance.date_time.strftime('%Y-%m-%d')}"
                )
        elif instance.status == 'completed':
            for membership in instance.requester.members.all() | instance.opponent.members.all():
                Notification.objects.create(
                    user=membership.player.user,
                    message=f"Match results for scrim against {instance.opponent.name} have been recorded."
                )
