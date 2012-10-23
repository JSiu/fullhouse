from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from forms import AnnouncementForm
from models import Announcement
from models import House

def home(request):
    return HttpResponseRedirect('/welcome/')

def create_announcement(request):
    if request.method == "GET":
        form = AnnouncementForm()
        return render_to_response('create_announcement.html',
            RequestContext(request, {
                'form': form
            }))
    else:
        if request.user.userprofile.house == None:
            # Create a dummy house, since there's no other way now.
            house = House()
            house.name = "temp house"
            house.zipcode = 98105
            house.save()
            request.user.userprofile.house = house
            request.user.userprofile.save()
        announcement = Announcement()
        announcement.title = request.POST["title"]
        announcement.text = request.POST["text"]
        announcement.creator = request.user.userprofile
        announcement.house = request.user.userprofile.house
        announcement.save();
        return HttpResponseRedirect('/dashboard/')

def welcome(request):
    form = AuthenticationForm()
    return render_to_response('welcome.html',
        RequestContext(request, {
            'form': form
        }))

@login_required
def dashboard(request):
    return render_to_response('dashboard.html', {
        'announcements': request.user.userprofile.house.announcements.all()
    }, context_instance=RequestContext(request))
