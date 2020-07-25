from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from petitions.models import Petition, Signature


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField('Стать', choices=(('M', 'Чоловік'), ('W', 'Жінка')), max_length=1)
    is_admin = models.BooleanField('Розришений профіль', default=False)
    location = models.CharField('Місто', max_length=20, blank=True, null=True)
    fb_link = models.URLField('Посилання на профіль в ФБ', blank=True, null=True)

    def get_user_petitions(self):

        return Petition.objects.filter(author=self.user)

    def get_user_signed_petitions(self):

        signatures = Signature.objects.filter(user=self.user)
        petitions = []

        for signature in signatures:
            petitions.append(signature.petition)

        return petitions

    def get_petitions_to_rewiew(self):

        return Petition.objects.filter(status=Petition.ON_CONSIDERATION)


# ========================================================================================== #
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Ticket(models.Model):

    name = models.CharField('Ім\'я', max_length=50, null=True)
    email = models.EmailField('Почта', max_length=50, null=True, blank=True)
    text = models.TextField('Текст', max_length=5000, null=True)
    checked = models.BooleanField('Опрацьовано', default=False)

    def __str__(self):

        return '({}) {}'.format(self.name, self.text[:150])


