from collections import OrderedDict
from django.views import View
from django.http import JsonResponse

from core.models import Customer, Adress, Workplace

# rest framework imports
from rest_framework.metadata import SimpleMetadata
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.generics import (UpdateAPIView, GenericAPIView,
                                    RetrieveUpdateAPIView)
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin
from .serializers import (AdressSerializer, CustomerSerializer,
                            WorkplaceSerializer)



class restApi(View):

    def get(self, *args, **kwargs):

        print(self.request.GET)
        print(self.request.POST)

        body = self.request.body  # byte string of json data
        data = {}

        try:
            data = json.loads(body) # string of Json data > python dict
        except:
            pass
        print(data)

        data['params'] = dict(self.request.GET)
        data['headers'] = dict(self.request.headers)
        data['content_type'] = self.request.content_type

        return JsonResponse(data)


@api_view(['GET', 'PATCH'])
def api_home(request, *args, **kwargs):

    '''
    DRF api view
    '''
    # instance = Customer.objects.all().order_by('?').first() # random ordering, first item only
    
    pk = kwargs['pk']
    instance = Customer.objects.get(pk=pk)
    data = {}
    field_params = {
        'basic' : [
            'first_name',
            'last_name',
            'martial_status',
            'id_passport',
        ],
        'contact' : [
            'adress',
            'phone_no',
            'email',
        ],
        'workplace': [
            'workplace',
            'job_posistion',
            'salaty',
            'esd',

        ]
    }

    # context = {
    #     'included_fields': [
    #         'last_name',
    #         'workplace',
    #         'first_name',
    #         'adress',
    #     ],
    # }
    # context = {}

    # data = model_to_dict(instance, fields = ['first_name', 'last_name', 'dob', 'adress'])

    # data = CustomerSerializer(instance=instance, context=context).data

    data = CustomerSerializer(instance=instance, fields=field_params['basic']).data
    # print(data['workplace']['adress'])
    
    # print(*args)
    # print(kwargs['pk'])

    # if request.method == 'PATCH':
        



    #     customer_instance = CustomerSerializer(instance=instance, data=request.data, partial=True)
    #     adress_instance = AdressSerializer(instance=instance.adress, data=request.data['adress'], partial=True)
    #     # workplace_instance = WorkplaceSerializer(instance=instance.workplace, data=data['workplace'], partial=True)
    #     # workplace_adr_instance = AdressSerializer(instance=instance.workplace.adress, data=data['workplace']['adress'], partial=True)
    #     # print(request.data['workplace']['id_nip'])
    #     # print(request.data['adress'])

    #     if customer_instance.is_valid():
    #         customer_instance.save()

    #     if adress_instance.is_valid(): #and workplace_instance.is_valid() and workplace_adr_instance.is_valid():
    #         # customer_instance.save()
    #         adress_instance.save()
    #         # workplace_instance.save()
    #         # workplace_adr_instance.save()
    #     #     return Response(request.data)
    #     # else:
    #     #     return Response(instance.errors)



    return Response(data)



