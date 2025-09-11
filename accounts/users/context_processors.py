# tiers/context_processors.py

def user_company(request):
    if not request.user.is_authenticated:
        return {'company': None, 'branches': None}
    company = request.user.company
    return {'company': company, 'branches': request.user.accessible_branches.all()}
