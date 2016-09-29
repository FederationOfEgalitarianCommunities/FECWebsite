"""This module contains views used to display & choose Decisions."""
import urllib

from django.shortcuts import render
from django.http import Http404

from .models import Decision


def decision_detail_view(request):
    """Render An Option Chooser or a Summary of Choosen Options."""
    if request.method != 'GET':
        raise Http404
    get_params = request.GET.copy()
    context = {}
    decisions = Decision.objects.all().order_by('_order')
    is_summary = 'summary' in get_params
    if is_summary:
        del get_params['summary']
        template_name = 'ciab/summary.html'
    else:
        template_name = 'ciab/steps.html'
        try:
            current_step = int(get_params.pop('currentStep')[0])
        except:
            current_step = 0

    sidebar_items = []
    for (index, decision) in enumerate(decisions):
        passed_id = get_params.get(str(index), None)
        if passed_id:
            selected_option = decision.option_set.filter(id=passed_id)
            if selected_option.exists():
                sidebar_items.append((decision, selected_option[0]))
                continue
        sidebar_items.append((decision, None))

    context = {'decisions': decisions, 'sidebar_items': sidebar_items,
               'sidebar_link': '?' + urllib.urlencode(get_params)}

    if not is_summary:
        context['decision'] = decisions[current_step]
        context['step_number'] = current_step + 1
        if current_step < len(decisions) - 1:
            get_params['currentStep'] = current_step + 1
            if str(current_step) in get_params:
                del get_params[str(current_step)]
            context['next_link'] = '?{}&{}='.format(
                urllib.urlencode(get_params), current_step)
        else:
            get_params['summary'] = ''
            context['next_link'] = '?{}&{}='.format(
                urllib.urlencode(get_params), current_step)
    return render(request, template_name, context)
