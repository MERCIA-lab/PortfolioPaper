import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Portfolio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='portfolio')
    full_name = models.CharField(max_length=150)
    job_title = models.CharField(max_length=150, blank=True)
    summary = models.TextField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    location = models.CharField(max_length=150, blank=True)
    photo = models.ImageField(upload_to='portfolio/photos/', blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.full_name or self.user.username)
            slug = base_slug
            counter = 1
            while Portfolio.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name or self.user.email


class Education(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name='education', on_delete=models.CASCADE)
    school = models.CharField(max_length=150)
    degree = models.CharField(max_length=150)
    start_year = models.CharField(max_length=20, blank=True)
    end_year = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f'{self.school} - {self.degree}'


class Experience(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name='experience', on_delete=models.CASCADE)
    company = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    start_date = models.CharField(max_length=30, blank=True)
    end_date = models.CharField(max_length=30, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.role} @ {self.company}'


class Skill(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name='skills', on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    level = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.name


class Project(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name='projects', on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True)

    def __str__(self):
        return self.title
