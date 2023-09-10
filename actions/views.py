from django.shortcuts import render
from actions.models import Action
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def dashboard(request):   
    action_list = Action.objects.all()
    followers = request.user.profile.following.all().values_list('user_id', flat=True)
    if followers:
        action_list = action_list.filter(user_id__in=followers)                               
    action_list = action_list[:100]
    paginator = Paginator(action_list, 8)
    page_number = request.GET.get('page')
    try:
        actions = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        actions = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        actions = paginator.page(paginator.num_pages)
    return render(request, 'actions/dashboard.html', {'actions': actions})
