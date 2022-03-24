from django.db import models
from datetime import datetime
from cloudinary.models import CloudinaryField
from django.template.defaultfilters import slugify

class Brand(models.Model):
    title = models.CharField(max_length=200, unique=True)
    is_featured = models.BooleanField(default=False)
    logo=models.CharField(max_length=200)
   
    def __str__(self):
        return self.title

class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    title = models.CharField(max_length=200, unique=True)
    parent = models.ForeignKey('self',related_name='children', on_delete=models.CASCADE ,blank=True,null=True)
    is_featured = models.BooleanField(default=False)
    photo = CloudinaryField('Image', overwrite=True, format="jpg")
    slug = models.SlugField(max_length=255, null=True, blank=True)
    description = models.TextField(max_length=200)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/%s/' % (self.slug)

    def save(self, *args, **kwargs):
        to_assign = slugify(self.title)
        if Category.objects.filter(slug=to_assign).exists():
            to_assign = to_assign+str(Category.objects.all().count())
        self.slug = to_assign
        super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    
    parent=models.ForeignKey('self', related_name='variants', on_delete=models.CASCADE,blank=True,null=True)
    
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    compare_price = models.DecimalField(max_digits=6, decimal_places=2)
    is_featured = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(default=datetime.now)

    slug = models.SlugField(max_length=255, null=True, blank=True)

    num_visits = models.IntegerField(default=0)
    last_visit = models.DateTimeField(blank=True, null=True)
    sold = models.IntegerField(default=0)
    photo = CloudinaryField('Image', overwrite=True, format="jpg")

    class Meta:
        ordering = ('-date_added',)

    def get_category(self):
        return self.category.title

    def get_absolute_url(self):
        return '/%s/%s/' % (self.category.slug, self.slug)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        to_assign = slugify(self.title)
        if Product.objects.filter(slug=to_assign).exists():
            to_assign = to_assign+str(Product.objects.all().count())
        self.slug = to_assign
        super().save(*args, **kwargs)