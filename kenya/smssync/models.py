from django.db import models

class SMSSyncOutgoing(models.Model):

    target = models.CharField(max_length=50)

    content = models.CharField(max_length=1000)

    def __unicode__(self):
        return '"{cont}" >> {tar}'.format(cont=self.content, tar=self.target)
