# tiers/context_processors.py

def user_company(request):
    if not request.user.is_authenticated:
        return {'company': None, 'branches': None}
    company = request.user.company
    if request.user.is_company_admin:
        branches = company.branches.all()
    else:
        branches = request.user.accessible_branches.all()
    return {'company': company, 'branches': branches}
