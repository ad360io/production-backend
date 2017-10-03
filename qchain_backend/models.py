from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, DecimalValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from decimal import Decimal

AD_TYPES = (('btw', 'ban_top_wide'), ('br', 'ban_right'),
            ('popup', 'popup'), ('bl', 'ban_left'))
AD_TYPES_rev = (('ban_top_wide', 'btw'),('ban_right', 'br'),('popup', 'popup'),
         ('ban_left', 'bl'))
GENRE_CHOICES = (('Gaming', 'Gaming'), ('Movies', 'Movies'),
                 ('Auto', 'Auto'), ('Porn', 'Porn'))
MAX_DIGITS = 12
DECIMAL_PLACES = 8
NAME_LENGTH = 80
SHORT_TXT_LENGTH = 300
CHOICE_LENGTH = 15
URL_LENGTH = 200

class Agent(models.Model):
    """
    Class for agent.
    An agent is both publisher and advertiser.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(null=True)
    bio = models.CharField(max_length=SHORT_TXT_LENGTH, null=True)
    e_balance = models.DecimalField(default= Decimal('0.00000000'),
                                    max_digits=MAX_DIGITS,
                                    decimal_places=DECIMAL_PLACES,
                                    validators=[DecimalValidator(MAX_DIGITS,
                                                                 DECIMAL_PLACES)])
    x_balance = models.DecimalField(default= Decimal('0.00000000'),
                                    max_digits=MAX_DIGITS,
                                    decimal_places=DECIMAL_PLACES,
                                    validators=[DecimalValidator(MAX_DIGITS,
                                                                 DECIMAL_PLACES)])
    def __str__(self):
        return self.user.username


class Website(models.Model):
    """
    Class for website.
    Each website is owned by a user but a user may have multiple websites.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.URLField(max_length=URL_LENGTH)
    name = models.CharField(max_length=NAME_LENGTH)
    description = models.CharField(max_length=SHORT_TXT_LENGTH)
    # NOTE: USE CONSTANT VARIABLES TO REPRESENT TYPE STRINGS AS RECOMMENDED
    genres = models.CharField(
        max_length=CHOICE_LENGTH,
        choices=GENRE_CHOICES)

    def __str__(self):
        return self.name

class Adspace(models.Model):
    """
    Class for adspaces.
    An adspace is a location on the website and belongs to a website and its owner.
    """
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    name = models.CharField(max_length=NAME_LENGTH, verbose_name="Adspace Name")
    adtype = models.CharField(max_length=CHOICE_LENGTH, choices=AD_TYPES_rev,
                              verbose_name="Ad Type")
    genre = models.CharField(max_length=CHOICE_LENGTH, choices=GENRE_CHOICES)
    height = models.IntegerField()
    width = models.IntegerField()
    def __str__(self):
        return self.name



class Ad(models.Model):
    """
    Class for advertisements.
    An advertisement belongs to its (single) owner.
    """
    advertiser = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=NAME_LENGTH, verbose_name="Ad Name")
    adtype = models.CharField(max_length=CHOICE_LENGTH, choices=AD_TYPES_rev,
                              verbose_name="Ad Type")
    genre = models.CharField(max_length=CHOICE_LENGTH, choices=GENRE_CHOICES)
    content = models.URLField(max_length=URL_LENGTH)
    height = models.IntegerField()
    width = models.IntegerField()
    def __str__(self):
        return self.name


class Contract(models.Model):
    """
    Class for contract.
    This is not the actual Ethereum/NEM smart contract.
    """
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    adspace = models.ForeignKey(Adspace, on_delete=models.CASCADE)
    name = models.CharField(max_length=NAME_LENGTH)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField()
    currency = models.CharField(max_length=NAME_LENGTH, choices=(('eqc', 'EQC'),
                                                        ('xqc', 'XQC')))
    payout_cap = models.DecimalField(max_digits=MAX_DIGITS,
                                     decimal_places=DECIMAL_PLACES,
                                     validators=[MinValueValidator(0)])
    def __str__(self):
        return self.name

