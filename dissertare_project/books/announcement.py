""" Announcement """
from .models import Announcement

class Announcement_context():
    def __init__(self, request):
        self.announcement = Announcement.objects.all()