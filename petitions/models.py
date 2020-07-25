from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import reverse
import datetime


class Petition(models.Model):

    ACTIVE = 'ACTIVE'  # the collection of signatures
    ON_CONSIDERATION = 'ON_CONSIDERATION'  # on ON_CONSIDERATION
    ANSWERED = 'ANSWERED'  # has answer
    REJECTED = 'REJECTED'  # not supported

    PETITION_STATUSES = (
        (ACTIVE, 'Збір підписів'),
        (ON_CONSIDERATION, 'На розгляді'),
        (ANSWERED, 'З відповіддю'),
        (REJECTED, 'Не пітримано'))

    title = models.CharField(verbose_name='Заголовок', max_length=150)
    text = models.TextField(verbose_name='Текст', max_length=10000)
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE, related_name='petition_author')
    publication_date = models.DateTimeField(verbose_name='дата публікації', auto_now_add=True)
    to_date = models.DateTimeField(verbose_name='Кінцева дата',
                                   default=datetime.datetime.now()+datetime.timedelta(days=settings.PETITION_DAYS_LEFT))
    answer = models.TextField(verbose_name='Відповідь', max_length=10000, blank=True, null=True)
    responder = models.ForeignKey(User, verbose_name='Відповідач', null=True, blank=True, on_delete=models.CASCADE,
                                  related_name='petition_responder')
    response_date = models.DateTimeField(verbose_name='Дата відповіді', null=True, blank=True)
    status = models.CharField(verbose_name='Статус', choices=PETITION_STATUSES, max_length=20, default=ACTIVE)

    @property
    def is_active(self):
        return self.status == self.ACTIVE

    @property
    def is_answered(self):
        return self.status == self.ANSWERED

    @property
    def is_rejected(self):
        return self.status == self.REJECTED

    @property
    def is_on_consideration(self):
        return self.status == self.ON_CONSIDERATION

    def user_signed(self, user):
        return Signature.objects.filter(petition=self, user=user).exists()

    def get_signatures(self):
        return Signature.objects.filter(petition=self).order_by('date')

    @property
    def get_signatures_count(self):
        return Signature.objects.filter(petition=self).count()

    def __str__(self):
        return '%s (%d%%)' % (self.title, self.get_progress_percentages)

    def sign(self, user):
        
        Signature(user=user, petition=self).save()

        if not self.get_signatures_left:
            self.status = self.ON_CONSIDERATION
            self.save()

    @property
    def get_progress_percentages(self):
        return int(self.get_signatures_count / settings.PETITION_SIGNATURES * 100)

    @property
    def get_signatures_left(self):
        return settings.PETITION_SIGNATURES - self.get_signatures_count

    def get_absolute_url(self):
        return reverse('petition', args=[self.id])

    def get_end_date(self):
        return self.to_date

    def get_signed_petitions(self, user):

        return Signature.objects.filter(user=user).sort_by('date')

    def get_days_to_end(self):

        delta_dates = self.to_date.date() - datetime.date.today()

        if delta_dates.days > 0:
            return delta_dates.days
        return 0

    def get_status(self):

        return dict(self.PETITION_STATUSES).get(self.status, '-')


class Signature(models.Model):

    petition = models.ForeignKey(Petition, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата підписання')

    def __str__(self):
        return '%s (%s)' % (self.petition.title, self.user.get_full_name())
