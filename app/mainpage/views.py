from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse


import re
import os




from physics.views import COVERAGE_TOTALS


def mainpage(request):

    context = {'navbar': None}
    return render(request, 'mainpage/index.html', context)


def phgo(request):


    def countfiles(dir):
        return len([name for name in os.listdir(dir) if (os.path.isfile(os.path.join(dir, name)) and ('-' not in name))])
    

    fps = ['/home/app/web/mediafiles/imgbank/' + str(i) + '/' for i in range(1, 6)]
    counts = [countfiles(fps[i]) for i in range(5)]
    count1, count2, count3, count4, count5 = counts
    totals = [sum(COVERAGE_TOTALS[i]) for i in range(1, 6)]
    total1, total2, total3, total4, total5 = totals
    coverages = [round(counts[i] / totals[i] * 100) for i in range(5)]
    coverage1, coverage2, coverage3, coverage4, coverage5 = coverages

    # this is freedom percentage
    global_total = sum(totals)
    global_count = sum(counts)
    freedom = round(global_count / global_total * 100)

    context = {
        'count1': count1,
        'total1': total1,
        'coverage1': coverage1,
        'count2': count2,
        'total2': total2,
        'coverage2': coverage2,
        'count3': count3,
        'total3': total3,
        'coverage3': coverage3,
        'count4': count4,
        'total4': total4,
        'coverage4': coverage4,
        'count5': count5,
        'total5': total5,
        'coverage5': coverage5,
        'freedom': freedom,
    }
    return render(request, 'physics/index.html', context)


def antiplagpage(request):
    return render(request, "antiplag/index.html")