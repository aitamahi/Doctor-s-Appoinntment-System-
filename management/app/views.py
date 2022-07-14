from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse_lazy
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse
from django.views.generic import TemplateView, UpdateView, CreateView, ListView, DetailView, DeleteView
from django.views.generic.edit import DeleteView, UpdateView
from .models import *
import json
from django.contrib.auth import authenticate, login, logout
import pandas as pd

"""
For Patient Profile

"""


class DoctorReg(View):
     @method_decorator(csrf_exempt)
     def dispatch(self, *args, **kwargs):
        return super(DoctorReg,self).dispatch(*args,**kwargs)
     def get(self,request, *args, **kwargs):
         time= Timeslot.objects.all()
         specialist= Specialists.objects.all()
         return render(request,'register2.html',locals())
     def post(self,request, *args, **kwargs):
         data_dict = json.loads(request.body)
         print(data_dict)
         #import pdb; pdb.set_trace()

         dept = Specialists.objects.get(id = int(data_dict.get('dept')))
         user = User()
         user = User.objects.create_user(username=data_dict["email"],first_name=data_dict["name"],email=data_dict["email"],password=data_dict["psw"])
         user.save()
         cred_obj = Credentials()
         cred_obj.user = user
         cred_obj.is_doctor=True
         cred_obj.save()
         apn = Appointment()
         apn.user = user
         apn.full_name = data_dict.get('name')
         apn.Specialist = dept
         apn.save()
         for i in data_dict.get('timeslot'):
             slot = Timeslot.objects.get(id = int(i))
             apn.time.add(slot)

         resp = HttpResponse(json.dumps(data_dict), content_type="application/json", status=200)
         return resp

class UserReg(View):
     @method_decorator(csrf_exempt)
     def dispatch(self, *args, **kwargs):
        return super(UserReg,self).dispatch(*args,**kwargs)
     def get(self,request, *args, **kwargs):
         return render(request,'userreg.html',locals())
     def post(self,request, *args, **kwargs):
         data_dict = json.loads(request.body)
         print(data_dict)
         #import pdb; pdb.set_trace()
         userObj = User.objects.create_user(username=data_dict["email"],first_name=data_dict["name"],email=data_dict["email"],password=data_dict["psw"])
         userObj.save()


         resp = HttpResponse(json.dumps(data_dict), content_type="application/json", status=200)
         return resp

class Login(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(Login,self).dispatch(*args,**kwargs)

    def get(self,request, *args, **kwargs):
        return render(request,'login.html',locals())

    def post(self,request,*args,**kwargs):

        contenttype = request.META.get('CONTENT_TYPE', None)
        data_dict = None
        res = {}
        if 'json' in contenttype or 'text/plain' in contenttype:
            try:
                data_dict = json.loads(request.body.decode('utf-8'))
            except Exception as e:
                print(e)
        elif 'multipart/form-data' in contenttype:
            data_dict = request.POST.dict()
        elif contenttype == 'application/x-www-form-urlencoded':
            data_dict = request.POST
        else:
            print('Unknown ContentType: %s', contenttype)
            pdr = HttpResponse(status=400)
            pdr.write('Unknown HTTP ContentTye')
            return pdr
        try:
            username = data_dict['username']
            password = data_dict['password']
            try:
                if username == username :
                    user_obj = User.objects.get(username = username)
                    try:
                        user_obj = Credentials.objects.get(user = user_obj, is_doctor=True)
                        res['url'] = '/doctor/'
                    except:
                        user_obj
                        res['url'] = '/search/'

                    if user_obj:
                        # import pdb; pdb.set_trace()
                        user = authenticate(request,username=username, password=password)
                        if user is not None:
                            login(request, user)
                            request.session['username'] = user.username
                            request.session['name'] = user.username.upper()

                            resp = HttpResponse(content_type="application/json", status=200)
                            resp.write(json.dumps(res))
                            return resp
                        else:
                            data_dict['error_message'] = 'Incorrect Password'
                            resp = HttpResponse(content_type="application/json", status=500)
                            resp.write(json.dumps(data_dict))
                            return resp
                else:
                    data_dict['error_message'] = 'User Does not existed'
                    resp = HttpResponse(content_type="application/json", status=500)
                    resp.write(json.dumps(data_dict))
                    return resp
            except Exception as e:
                print(e)
                data_dict['error_message'] = 'Invalid Username'
                resp = HttpResponse(content_type="application/json", status=500)
                resp.write(json.dumps(data_dict))
                return resp

            resp = HttpResponse(content_type="application/json", status=200)
            resp.write(json.dumps(res))
            return resp
        except Exception as e:
            print(e)
            resp = HttpResponse(content_type="application/json", status=500)
            resp.write(json.dumps(data_dict))
            return resp

class SearchDoctor(View):
     @method_decorator(csrf_exempt)
     @method_decorator(login_required)
     def dispatch(self, *args, **kwargs):
        return super(SearchDoctor,self).dispatch(*args,**kwargs)
     def get(self,request, *args, **kwargs):
         userlist = Credentials.objects.filter(is_doctor=True).values('user','user__first_name')
         credf = pd.DataFrame(Credentials.objects.filter(is_doctor=True).values('user','user__first_name')[::1])
         appointmentdf = pd.DataFrame(Appointment.objects.filter(user__id__in=credf['user'].unique().tolist()).values('user','time__timeslot','time','Specialist','Specialist__department')[::1])
         appointmentdf = appointmentdf.to_dict('records')
         return render(request,'search_doctors.html',locals())
     def post(self,request, *args, **kwargs):
         data_dict = json.loads(request.body)
         print(data_dict)
         #import pdb; pdb.set_trace()
         if data_dict.get("status") =="DoctorConsult":
             checkObj = TakeAppointment.objects.filter(doctor__id=data_dict['doctor'],date=data_dict['date'])
             if checkObj.count()>0:
                 usertime = pd.DataFrame(checkObj.values('time','time__timeslot')[::1])
                 data_dict['timedata'] = usertime.to_dict('records')
             else:
                data_dict['timedata']=[]

             resp = HttpResponse(json.dumps(data_dict), content_type="application/json", status=200)
             return resp
         elif data_dict.get("status")=="Appointment_save":
            takeAppObj = TakeAppointment()
            takeAppObj.doctor = User.objects.get(id=data_dict.get('doctor'))
            takeAppObj.user = request.user
            takeAppObj.date = data_dict.get('date')
            #takeAppObj.phone_number = data_dict.get('phone')
            #takeAppObj.message = data_dict.get('msg')
            takeAppObj.time = Timeslot.objects.get(id=data_dict.get('appoint_time'))
            takeAppObj.save()

            resp = HttpResponse(json.dumps(data_dict), content_type="application/json", status=200)
            return resp

class DoctorPage(View):
     @method_decorator(csrf_exempt)
     @method_decorator(login_required)
     def dispatch(self, *args, **kwargs):
        return super(DoctorPage,self).dispatch(*args,**kwargs)
     def get(self,request, *args, **kwargs):
         user = request.user.username
         Patient = TakeAppointment.objects.filter(doctor__username=user).values('user__username','date','time__timeslot','date','message')
         return render(request,'doctor.html',locals())


class Logout(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Logout,self).dispatch(*args,**kwargs)

    def get(self,request,*args,**kwargs):
        print("=======================logut")
        request.session.flush()
        response = "success"
        return HttpResponseRedirect('/')
