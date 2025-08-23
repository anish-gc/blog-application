from django.db import models

from utilities.models import BaseModel

class Post(BaseModel):
    title = models.CharField(max_length=255, help_text="Enter the title of the post")
    content = models.TextField(help_text="Write the content of the post")
    author = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, related_name="posts")
   
    def __str__(self):
        return self.title

    class Meta:
        db_table = "posts"
        ordering = ['-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        indexes = [
            models.Index(fields=['title']), 
        ]  
    def to_dict(self):
        '''Convert model instance to dictionary'''
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author': {
                'id': self.author.id,
                'username': self.author.username,
        
            },
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'is_published': getattr(self, 'is_active', True),
        }    