import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.db.models import Q


class JSONResponseMixin:
    """Mixin to handle JSON responses"""
    
    def json_response(self, data=None, status=200, errors=None):
        """Return JSON response"""
        response_data = {}
        
        if data is not None:
            if hasattr(data, '__dict__'):
                # Handle model instances
                response_data.update(self.serialize_object(data))
            elif isinstance(data, (list, tuple)):
                # Handle querysets or lists
                response_data['data'] = [
                    self.serialize_object(item) if hasattr(item, '__dict__') 
                    else item for item in data
                ]
            else:
                response_data.update(data)
        
        if errors:
            response_data['errors'] = errors
            
        return JsonResponse(response_data, status=status, safe=False)
    
    def serialize_object(self, obj):
        """Basic serialization for model objects"""
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        
        # Default serialization for Post model
        data = {
            'id': obj.id,
            'title': obj.title,
            'content': obj.content,
            'created_at': obj.created_at.isoformat(),
            'updated_at': obj.updated_at.isoformat(),
        }
        
        if hasattr(obj, 'author'):
            data['author'] = {
                'id': obj.author.id,
                'username': obj.author.username,
               
            }
        return data
    
    def get_json_data(self, request):
        """Parse JSON data from request"""
        try:
            return json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return None
        
class PaginationMixin:
    """Mixin to handle pagination"""
    page_size = 20
    max_page_size = 100
    
    def paginate_queryset(self, queryset, request):
        """Paginate queryset"""
        page_size = min(
            int(request.GET.get('page_size', self.page_size)),
            self.max_page_size
        )
        page_number = int(request.GET.get('page', 1))
        
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page_number)
        
        return {
            'data': list(page_obj),
            'pagination': {
                'page': page_obj.number,
                'pages': paginator.num_pages,
                'per_page': page_size,
                'total': paginator.count,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
            }
        }


class SearchMixin:
    """Mixin to handle search functionality"""
    search_fields = ['title', 'content']
    
    def apply_search(self, queryset, request):
        """Apply search filters to queryset"""
        search_query = request.GET.get('search', '').strip()
        if not search_query:
            return queryset
        
        q_objects = Q()
        for field in self.search_fields:
            q_objects |= Q(**{f'{field}__icontains': search_query})
        
        return queryset.filter(q_objects)
