from django.db import models

# a model for one time content, which will be a singleton model (only one instance will exist)
class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1  # Always set the primary key to 1
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
    
class Hero(SingletonModel):
    title = models.CharField(max_length=150) 
    title_ar = models.CharField(max_length=150, null=True, blank=True)
    description = models.TextField()
    description_ar = models.TextField(null=True, blank=True)
    seekers_count = models.IntegerField(default=0)
    
class HeroImage(models.Model):
    hero = models.ForeignKey(Hero, related_name="images", on_delete=models.CASCADE) 
    image = models.ImageField(upload_to='hero_images/')
    
class FAQ(models.Model):
    question = models.CharField(max_length=255)
    question_ar = models.CharField(max_length=255, null=True, blank=True)
    answer = models.TextField()
    answer_ar = models.TextField(null=True, blank=True)