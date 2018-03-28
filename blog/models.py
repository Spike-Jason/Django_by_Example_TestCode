from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter()


class Post(models.Model):
    STATUS_CHOICES=(
        ('draft', 'Draft'),
        ('published','Published'),
    )
    title = models.CharField(max_length=250)  #通过CharField在SQL中转化为VARCHAR
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish') #通过unique_for_date参数让帖子的URL通过日期和slug来构成
    # 通过ForeignKey作为一个约束实现一对多的关系，并通过related_name属性指定从User到Post的反向关系
    #author = models.ForeignKey(User,related_name='blog_posts')
    author = models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True) #创建日期的保存，字段会字段保存
    updated = models.DateTimeField(auto_now=True)#更新保存对象时，字段自动更新
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default='draft')

    objects = models.Manager()
    published = PublishedManager()
    class Meta:
        ordering = ('-publish',)  #这是一个元数据，当Django查询数据库时，默认返回pubilsh字段进行降序排列
    def __str__(self):
        return self.title    #当前对象默认的可读表现。

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug])
    tags = TaggableManager()
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments',on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created', )
    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)
