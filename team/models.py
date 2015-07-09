from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save


class TeamManager(models.Manager):
    def create_team(self, creator, name):
        return self.create(creator=creator, name=name)


class Team(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     through='Membership',
                                     through_fields=('team', 'user',)
                                     )
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='creator')

    objects = TeamManager()

    def invite(self, user, inviter):
        return Membership.objects.create(user=user, team=self, status=Membership.INVITED, role=Membership.MEMBER, inviter=inviter, )

    def apply(self, user):
        return Membership.objects.create(user=user, team=self, status=Membership.APPLIED, role=Membership.MEMBER, )

    def __unicode__(self):
        return self.name


class Membership(models.Model):
    APPLIED, INVITED, ACCEPTED, REJECTED = range(4)
    STATUS_CHOICES = (
        (APPLIED, u'applied'),
        (INVITED, u'invited'),
        (ACCEPTED, u'accepted'),
        (REJECTED, u'rejected'),
    )

    CREATOR, ADMIN, MEMBER = range(3)
    ROLE_CHOICES = (
        (CREATOR, u'creator'),
        (ADMIN, u'admin'),
        (MEMBER, u'member'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    team = models.ForeignKey(Team)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES)
    role = models.IntegerField(choices=ROLE_CHOICES)
    inviter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="inviter", default=0)

    class Meta:
        unique_together = ('user', 'team',)


@receiver(post_save, sender=Team)
def autocreate_team_creator(sender, **kwargs):
    print("Request finished!")
    # Membership.objects.create(team=sender, user=sender.creator, status=Membership.ACCEPTED, role=Membership.CREATOR)
