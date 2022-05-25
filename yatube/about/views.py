
from django.views.generic.base import TemplateView
# Create your views here.


class AboutAuthorView(TemplateView):
    template_name = 'about/author.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["author_title"] = 'буба хуба'
        context["author_text"] = 'хуба буба'
        return context


class AboutTechView(TemplateView):
    template_name = 'about/tech.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tech_title"] = 'абуб абух'
        context["tech_text"] = 'абух абуб'
        return context
