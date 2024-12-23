""" announcement context_processors """
from .announcement import Announcement_context

def announcement(request):
    announcement_obj = Announcement_context(request)
    announcements = announcement_obj.announcement
    
    return {'announcements': announcements}
