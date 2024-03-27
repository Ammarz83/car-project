from django.db import models
from slugify import slugify
from django.contrib.auth import get_user_model

User = get_user_model()


class Brand(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.DO_NOTHING
    )
    title = models.CharField(max_length=70)            #
    country = models.CharField(max_length=70)
    slug = models.SlugField(primary_key=True, blank=True,max_length=120)
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)   
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.title}'
    
    class Meta:
        verbose_name = 'Car'
        verbose_name_plural = 'Car'

class Car(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.DO_NOTHING
    )
    model = models.CharField(max_length=50)
    brand = models.ForeignKey(
        to=Brand,
        on_delete=models.DO_NOTHING
    )
    year = models.CharField(max_length=50)
    about = models.TextField()
    image = models.ImageField(upload_to='brand_images')
    slug = models.SlugField(primary_key=True, blank=True,max_length=120)
    name = models.CharField(max_length=101, blank=True)
    

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.brand + ' ' + self.model
        if not self.slug:
            self.slug = slugify(self.model) + '_' + slugify(self.brand)
        return super().save(*args, **kwargs)

    def __str__(self) :
        return f'{self.brand} {self.brand}'
    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'
        

