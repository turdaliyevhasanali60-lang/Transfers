from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Season(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Club(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='clubs',null=True, blank=True)
    president = models.CharField(max_length=255, null=True, blank=True)
    found_date = models.DateField(null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    coach = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=255)
    number = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])
    position = models.CharField(max_length=255, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    price = models.FloatField(validators=[MinValueValidator(0)])
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Transfer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    old_club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='export_transfers')
    new_club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='import_transfers')
    price = models.FloatField(validators=[MinValueValidator(0)], null=True, blank=True)
    price_tft = models.FloatField(verbose_name="tft.com Price", validators=[MinValueValidator(0)], null=True, blank=True)
    created_at = models.DateField()
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    def __str__(self):
        return f"Transfer: {self.old_club} to {self.new_club}"