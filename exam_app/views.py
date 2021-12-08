from django.shortcuts import render, redirect, HttpResponse
from login_app.models import User
from .models import Group
from django.contrib import messages
from django.db.models import Count


def index(request):
    if 'user_id' not in request.session:
        return redirect('/')

    context = {
            'user': User.objects.get(id = request.session['user_id']),
            'all_groups': Group.objects.all().annotate(mem_count=Count('members')).order_by('-mem_count')
        }

    return render(request,'index.html', context)

def add_group(request):
    if 'user_id' not in request.session:
        return redirect('/')

    errors = Group.objects.group_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)

    else:
        org_name = request.POST['org_name']
        desc = request.POST['desc']
        created_by = User.objects.get(id=request.session['user_id'])

        group = Group.objects.create(org_name=org_name, description=desc, created_by=created_by)

        group.members.add(group.created_by)
        group.save()


    return redirect('/groups')

def group_details(request, group_id):
    if 'user_id' not in request.session:
        return redirect('/')

    group = Group.objects.get(id=group_id)

    context = {
        'group': group,
        'user': User.objects.get(id=request.session['user_id']),
        'members': group.members.all()
    }

    return render(request,'group_details.html', context)

def leave(request,group_id):
    if 'user_id' not in request.session:
        return redirect('/')

    group = Group.objects.get(id=group_id)
    user = User.objects.get(id=request.session['user_id'])
    group.members.remove(user)
    group.save()

    return redirect(f'/groups/{group.id}')

def join(request,group_id):
    if 'user_id' not in request.session:
        return redirect('/')

    group = Group.objects.get(id=group_id)
    user = User.objects.get(id=request.session['user_id'])
    group.members.add(user)
    group.save()

    return redirect(f'/groups/{group.id}')

def remove(request,group_id):
    if 'user_id' not in request.session:
        return redirect(f'/groups/{group_id}')

    group = Group.objects.get(id=group_id)
    user = User.objects.get(id=request.session['user_id'])

    if group.created_by.id != user.id:
        return redirect(f'/groups/{group_id}')

    elif group.created_by.id == user.id:
        Group.delete(group)

        return redirect('/groups')