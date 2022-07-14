from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

department = (
    ('None', "None"),
    ('Cardiology', "Cardiology"),
    ('ENT Specialists', "ENT Specialists"),
    ('Astrology', 'Astrology'),
    ('Neuroanatomy', 'Neuroanatomy'),
    ('Blood Screening', 'Blood Screening'),
    ('Eye Care', 'Eye Care'),
    ('Physical Therapy', 'Physical Therapy'),
)
TIMESLOT_LIST = (
	('0', '00:00 – 00:00'),
	('1', '10:00 – 10:30'),
	('2', '11:00 – 11:30'),
	('3', '12:00 – 12:30'),
	('4', '13:00 – 13:30'),
	('5', '14:00 – 14:30'),
	('6', '15:00 – 15:30'),
	('7', '16:00 – 16:30'),
	('8', '17:00 – 17:30'),
    )
class Timeslot(models.Model):
    timeslot = models.CharField(max_length = 20, choices=TIMESLOT_LIST, default = '0')

class Specialists(models.Model):
    department = models.CharField(choices=department, max_length=100, default = 'None')

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    time = models.ManyToManyField(Timeslot)
    Specialist = models.ForeignKey(Specialists, on_delete=models.CASCADE,blank=True, null=True)
    date = models.DateTimeField(default=timezone.now,blank=True, null=True)
    qualification_name = models.CharField(max_length=100,blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now,blank=True, null=True)

    def __str__(self):
        return self.full_name

    # def get_absolute_url(self):
    # return reverse('appointment:delete-appointment', kwargs={'pk': self.pk})

class Credentials(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    is_doctor = models.BooleanField(default=False)

class TakeAppointment(models.Model):
    doctor = models.ForeignKey(User, related_name="Doctor", on_delete=models.CASCADE,blank=True, null=True)
    user = models.ForeignKey(User,related_name="Patient", on_delete=models.CASCADE,blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    date = models.DateTimeField(default=timezone.now,blank=True, null=True)
    time = models.ForeignKey(Timeslot,on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return self.user.username
