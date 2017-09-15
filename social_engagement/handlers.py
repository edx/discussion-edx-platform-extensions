"""
Discussion forum signal handlers
"""
from django.dispatch import receiver

from django_comment_common.signals import (
    thread_deleted,
    comment_deleted,
    thread_voted,
    comment_voted,
    thread_unfollowed,
)
from social_engagement.tasks import task_update_user_engagement_score


@receiver(thread_deleted)
@receiver(comment_deleted)
@receiver(thread_voted)
@receiver(comment_voted)
@receiver(thread_unfollowed)
def thread_comment_signal_handler(sender, **kwargs):  # pylint: disable=unused-argument
    """
    Updates user social engagement score
    """
    post = kwargs['post']
    course_id = getattr(post, 'course_id', None)
    user_id = getattr(post, 'user_id', None)
    if course_id and user_id:
        task_update_user_engagement_score.delay(unicode(course_id), user_id)
