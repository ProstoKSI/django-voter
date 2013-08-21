try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from celery.task import task

from voter import compute

from poetry.models import Book
from threadedcomments.models import ThreadedComment
from blog.models import Post

@task(ignore_result=True)
def task_compute_book_rating(book_id):
    book = Book.objects.get(id=book_id)
    compute.compute_book_rating(book)

    for author in book.authors.all():
        task_compute_user_rating.delay(author.id)

@task(ignore_result=True)
def task_compute_post_rating(post_id):
    post = Post.objects.get(id=post_id)
    compute.compute_post_rating(post)
    
    task_compute_user_rating.delay(post.author.id)

@task(ignore_result=True)
def task_compute_comment_rating(comment_id):
    comment = ThreadedComment.objects.get(id=comment_id)
    compute.compute_comment_rating(comment)

    task_compute_user_rating.delay(comment.user.id)

@task(ignore_result=True)
def task_compute_user_rating(user_id):
    user = User.objects.get(id=user_id)
    compute.compute_user_rating(user)

COMPUTE_TYPE_FUNC = {
    'book': task_compute_book_rating,
    'post': task_compute_post_rating,
    'comment': task_compute_comment_rating,
    'user': task_compute_user_rating,
}

def task_compute_object_rating(obj_type, obj):
    return COMPUTE_TYPE_FUNC[obj_type].delay(obj.id)
   
