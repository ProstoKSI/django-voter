from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from voter.models import Rating, RatingVote, Badge


class RatingVoteInline(admin.TabularInline):
    model = RatingVote


class RatingAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'score', 'likes', 'dislikes')
    inlines = [
        RatingVoteInline,
    ]

    def get_name(self, rating):
        return rating.get_objects_name()
    get_name.short_description = _('Name')


class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating_weight')
    filter_horizontal = ['users']


class RatingVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_rating', 'vote_type')

    def get_rating(self, vote):
        return vote.rating.get_objects_name()
    get_rating.short_description = _('Rating')


admin.site.register(Rating, RatingAdmin)
admin.site.register(Badge, BadgeAdmin)
admin.site.register(RatingVote, RatingVoteAdmin)

