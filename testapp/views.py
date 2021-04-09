from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse,HttpResponse
import json
from django.core.serializers import serialize
from .models import Employee
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .forms import empform
# Create your views here.

@method_decorator(csrf_exempt,name='dispatch')
class Home(View):
    def get(self,r , *args, **kwargs):
        # from get what can we except ? we should able to deliver response if someone requested with the specific id or else we deliver all the records
        # first we have get the id or none
        try:
            data=r.body # we are not sure the user is gonna send the data with get req or no so put this in the try block
            # this will be in the json format so we have to convert this into python
            p_data=json.loads(data)
            # now we can get the id from the pyhton data
            id = p_data.get('id')
        except:
            id = None
        # at this point we have the value of id or None we have send response accordingly
        if id is None:
            # here if id is none we have to send the entire data
            obj=Employee.objects.all()
            # now we got this data which is the form of database data we have to conver it python and then to json
            p_data = serialize('json',obj) # this will convert into json
            p_data= json.loads(p_data)
            print(p_data[0])
            # now we have the python data i which we only want the fields
            f_l=[]
            for i in p_data:
                f_l.append(i['fields'])
            j_data = json.dumps(f_l)

            return HttpResponse(j_data,content_type='application/json')
        else:
            obj = Employee.objects.get(id=id)
            # this is in the obj format
            j_data= serialize('json',[obj,])
            p_data = json.loads(j_data)
            return JsonResponse(p_data[0]['fields'])

        return JsonResponse("this is from the get method",safe=False)

    def post(self,r,*args,**kwargs):
        # from the post we should get some data for sure. for that we have to create modelform.
        try:
            data = r.body
            # this is in  json format
            p_data=json.loads(data)
            #this is in python dict
            form = empform(p_data)
            print("venu herer")
            if form.is_valid():
                print(p_data)
                print("manisha")
                form.save()
                print("did i save")
                return JsonResponse("this is from the post",safe=False,status=207)

        except Exception as e:
            print(e)
            return JsonResponse("something went wrong ",safe=False,status=400)
    def put(self,r,*args,**kwargs):
        data = r.body
        # this is json data
        p_data = json.loads(data)
        # now we have the python data inorder to modify the data we need the id
        id = p_data.get('id')
        obj = Employee.objects.get(id=id)
        old_data={
            'eno':obj.eno,
            'ename':obj.ename,
            'eadd': obj.eadd,
            'ecity': obj.ecity,
        }
        old_data.update(p_data)
        # now we have updated the dict
        form = empform(old_data,instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse("success",safe=False)
        return JsonResponse("this is from put",safe=False)