class CustomerUpdateApiView(UpdateModelMixin, RetrieveModelMixin, GenericAPIView):

    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    lookup_field = 'pk'
    # metadata_class = SimpleMetadata
    fields = [
            'last_name',
            'adress',
            # 'workplace',
            # 'phone_no',
            # 'gender'
        ]
    
    # def get_serializer_context(self):
    #     """
    #     Extra context provided to the serializer class.
    #     """
    #     return {
    #         'request': self.request,
    #         'format': self.format_kwarg,
    #         'view': self,
    #         'fields': self.request['fields']
    #     }


    '''
    NOT FINISHED !
    '''

    def get(self, *args, **kwargs):
        instance = Customer.objects.get(pk=kwargs['pk'])
        meta = SimpleMetadata()
        data = meta.determine_metadata(self.request, self)['actions']['PUT']
        ser_data = CustomerSerializer(instance=instance, fields=self.fields).data
        merged_data = {}
    
        def merge_dictionaries(serializer_dict, meta_dict, output_dict):

            for k,v in serializer_dict.items():
                
                if isinstance(v, (OrderedDict, dict)):
                    
                        
                    meta_val = meta_dict.get(k, None)
                    print(True)
                    if meta_val is None:
                        print('meta_val_true')
                        pass
                    else:

                        pass

                else:
                    output_dict[k] = meta_dict[k]
                    output_dict[k]['val'] = v
                    # print('test')

            pass



        '''
        def merge_dictionaries(serializer_data, meta_data, recursion_data):

            if hasattr(serializer_data, 'items'):
                print(hasattr(serializer_data, 'items'))
                for k, v in serializer_data.items():
                    meta_val = meta_data.get(k, None)
                    # print(recursion_data)
                    print('KEY IS: ------', k)
                    print('\n-----BREAK-----\n')
                    print('META VAL----', meta_val)
                    print('\n-----BREAK-----\n')
                    print('META DATA --------',meta_data)
                    if meta_val is not None:
                        recursion_data[k] = meta_val
                    # print(recursion_data[k])
                        print('-----END------\n')
                        print(serializer_data[k], '\n')
                        print(meta_data[k], '\n')
                        print(recursion_data[k], '\n')
                        merge_dictionaries(serializer_data[k], meta_data[k], recursion_data[k])
                    else:
                        for key, val in meta_data.items():
                            if isinstance(val, (OrderedDict, dict)):
                                print(key, '\n')
                                print(val, '\n------end')
                                print('\n\n\n\n----IT WORKS')
                                merge_dictionaries(serializer_data, val, recursion_data[k])
                            else: 
                                print('TEST')
                                # recursion_data[key] = 'val'
                                # recursion_data[key] = val
                                # print(recursion_data[key])
                                # print(val)


                        # print('\n-----BREAK-----\n------ELSE------')
                        # print(meta_data['children'][k].get(k, None))
                        # for key, val in meta_data[k].items():
                        #     if isinstance(val, OrderedDict):
                        #         merge_dictionaries(serializer_data[k], val, recursion_data[k])

                        # meta_val_nest = meta_data['children'].get(k, None)
                        # recursion_data[k] = meta_val_nest
                        # merge_dictionaries(serializer_data[k], meta_data['children'][k], recursion_data[k])
            else:
                # print('Recursion[meta_data] = serializer_data\n')
                # print(recursion_data)
                # print(meta_data)
                # print(serializer_data)
                recursion_data['val'] = serializer_data

                # recursion_data[meta_data] = serializer_data




            # pass

        
        '''


        merge_dictionaries(ser_data, data, merged_data)

        
        '''

        # def merge_json(ser_data, data):
        #     counter = 0
        for k, v in ser_data.items():
            # counter = counter + 1
            # print(counter)
            meta_values = data.get(k, None)
            ser_data_values = ser_data.get(k, None)
            merged_data[k] = meta_values
            # if merged_data[k]['type'] == 'nested object':
            if isinstance(v, dict):
                print(merged_data[k])
                # merge_json(ser_data[k], data[k])
            
                # for key, val in merged_data[k].items():
                #     # print(key, '\n', val)
                #     print('tt')
            
                # print('NESTED')
                # print(type(merged_data[k]))
            else:

                # merged_data[k]['VALUE'] = ser_data_values
                print('to')
        
        # merge_json(ser_data, data)
        # print(merged_data)
        '''

        '''
        print(data['actions']['PUT'].keys(), '\n')
        for k, v in data['actions']['PUT'].items():
            for key, val in ser_data.items():
                if k == key:
                #     print(k)
                #     print(v)
                #     print(key)
                #     print(val)
                    # merged_data['test']['value'] = val
                    # merged_data[k]['value'] = val
                    merged_data[k] = v
                    # merged_data[k].update('value', val)
                    # print(merged_data[k], '\n')
                    
                    
        # print(merged_data['last_name'])
        print(ser_data)

        '''
        return Response({
            # 'serializer': ser_data,
            # 'data': data,
            'merged' : merged_data
        })
        # return Response(ser_data)
        # return super().retrieve(*args, **kwargs)

    def update(self, *args, **kwargs):
        instance = Customer.objects.get(pk=kwargs['pk'])
        serializer = self.get_serializer(instance=instance, data=self.request.data, partial=True, fields=self.fields)
        print(self.request.data)
        # super().update(*args, **kwargs)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def patch(self, *args, **kwargs):
        return self.partial_update(self.request, *args, **kwargs)

    def put(self, *args, **kwargs):
        return self.update(self.request, *args, **kwargs)

    def options(self, *args, **kwargs):
        return self.get(self, *args, **kwargs)



    # def perform_update(self, serializer):
    #     instance = serializer.save()

# class CustomerUpdateApiView(UpdateModelMixin, GenericAPIView):

#     def update(self, request, *args, **kwargs):
#         instance = Customer.objects.get(id=kwargs['pk'])
#         customer_ser_inst = CustomerSerializer(instance=instance, data=request.data)



class CustomerUpdateFetchApiView(RetrieveModelMixin,
                                UpdateModelMixin,
                                GenericAPIView):

    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    

    field_params = {
        'basic' : [
            'first_name',
            'last_name',
            'martial_status',
            'id_passport',
        ],
        'contact' : [
            'adress',
            'phone_no',
            'email',
        ],
        'workplace': [
            'workplace',
            'job_posistion',
            'salaty',
            'esd',

        ]
    }
    # def get_serializer_context(self):
    #     mode = self.request.query_params.get('mode', default=None)
    #     return mode


    def get(self, request, *args, **kwargs):
        # print(self.request.GET.get('mode'))
        print(request)
        print(request.data)
        pk = kwargs['pk']
        instance = Customer.objects.get(pk=pk)
        mode = request.query_params.get('mode', default=None)


        data = CustomerSerializer(instance=instance, fields=self.field_params[mode]).data

        return Response(data)
        

    # def put(self, *args, **kwargs):
    #     return super().partial_update(self.request, *args, **kwargs)



    def partial_update(self, request, *args, **kwargs):
        instance = Customer.objects.get(pk=kwargs['pk'])
        mode = request.query_params.get('mode', default=None)
        serializer = self.get_serializer(instance=instance, 
                                        data=self.request.data, partial=True, 
                                        fields=self.field_params[mode])
        # print(self.request.data)
        # super().update(*args, **kwargs)
        if serializer.is_valid():
            self.perform_update(serializer=serializer)
            # serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        # return super().partial_update(request, *args, **kwargs)


    def patch(self, request, *args, **kwargs):
        # pk = kwargs['pk']
        # instance = Customer.objects.get(pk=pk)
        # mode = self.request.query_params.get('mode', default=None)
        # serializer = self.get_serializer(instance, data=request.data, fields=['first_name', 'last_name'])
        # return self.partial_update(request, serializer)
        return self.partial_update(request, *args, **kwargs)    
