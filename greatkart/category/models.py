from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)                         # Add slug field if we want to display slugs.Now edit in admin.py file also.
    description = models.TextField(max_length=100, blank=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)

    # when we register the model to admin then it automatically add 's' to the model name so
    # we dont want such typos so we use these two lines. 
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    # This function get the particular url of that category
    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.category_name