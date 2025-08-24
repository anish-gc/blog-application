from django.views import View
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db import transaction

from utilities.decorators import jwt_required
from utilities.mixins import JSONResponseMixin, PaginationMixin, SearchMixin
from .models import Post
from django.http import JsonResponse

User = get_user_model()


class BasePostView(View, JSONResponseMixin):
    """Base view for all post operations"""
    
    def dispatch(self, request, *args, **kwargs):
        """Override to handle preflight requests"""
        if request.method == 'OPTIONS':
            response = JsonResponse({})
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response
        return super().dispatch(request, *args, **kwargs)
    
    def get_post_or_404(self, post_id, user=None, check_ownership=False):
        """Get post by ID with optional ownership check"""
        try:
            post = get_object_or_404(Post, id=int(post_id))
            
            if check_ownership and user and post.author != user:
                return None, self.json_response(
                    errors={'detail': 'You do not have permission to perform this action'},
                    status=403
                )
            
            return post, None
        except ValueError:
            return None, self.json_response(
                errors={'detail': 'Invalid post ID'},
                status=400
            )
    
    def validate_post_data(self, data):
        """Validate post data"""
        errors = {}
        
        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
        
        if not title:
            errors['title'] = 'Title is required'
        elif len(title) < 3:
            errors['title'] = 'Title must be at least 3 characters long'
        elif len(title) > 200:
            errors['title'] = 'Title cannot exceed 200 characters'
        
        if not content:
            errors['content'] = 'Content is required'
        elif len(content) < 10:
            errors['content'] = 'Content must be at least 10 characters long'
        
        return errors


class PostListView(BasePostView, PaginationMixin, SearchMixin):
    """
    GET /posts/ - Get all posts (Public)
    """
    
    def get(self, request):
        """Get all published posts with pagination and search"""
        try:
            queryset = Post.objects.select_related('author').filter(is_active=True)
            
            # Apply search
            queryset = self.apply_search(queryset, request)
            
            # Apply author filter if provided
            author_id = request.GET.get('author')
            if author_id:
                try:
                    queryset = queryset.filter(author_id=int(author_id))
                except ValueError:
                    return self.json_response(
                        errors={'author': 'Invalid author ID'},
                        status=400
                    )
            
            # Apply ordering
            ordering = request.GET.get('ordering', '-created_at')
            valid_orderings = ['created_at', '-created_at', 'title', '-title', 'updated_at', '-updated_at']
            if ordering in valid_orderings:
                queryset = queryset.order_by(ordering)
            
            # Paginate results
            paginated_data = self.paginate_queryset(queryset, request)
            
            # Serialize data
            posts_data = []
            for post in paginated_data['data']:
                posts_data.append(self.serialize_object(post))
            response_data = {
                'posts': posts_data,
                'pagination': paginated_data['pagination']
            }
            
            return self.json_response(response_data)
            
        except Exception as e:
            return self.json_response(
                errors={'detail': 'An error occurred while fetching posts'},
                status=500
            )


class PostCreateView(BasePostView):
    """
    POST /posts/ - Create new post (Authenticated)
    """
    
    @jwt_required  
    def post(self, request):
        """Create a new post"""
        try:
            # Parse JSON data
            data = self.get_json_data(request)
            if data is None:
                return self.json_response(
                    errors={'detail': 'Invalid JSON data'},
                    status=400
                )
            
            # Validate data
            validation_errors = self.validate_post_data(data)
            if validation_errors:
                return self.json_response(errors=validation_errors, status=400)
            
            # Create post
            with transaction.atomic():
                post = Post.objects.create(
                    title=data['title'].strip(),
                    content=data['content'].strip(),
                    is_active=data.get('is_published', True), 
                    author=request.user
                )
            
            return self.json_response(
                {'post': self.serialize_object(post)},
                status=201
            )
            
        except Exception as e:
            return self.json_response(
                errors={'detail': 'An error occurred while creating the post'},
                status=500
            )

