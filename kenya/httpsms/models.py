from django.db import models

# Create your models here.

class HTTPSMSOutgoing(models.Model):

    target = models.CharField(max_length=50)
    
    network = models.CharField(max_length=50)
    
    content = models.CharField(max_length=1000)

    def __unicode__(self):
        return '{0.tar}({0.network}): {0.content}'.format(self)
        
