from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


class BranchesView(View):
    def get(self, request, bpk):
        user = request.user
        company = user.company
        branch = company.branches.get(pk=bpk)

        context = {
            'branch': branch,
        }
        
        return render(request, 'branches/branches.html', context)
