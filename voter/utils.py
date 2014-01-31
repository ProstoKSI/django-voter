from django.db.models import Max

from .models import RatingVote, VOTE_LIKE


DEFAULT_RATING_WEIGHT = 1
DEFAULT_RATING_BONUS = 0

def get_user_best_badge_info(user):
    badge_list = user.badge_list.all().aggregate(
        rating_weight=Max('rating_weight'),
        rating_bonus=Max('rating_bonus')
    )
    if badge_list['rating_weight'] is not None:
        return badge_list
    return {
        'rating_weight': DEFAULT_RATING_WEIGHT, 
        'rating_bonus': DEFAULT_RATING_BONUS,
    }

def get_weighted_vote(rating):
    score = 0
    vote_list = RatingVote.objects.filter(rating=rating)
    for vote in vote_list:
        badge = get_user_best_badge_info(vote.user)
        score += (+1 if vote.vote_type == VOTE_LIKE else -1) * badge['rating_weight']
    return score

