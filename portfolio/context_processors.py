from landing.models import Profile

def profile_context(request):
    """
    Makes profile available in all templates.
    This avoids passing profile in every view.
    """
    try:
        profile = Profile.objects.first()
    except:
        profile = None
    
    return {
        'profile': profile,
    }