class Stat(models.Model):
    """
    Class for impressions of a given contract.
    """
    contract = models.ManyToManyField(Contract)
    ## When creating stats with code, we can't assign contracts because it is
    ## a many to ManyToManyField. The way to do this is to define a 'through'
    ## model and declare instances of that. See the ticket here :
    ## https://code.djangoproject.com/ticket/21763
    stat_date = models.DateField()
    impressions = models.IntegerField(unique_for_date="stat_date",
                                      validators=[MinValueValidator(0)])
    clicks = models.IntegerField(unique_for_date="stat_date",
                                 validators=[MinValueValidator(0)])
    rpm = models.DecimalField(max_digits=MAX_DIGITS,
                            #   unique_for_date=date,
                              decimal_places=DECIMAL_PLACES,
                              validators=[MinValueValidator(0),
                                          DecimalValidator(MAX_DIGITS,
                                                           DECIMAL_PLACES)])
    revenue = models.DecimalField(max_digits=MAX_DIGITS,
                                #   unique_for_date=date,
                                  decimal_places=DECIMAL_PLACES,
                                  validators=[MinValueValidator(0),
                                              DecimalValidator(MAX_DIGITS,
                                                               DECIMAL_PLACES)])
    def __str__(self):
        return "Stats for date"+str(self.stat_date)

class RequestForAdv(models.Model):
    """
    Class for request for an advertisement from a publisher.
    """
    adsp = models.ManyToManyField(Adspace)
    name = models.CharField(max_length=NAME_LENGTH)
    currency = models.CharField(max_length=4,
                                choices=(("eqc", "EQC"), ("xqc", "XQC")))
    asking_rate = models.DecimalField(max_digits=MAX_DIGITS,
                                      decimal_places=DECIMAL_PLACES,
                                      validators=[MinValueValidator(0),
                                                  DecimalValidator(MAX_DIGITS,
                                                                   DECIMAL_PLACES)])
    ask_date_from = models.DateField()
    ask_date_to = models.DateField()
    cpi = models.DecimalField(default=0,max_digits=MAX_DIGITS,
                                      decimal_places=DECIMAL_PLACES,
                                      validators=[MinValueValidator(0),
                                                  DecimalValidator(MAX_DIGITS,
                                                                   DECIMAL_PLACES)])
    cpc =  models.DecimalField(default=0,max_digits=MAX_DIGITS,
                                      decimal_places=DECIMAL_PLACES,
                                      validators=[MinValueValidator(0),
                                                  DecimalValidator(MAX_DIGITS,
                                                                   DECIMAL_PLACES)])
    msg = models.CharField(max_length=SHORT_TXT_LENGTH)

    def __str__(self):
        return self.name

    def clean(self):
        if self.ask_date_from >= self.ask_date_to:
            raise ValidationError(_('From date should preceed to date.'))

class AdListing(models.Model):
    """
    Class for storing an ad listing from an advertiser
    """
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    name = models.CharField(max_length=NAME_LENGTH)
    currency = models.CharField(max_length=4,
                                choices=(("eqc", "EQC"), ("xqc", "XQC")))
    asking_rate = models.DecimalField(max_digits=MAX_DIGITS,
                                      decimal_places=DECIMAL_PLACES,
                                      validators=[MinValueValidator(0),
                                                  DecimalValidator(MAX_DIGITS,
                                                                   DECIMAL_PLACES)])
    ask_date_from = models.DateField()
    ask_date_to = models.DateField()
    cpi = models.DecimalField(default=0,max_digits=MAX_DIGITS,
                                      decimal_places=DECIMAL_PLACES,
                                      validators=[MinValueValidator(0),
                                                  DecimalValidator(MAX_DIGITS,
                                                                   DECIMAL_PLACES)])
    cpc =  models.DecimalField(default=0,max_digits=MAX_DIGITS,
                                      decimal_places=DECIMAL_PLACES,
                                      validators=[MinValueValidator(0),
                                                  DecimalValidator(MAX_DIGITS,
                                                                   DECIMAL_PLACES)])
    msg = models.CharField(max_length=SHORT_TXT_LENGTH)
    def __str__(self):
        return self.name

    def clean(self):
        if self.ask_date_from >= self.ask_date_to:
            raise ValidationError(_('From date should preceed to date.'))