class UserPostsView(BasePostView, PaginationMixin, SearchMixin):
    """
    GET /posts/my-posts/ - Get authenticated user's posts
    """
    @jwt_required  
    def get(self, request):
        """Get authenticated user's posts with pagination and search"""
        try:
            # Check if user is authenticated
            if not request.user.is_authenticated:
                return self.json_response(
                    errors={'detail': 'Authentication required'},
                    status=401
                )
            
            # Base queryset - only user's posts (both published and drafts)
            queryset = Post.objects.select_related('author').filter(
                author=request.user
            )
            
            # Apply search
            queryset = self.apply_search(queryset, request)
            
            # Apply ordering
            ordering = request.GET.get('ordering', '-created_at')
            valid_orderings = ['created_at', '-created_at', 'title', '-title', 'updated_at', '-updated_at']
            if ordering in valid_orderings:
                queryset = queryset.order_by(ordering)
            
            # Paginate results
            paginated_data = self.paginate_queryset(queryset, request)
            
            # Serialize data
            posts_data = []
            for post in paginated_data['data']:
                posts_data.append(self.serialize_object(post))
                
            response_data = {
                'posts': posts_data,
                'pagination': paginated_data['pagination']
            }
            
            return self.json_response(response_data)
            
        except Exception as e:
            return self.json_response(
                errors={'detail': 'An error occurred while fetching your posts'},
                status=500
            )
class PostDetailView(BasePostView):
    """
    GET /posts/<id>/ - Get post details (Public)
    """
    
    def get(self, request, post_id):
        """Get post details by ID"""
        try:
            post, error_response = self.get_post_or_404(post_id)
            if error_response:
                return error_response
            
            # Check if post is published (unless owner is viewing)
            if not post.is_active and (not request.user or post.author != request.user):
                return self.json_response(
                    errors={'detail': 'Post not found'},
                    status=404
                )
            
            return self.json_response({'post': self.serialize_object(post)})
            
        except Exception as e:
            return self.json_response(
                errors={'detail': 'An error occurred while fetching the post'},
                status=500
            )


class PostUpdateView(BasePostView):
    """
    PUT /posts/<id>/ - Edit a post (Only author)
    """
    
    @jwt_required
    def put(self, request, post_id):
        """Update post (full update)"""
        return self._update_post(request, post_id, partial=False)
    
    @jwt_required
    def patch(self, request, post_id):
        """Update post (partial update)"""
        return self._update_post(request, post_id, partial=True)
    
    def _update_post(self, request, post_id, partial=False):
        """Handle post updates"""
        try:
            # Get post and check ownership
            post, error_response = self.get_post_or_404(
                post_id, 
                user=request.user, 
                check_ownership=True
            )
            if error_response:
                return error_response
            
            # Parse JSON data
            data = self.get_json_data(request)
            if data is None:
                return self.json_response(
                    errors={'detail': 'Invalid JSON data'},
                    status=400
                )
            
            # For partial updates, only validate provided fields
            if not partial:
                validation_errors = self.validate_post_data(data)
            else:
                # Create a dict with current values for validation
                validation_data = {
                    'title': data.get('title', post.title),
                    'content': data.get('content', post.content),
                }
                validation_errors = self.validate_post_data(validation_data)
                
                # Only keep errors for fields that are being updated
                validation_errors = {
                    k: v for k, v in validation_errors.items() 
                    if k in data
                }
            
            if validation_errors:
                return self.json_response(errors=validation_errors, status=400)
            
            # Update post
            with transaction.atomic():
                if 'title' in data:
                    post.title = data['title'].strip()
                if 'content' in data:
                    post.content = data['content'].strip()
                if 'is_published' in data:
                    post.is_active = bool(data['is_published'])
                
                post.save()
            
            return self.json_response({'post': self.serialize_object(post)})
            
        except Exception as e:
            return self.json_response(
                errors={'detail': 'An error occurred while updating the post'},
                status=500
            )


class PostDeleteView(BasePostView):
    """
    DELETE /posts/<id>/ - Delete a post (Only author)
    """
    
    @jwt_required
    def delete(self, request, post_id):
        """Delete post"""
        try:
            # Get post and check ownership
            post, error_response = self.get_post_or_404(
                post_id, 
                user=request.user, 
                check_ownership=True
            )
            if error_response:
                return error_response
            
            # Store post data for response before deletion
            post_data = self.serialize_object(post)
            
            # Delete post
            with transaction.atomic():
                post.delete()
            
            return self.json_response({
                'message': 'Post deleted successfully',
                'deleted_post': post_data
            })
            
        except Exception as e:
            return self.json_response(
                errors={'detail': 'An error occurred while deleting the post'},
                status=500
            )