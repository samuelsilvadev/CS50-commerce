from auctions.models import Watchlist


def count_context(request):
    if request.user is not None and request.user.is_authenticated:
        count = Watchlist.objects.filter(user=request.user).count()

        return {"watchlist_count": count}
