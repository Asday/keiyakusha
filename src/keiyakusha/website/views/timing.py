from django.views.generic import TemplateView


class TimingView(TemplateView):
    template_name = 'timing/index.html'
