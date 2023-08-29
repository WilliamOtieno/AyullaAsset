from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect
from .services import add_coin_to_user_portfolio, get_top_ranked_currencies, search_coin
from .selectors import get_total_referral_bonus, get_user_coins, get_user_referrals


class HomeView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["data"] = get_top_ranked_currencies()
        query = self.request.GET.get("query")
        if query is not None:
            search_results = search_coin(query)
            context["search_data"] = search_results
        new_coin = self.request.GET.get("coin_id")
        if new_coin is not None:
            add_coin_to_user_portfolio(self.request.user, new_coin)
            return redirect("core:portfolio")
        return context


class PortfolioView(LoginRequiredMixin,TemplateView):
    template_name = "portfolio.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        new_coin = self.request.GET.get("coin_id")
        if new_coin is not None:
            add_coin_to_user_portfolio(self.request.user, new_coin)
            return redirect("core:portfolio")
        context["referrals"] = get_user_referrals(self.request.user)
        context["coins"] = get_user_coins(self.request.user)
        context["bonus"] = get_total_referral_bonus(self.request.user)
        return context

