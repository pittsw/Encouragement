from django.db import models

# Create your models here.from django.db import models

class ShujaaOutgoing(models.Model):

    target = models.CharField(max_length=50)

    content = models.CharField(max_length=480)

    def __unicode__(self):
        return '"{cont}" >> {tar}'.format(cont=self.content, tar=self.target)

