from django.contrib import messages
from django.forms.utils import from_current_timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from blog.models import Post

from .forms import CommentForm


@require_POST
def comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    # django 将用户提交的数据封装在 request.POST 中，这是一个类字典对象。
    # 我们利用这些数据构造了 CommentForm 的实例，这样就生成了一个绑定了用户提交数据的表单。
    form = CommentForm(request.POST)

    # 检查表单的数据是否符合格式要求
    if form.is_valid():
        # 检查到数据是合法的，调用表单的 save 方法保存数据到数据库，
        # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
        comment = form.save(commit=False)

        # post 是一个一对多的ForeignKey,设定为这个post的对象
        comment.post = post

        # 将评论数据保存进数据库
        comment.save()

        # 成功
        messages.add_message(request, messages.SUCCESS, "评论发表成功", extra_tags="success")
        # 重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
        # 然后重定向到 get_absolute_url 方法返回的 URL。
        return redirect(post)

    # 检查到数据不合法，我们渲染一个预览页面，用于展示表单的错误。
    # 渲染一个预览页面,用于显示表单的错误
    context = {
        "post": post,
        "form": form,
    }
    # 失败
    messages.add_message(request, messages.ERROR, "评论发表失败", extra_tags="danger")
    return render(request, "comments/preview.html", context=context)
