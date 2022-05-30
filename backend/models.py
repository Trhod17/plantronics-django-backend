from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MinLengthValidator, MaxValueValidator, MaxLengthValidator, FileExtensionValidator

class Plant(models.Model):
    plant_name = models.CharField(max_length=255, validators=[MaxLengthValidator(255), MinLengthValidator(3)])
    plant_latin_name = models.CharField(max_length=255, validators=[MaxLengthValidator(255), MinLengthValidator(3)])
    plant_image = models.ImageField(upload_to='images/', blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg', 'webp'])])
    plant_description = models.CharField(max_length=1000, null=True,
                                         blank=True)
    family = models.ForeignKey('backend.Family', on_delete=models.RESTRICT)
    genus = models.ForeignKey(
        'backend.genus', on_delete=models.RESTRICT)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = ('Plant')

    def __str__(self):
        return self.plant_name

    def get_absolute_url(self):
        return reverse('', kwargs={'pk': self.pk})


class Genus(models.Model):

    genus = models.CharField(max_length=255, primary_key=True, )
    genus_description = models.CharField(max_length=1000, null=True,
                                         blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = ('genus')
        verbose_name_plural = ('genus')

    def __str__(self):
        return self.genus

    def get_absolute_url(self):
        return reverse('', kwargs={'pk': self.pk})


class Family(models.Model):

    family = models.CharField(max_length=255, primary_key=True, validators=[MaxLengthValidator(255), MinLengthValidator(3)])
    family_description = models.CharField(max_length=1000, null=True,
                                          blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = ('Family')
        verbose_name_plural = ('Families')

    def __str__(self):
        return self.family

    def get_absolute_url(self):
        return reverse('', kwargs={'pk': self.pk})


class Info(models.Model):

    class Seasons(models.TextChoices):
        WINTER = 'W', ('Winter')
        SPRING = 'SP', ('Spring')
        SUMMER = 'SU', ('Summer')
        AUTUMN = 'AU', ('Autumn')
        __empty__ = ('(Unknown)')

    class TimeFrames(models.TextChoices):
        DAILY = 'D', ('Daily')
        ADAY = 'AD', ('Alternating Days (Every Other Day)')
        WEEKLY = 'W', ('Weekly')
        FORTNIGHTLY = 'F', ('Fort Nightly')
        MONTHLY = 'M', ('Monthly')
        __empty__ = ('(Unknown)')

    class Climates(models.TextChoices):
        ALL = 'A', ('All')
        ALL2 = 'A2', ('All Expect Polar')
        TROPTOSUBTROP = 'TTST', ('Sub Tropical to Tropical')
        SUBTROPANDTEMP = 'STAT', ('Temperate to Subtropical')
        POLARTOTEMPERATE = 'PTT', ('Polar to Temperate')
        TROPICAL = 'T', ('Tropical')
        SUBTROPICAL = 'ST', ('Sub-Tropical')
        TEMPERATE = 'TE', ('Temperate')
        POLAR = 'P', ('Polar or SubPolar')

    class SunPreferences(models.TextChoices):
        FULLSUN = 'FS', ('Full Sun')
        LIGHTSHADE = 'LS', ('''Light Shade
                             (Between 3 and 5 hours of direct sun)''')
        PARTIALSHADE = 'PS', ('Partial Shade (Receives 2 hours of sun a day)')
        FULLSHADE = 'FSH', ('Full Shade (Less then an hour of sunlight a day)')
        DENSESHADE = 'DS', ('''Dense Shade (No direct sun light and little
                             indirect sun light''')
        __empty__ = ('(Unknown)')

    plant = models.ForeignKey(
        "backend.Plant", on_delete=models.CASCADE, null=True)
    sun_preference = models.CharField(max_length=3,
                                      choices=SunPreferences.choices,
                                      default=SunPreferences.FULLSUN)
    climate = models.CharField(
        max_length=5, choices=Climates.choices, default=Climates.TROPICAL,
        verbose_name='Climate Zones')
    season = models.CharField(
        max_length=3, choices=Seasons.choices, default=Seasons.SUMMER,
        verbose_name=('Planting Season'))
    time_frame = models.CharField(max_length=3, choices=TimeFrames.choices,
                                  default=TimeFrames.DAILY,
                                  verbose_name=('Watering Schedule'))
    info_description = models.CharField(max_length=1000, null=True,
                                        blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = ('Info')
        verbose_name_plural = ('Info')

    def __str__(self):
        return 'info'

    def get_absolute_url(self):
        return reverse('', kwargs={'pk': self.pk})


class SoilPreference(models.Model):

    class SoilPreference(models.TextChoices):
        ANY = 'AN', ('Any Soil')
        CLAY = 'CL', ('Clay')
        SANDY = 'SA', ('Sandy')
        SILTY = 'SI', ('Silty')
        PEATY = 'PE', ('Peaty')
        CHALKY = 'CH', ('Chalky')
        LOAMY = 'LO', ('Loamy')
        __empty__ = ('(Unknown)')

    plants = models.ForeignKey(
        "backend.Plant", on_delete=models.CASCADE, null=True)
    preference = models.CharField(max_length=3,
                                  choices=SoilPreference.choices,
                                  default=SoilPreference.__empty__)
    soil_description = models.CharField(max_length=500, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = ('Soil Preference')
        verbose_name_plural = ('Soil Preferences')

    def __str__(self):
        return self.preference

    def get_absolute_url(self):
        return reverse('', kwargs={'pk': self.pk})


class UserPlant(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=200, unique=False, null=True)
    user = models.ForeignKey(
        User, to_field="username", null=False, on_delete=models.CASCADE)
    plant = models.ForeignKey(
        Plant, null=False, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ('User Plant')
        verbose_name_plural = ('Users Plants')

    def __str__(self):
        return 'userplant'

    def get_absolute_url(self):
        return reverse('', kwargs={'pk': self.pk})


class Edible(models.Model):

    class Edibility(models.TextChoices):
        YES = 'Y', ('Yes')
        NO = 'N', ('No')
        NOT_APPLICABLE = 'NA', ('Not Applicable')
        PARTIALLY = 'P', ('Partially Edible')
        REQUIRES_PREP = 'RP', ('Requires Preperation')
        PARTIALY_AND_REQUIRES_PREP = 'PRP', (
            'Partially Edible But Requires Preperation')
        __empty__ = ('(Unknown)')

    plant = models.ForeignKey(
        "backend.plant", on_delete=models.CASCADE)
    is_fruit_edible = models.CharField(choices=Edibility.choices,
                                       default=Edibility.__empty__,
                                       max_length=3)
    fruit_image = models.ImageField(upload_to='images/', blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg', 'webp'])])
    are_leaves_edible = models.CharField(choices=Edibility.choices,
                                         default=Edibility.__empty__,
                                         max_length=3)
    leaf_image = models.ImageField(upload_to='images/', blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg', 'webp'])])
    are_roots_edible = models.CharField(choices=Edibility.choices,
                                        default=Edibility.__empty__,
                                        max_length=3)
    root_image = models.ImageField(upload_to='images/', blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg', 'webp'])])
    are_flowers_edible = models.CharField(choices=Edibility.choices,
                                          default=Edibility.__empty__,
                                          max_length=3)
    flower_image = models.ImageField(upload_to='images/', blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg', 'webp'])])
    are_seeds_edible = models.CharField(choices=Edibility.choices,
                                        default=Edibility.__empty__,
                                        max_length=3)
    seed_image = models.ImageField(upload_to='images/', blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg', 'webp'])])
    edible_description = models.CharField(max_length=1000)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = ('Edible')

    def __str__(self):
        return 'edible'

    def get_absolute_url(self):
        return reverse('', kwargs={'pk': self.pk})
