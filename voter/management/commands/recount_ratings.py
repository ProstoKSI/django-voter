from django.core.management.base import NoArgsCommand
from django.contrib.auth.models import User

from voter.compute import recompute_ratings

class Command(NoArgsCommand):
    help = "Recount user ratings"
    
    def handle(self, *args, **options):
        obj_type_list = ['all']
        if len(args) > 0:
            obj_type_list = args
        for obj_type in obj_type_list:
            recompute_ratings(obj_type)
        
