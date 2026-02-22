from .models import User, Pharmacy

def profile_context(request):
    context = {}
    if request.user.is_authenticated:
        if request.user.user_type == 'user':
            try:
                context['profile_user'] = User.objects.get(login=request.user)
            except User.DoesNotExist:
                pass
        elif request.user.user_type == 'pharmacy':
            try:
                context['profile_pharmacy'] = Pharmacy.objects.get(login=request.user)
            except Pharmacy.DoesNotExist:
                pass
    return context
