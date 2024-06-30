from django.db import models

class BoardUnit(models.Model):
    bname = models.CharField(max_length=20, null=False)
    bgender = models.CharField(max_length=2, default='m', null=False)
    bsubject = models.CharField(max_length=100, null=False)
    btime = models.DateTimeField(auto_now=True)
    bmail = models.EmailField(max_length=100, blank=True, default='')
    bweb = models.CharField(max_length=200, blank=True, default='')
    bcontent = models.TextField(null=False)
    bresponse = models.TextField(blank=True, default='')

    def __str__(self):
        return self.bsubject