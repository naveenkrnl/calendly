from datetime import date
from django.shortcuts import render
from accounts.models import UserProfile
from .models import UserSlots
# Create your views here.

 
def home(request):
    # dictionary for initial data with
    # field names as keys

         
    return render(request, "base.html")

 
def my_slots(request):
    # dictionary for initial data with
    # field names as keys
    context = {}
    if request.POST:
        username = request.POST.get('username')

        if username == '' or username is None:
            context['error'] = "Name can't be empty"
        else:
            qs = UserProfile.objects.filter(name = username)
            if qs:
                context['error'] = "Name can't be empty"
                context['my_slots'] = UserSlots.objects.filter(user = qs.first())
                context['booked_by_you'] = UserSlots.objects.filter(slot_booked_by = qs.first())
            else:
                context['error'] = "User Doesn't exist"

    # add the dictionary during initialization
         

    return render(request, "my_slots.html", context)



     
def check_slot(request):
    # dictionary for initial data with
    # field names as keys
    import datetime
    context = {}
    context['users'] = UserProfile.objects.all()
    context['today'] = datetime.date.today()
    context['today'] = context['today'].strftime("%Y-%m-%d")

    if request.POST:
        username = request.POST.get('username')
        day = request.POST.get('date')
        if username == '' or username is None or username is "0":
            context['error'] = "Name can't be empty"
        else:
            qs = UserProfile.objects.filter(id = username)
            context['user_id'] = qs.first().id
            import datetime
            datetime_object = datetime.datetime.strptime(day + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
            one_day_after = datetime_object + datetime.timedelta(days=1)
            slots = []
            while datetime_object<one_day_after:
                slot = {}
                format = '%I:%M %p'
                slot['start_time_obj'] =  datetime_object

                slot['start_time'] =  datetime.datetime.strftime(datetime_object, '%Y-%m-%d %H:%M:%S')
                my_date = datetime.datetime.strftime(datetime_object, format)
                slot['start_time_text'] = my_date
                datetime_object = datetime_object + datetime.timedelta(minutes=30)
                format = '%I:%M %p'
                my_date = datetime.datetime.strftime(datetime_object, format)
                slot['end_time_obj'] =  datetime_object

                slot['end_time'] = datetime.datetime.strftime(datetime_object, '%Y-%m-%d %H:%M:%S')
                slot['end_time_text'] = my_date
                slot['label'] = slot['start_time_text'] + ' to ' + slot['end_time_text']
                slot['status'] = "Free"
                print(qs.first(),slot['start_time_obj'], slot['end_time_obj'])
                qs = UserSlots.objects.filter(user_id=context['user_id'],start_time=slot['start_time_obj'], end_time = slot['end_time_obj'])
                if qs:
                    print("booked")
                    slot['status'] = 'booked'

                slots.append(slot)
            context['slots'] = slots
    # add the dictionary during initialization
    return render(request, "check_slots.html", context)

    
def book_slot(request):
    # dictionary for initial data with
    # field names as keys
    import datetime
    context = {}
    context['users'] = UserProfile.objects.all()

    context['user_id'] = request.GET.get('user')
    context['start_time'] = request.GET.get('start_time')
    context['end_time'] = request.GET.get('end_time')

    context['user'] = UserProfile.objects.filter(id=context['user_id'])

    if not context['user']:
        context['error'] = 'Invalid User'
    else:
        context['user'] = context['user'].first()
        qs = UserSlots.objects.filter(user=context['user'],start_time=context['start_time'], end_time = context['end_time'] )
        if qs:
            context['error'] = 'This slot is already booked'
        if request.POST:
            context['reason'] = request.POST.get('reason')
            context['booked_by'] = request.POST.get('username')
            obj = UserSlots.objects.create(user=context['user'],start_time =context['start_time'], end_time = context['end_time'],reason = context['reason'], slot_booked_by_id = context['booked_by'] )
            obj.save()
            context['error'] = 'Slot Booked Successfully'

    # add the dictionary during initialization
    return render(request, "book_slots.html", context)