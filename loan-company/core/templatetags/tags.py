from core.models import UserInfo
from django import template




register = template.Library()

@register.simple_tag(takes_context=True)
def user_first_name(context):
    request = context['request']
    try:
        user_id = request.user.id
        user_name = UserInfo.objects.get(user=user_id)
        return user_name.first_name
    except:
        return request.user.username

@register.simple_tag(takes_context=True)
def user_last_name(context):
    request = context['request']
    try:
        user_id = request.user.id
        user_name = UserInfo.objects.get(user=user_id)
        return user_name.last_name
    except:
        return None



@register.simple_tag(takes_context=True)
def user_icon(context):
    request = context['request']
    try:
        user_id = request.user.id
        user_initials = UserInfo.objects.get(user=user_id)
        return user_initials.first_name[0].upper() + user_initials.last_name[0].upper()
        
    except:
        return None

@register.simple_tag(takes_context=True)
def sort_col(context, arg1=''):

    ####DO DOPRACOWANIA ! funkcjalnosc ok ale do zmiany wstawianie '&'####
    request = context['request']

    w = str(request.get_full_path)
    var_path = w.split("'")[1]
    clean_var_path = var_path.split('page', 1)[0]

    if arg1 == 'PAGINATE':
        
        if '?' in var_path:
            if clean_var_path[-1] == '?' or clean_var_path[-1] == '&':
                return clean_var_path+'page='
            else:
                return clean_var_path+'&page='
        else:
            return clean_var_path+'?page='
    
    else:
        ascending_pattern = f'order_by={arg1}'
        decending_pattern = f'order_by=-{arg1}'
        base_path = str(request.path) + '?'
        try: 
            query_string_path = var_path.split(base_path)[1]
        except IndexError:
            query_string_path = ''
        query_string_clean_path = query_string_path.split('&page', 1)[0]

        if '?' in var_path:
            if clean_var_path[-1] == '?' or clean_var_path[-1] == '&':
                if ascending_pattern in query_string_path:
                    x = query_string_clean_path.split(ascending_pattern)
                    z = base_path + decending_pattern
                    return z + '&' + ''.join(x)
                    
                elif decending_pattern in query_string_path:
                    x = query_string_clean_path.split(decending_pattern)
                    z = base_path + ascending_pattern
                    return z + '&' + ''.join(x)
                
                else:
                    return base_path + 'order_by='+arg1 + '&' + query_string_clean_path              

            else:
                return clean_var_path+'&order_by='+arg1

        else:
            return clean_var_path+'?order_by='+arg1
        

    

@register.simple_tag(takes_context=True)
def sort_active_th(context):
    request = context['request']
    return str(request.GET.getlist('order_by'))