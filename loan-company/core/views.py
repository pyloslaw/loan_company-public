import json
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.response import TemplateResponse
from django.views.generic import (CreateView, DetailView, ListView,
                                TemplateView, UpdateView,)
from django.views.generic.edit import BaseUpdateView
from .models import Customer, Adress, UserInfo
from .forms import (CustCreatePersonalInfo, CustCreateAdressForm,
                    CustomSignUpForm, CustomWorkplaceForm,
                    AddNewProductForm, CustCreatePersonalInfoUpdate,
                    ChangeUsername)
from django.views import View
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import (PasswordChangeView,
                                PasswordChangeDoneView, PasswordResetView,
                                PasswordResetDoneView, PasswordResetConfirmView)                                                                    
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

'''
### Trying Inline Formset ###
from django.forms.models import inlineformset_factory

UserInfoFormSet = inlineformset_factory(User, UserInfo, fields='__all__')
'''


def index(request): 
  

    return render(request, 'base.html')

@login_required
def create_customer(request):
    return render(request, 'core/create_customer.html')

class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    fields = '__all__'

#     def form_valid(self, form):
#         form.instance.adress_id = self.kwargs.get('pk')
#         return super(CustomerCreateView, self).form_valid(form)

# class AdressCreateView(CreateView):
#     model = Adress
#     fields = '__all__'

@login_required
def custom_customer(request):

    customer_form = CustCreatePersonalInfo(request.POST)
    customer_adress = CustCreateAdressForm(request.POST, prefix='customer_adress')
    workplace_adr_form = CustCreateAdressForm(request.POST, prefix='workplace_adr_form')    #prefix dlatego bo jest adress 2 instatncje - workplace i zwykly !!
    workplace_form = CustomWorkplaceForm(request.POST)
    pesel_check = request.GET.get('pesel')
    

    if request.method == 'GET' and pesel_check:
        try:
            cust_obj = Customer.objects.get(social_security_no_pesel=pesel_check)
            customer_data = serializers.serialize('json', [cust_obj])
            customer_adr = serializers.serialize('json', [cust_obj.adress])
            workplace_data = serializers.serialize('json', [cust_obj.workplace])
            workplace_adress_data = serializers.serialize('json', [cust_obj.workplace.adress])
            customer_creator = UserInfo.objects.get(user=cust_obj.created_by.id)

            json_list = [customer_data, customer_adr, workplace_data, workplace_adress_data]
            data_2 = []
            for item in json_list:
                data_2.extend(json.loads(item))

            data_2.append({
                'creator_first_name' : customer_creator.first_name,
                'creator_last_name' : customer_creator.last_name
                })

            merged_json = json.dumps(data_2, indent=2)

            # print(merged_json)
            return HttpResponse(merged_json, content_type='application/json')

        except:
            print('BRAK')
            context = {
                'customer_form': customer_form,
                'customer_adress': customer_adress,
                'workplace_adr_form': workplace_adr_form,
                'workplace_form': workplace_form,
            }
            # return HttpResponse('Error')
            return render(request, 'core/custom_create.html', context) 
    
    
    if request.method == 'POST' and request.POST.get('customer_id_value') == '':


        if customer_form.is_valid() and customer_adress.is_valid() and workplace_adr_form.is_valid() and workplace_form.is_valid():

            
            x = customer_form.save(commit=False)
            z = customer_adress.save(commit=False)
            y = workplace_adr_form.save(commit=False)
            q = workplace_form.save(commit=False)
            
            x.created_by = request.user
            x.adress = z
            q.adress = y
            x.workplace = q

            z.save()            
            y.save()
            q.save()
            x.save()

            return redirect('customer_detail', pk=x.id)

        else:
            context = {
                'customer_form': customer_form,
                'customer_adress': customer_adress,
                'workplace_adr_form': workplace_adr_form,
                'workplace_form': workplace_form,
            }


            return render(request, 'core/custom_create.html', context)

            
    elif request.method == 'POST' and request.POST.get('customer_id_value') != '':

        customer_id = request.POST.get('customer_id_value')
        customer_instance = Customer.objects.get(id=customer_id)

        cust_update = CustCreatePersonalInfoUpdate(request.POST, instance=customer_instance)
        cust_adress_update = CustCreateAdressForm(request.POST, prefix='customer_adress', instance=customer_instance.adress)
        workplace_adr_update = CustCreateAdressForm(request.POST, prefix='customer_adress', instance=customer_instance.workplace.adress)
        workplace_update = CustomWorkplaceForm(request.POST, instance=customer_instance.workplace)


        cust_update.save()
        cust_adress_update.save()
        workplace_adr_update.save()
        workplace_update.save()
        
        return redirect('customer_detail', pk=customer_id)   
    
    
    else:
        context = {
            'customer_form': customer_form,
            'customer_adress': customer_adress,
            'workplace_adr_form': workplace_adr_form,
            'workplace_form': workplace_form,
        }

        return render(request, 'core/custom_create.html', context)


        ### SKROCIC TO - ZROBIC LADNIEJSZE, EFEKTYWNE BARDZIEJ ###

    

    
class RegisterUser(View):
    user_info_form = CustomSignUpForm
    user_create_form = UserCreationForm
    user_adress_form = CustCreateAdressForm
    template_name = 'registration/sign_up.html'
    initial =   {
                'user_info_form': user_info_form,
                'user_create_form': user_create_form,
                'user_adress_form': user_adress_form,
                }

    def get(self, request):
        self.user_create_form(initial = self.initial)
        self.user_info_form(initial = self.initial)
        self.user_adress_form(initial=self.initial)
        return render(request, self.template_name, self.initial)

    def post(self, request):
        
        user_info = self.user_info_form(request.POST, request.FILES or None)
        user_create = self.user_create_form(request.POST)
        user_adress = self.user_adress_form(request.POST)
        if user_info.is_valid() and user_create.is_valid():
            z = user_info.save(commit=False)
            x = user_create.save(commit=False)
            y = user_adress.save(commit=False)
            z.adress = y
            z.user = x
            x.save()
            y.save()
            z.save()

            # WYMYSLIC KROTSZA WERSJĘ !!! !! z comitem itd 

            return HttpResponseRedirect(reverse('index'))

        return render(request, self.template_name, self.initial)
            


class UserProfileView(LoginRequiredMixin, DetailView):

    model = UserInfo
    fields = '__all__'
    template_name = 'registration/profile.html'
    queryset = UserInfo.objects.all()
    # pk_url_kwarg = 'id'

    def get_object(self, queryset=None):
        queryset = self.queryset
        id = self.kwargs['id']
        obj = queryset.get(user=id)
        return obj


    def get(self, *args, **kwargs):
        id = self.kwargs['id']
        current_user = self.request.user.id

        if current_user != id:
            return render(self.request, self.template_name, context={'massage': 'You dont have permissions to see that !!'})
        return super().get(*args, **kwargs)





#### Experimenting... ####
class UserProfileEditView(LoginRequiredMixin, UpdateView):
    queryset = UserInfo.objects.all()
    template_name = 'registration/profile_edit.html'
    fields = '__all__'
    


    def get_object(self, *args, **kwargs):
        queryset = self.queryset
        id = self.kwargs['id']
        obj = queryset.get(user=id)
        return obj
    
    
    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data['user_info'] = CustomSignUpForm(instance=self.object)
        data['user_adress'] = CustCreateAdressForm(instance=self.object.adress)
        data['user_basic'] = ChangeUsername(instance=self.object.user)
        '''
        if self.request.POST:
            data['user_info'] = CustomSignUpForm(self.request.POST, instance=self.object)
            data['user_adress'] = CustCreateAdressForm(self.request.POST, instance=self.object.adress)
            # data['user_basic'] = UserCreationForm(self.request.POST, instance=self.object.user)
        else:
            data['user_info'] = CustomSignUpForm(instance=self.object)
            data['user_adress'] = CustCreateAdressForm(instance=self.object.adress)
            # data['user_basic'] = UserCreationForm(instance=self.object.user)
        '''
        if self.kwargs['id'] != self.request.user.id:
            raise PermissionDenied
        return data

    def post(self, request, *args, **kwargs):
        object = self.get_object()
        forms = [
        CustCreateAdressForm(self.request.POST, instance=object.adress),
        ChangeUsername(self.request.POST, instance=object.user),
        CustomSignUpForm(self.request.POST, self.request.FILES or None,  instance=object)
        ]
        for form in forms:
            if form.is_valid():
                form.save()
                # print(form)
            else:
                return render(request, self.template_name, context={
                    'user_info':CustomSignUpForm(self.request.POST, self.request.FILES or None, instance=object),
                    'user_adress':CustCreateAdressForm(self.request.POST, instance=object.adress),
                    'user_basic':ChangeUsername(self.request.POST, instance=object.user)
                })
        return redirect('user_profile', id=self.kwargs['id'])

    # def form_valid(self, form):
    #     context = self.get_context_data()
    #     userinfo = context['user_info']
    #     useradress = context['user_adress']
    #     print(userinfo)
    #     print(form)
    #     self.object = form.save()
    #     if userinfo.is_valid() and useradress.is_valid():
    #         print('OK')
    #         useradress.save()
    #         userinfo.save()
    #     else:
    #         print('NOT OK')
            
        
    #     return super().form_valid(form)


    # def get(self, request, *args, **kwargs):
    #     print(self.kwargs)
    #     print(self.request)
    #     print(self.args)
    #     print(self.form_class)
    #     return super().get(request, *args, **kwargs)

    # pass

class UserChangePassword(LoginRequiredMixin, PasswordChangeView):
    template_name = 'registration/password_change.html'
    # success_url = reverse_lazy('user_password_done', kwargs={'id': })

    def get_success_url(self, *args, **kwargs):
        id = self.kwargs['id']
        print(id)
        return reverse('user_password_done', kwargs={'id': id})
    

class UserChangePasswordDone(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'registration/password_change_done_new.html'


class UserResetPassword(SuccessMessageMixin, PasswordResetView):
    success_message = 'Email has been sent to %(email)s'
    email_template_name = 'registration/reset_password_email.html'
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('index')
    

class UserResetPasswordForm(PasswordResetConfirmView):
    template_name = 'registration/reset_password_form.html'
    success_url = reverse_lazy('login')

    


'''

### Trying Inline FormSet ###

class UserProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    # fields = '__all__'
    fields = [
        'username',
        'last_login',
        'email'
    ]
    template_name = 'registration/profile_edit.html'
    queryset = User.objects.all()

    def get_object(self, queryset=None):
        queryset = self.queryset
        id = self.kwargs['id']
        obj = queryset.get(id=id)
        return obj

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['userinfo'] = UserInfoFormSet(self.request.POST, instance=self.object)
        else:
            data['userinfo'] = UserInfoFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        userinfo = context['userinfo']
        self.object = form.save()
        if userinfo.is_valid():
            userinfo.instance = self.object
            userinfo.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('user_profile', kwargs={'id': self.kwargs['id']})


    
'''



class CustomerListView(LoginRequiredMixin, ListView):

    paginate_by = 8

    def get_queryset(self):

        default_order = ['-created_date']
        order = self.request.GET.getlist('order_by', default_order)
        # print(self.request.GET)
        # print(order)
        return Customer.objects.filter(created_by=self.request.user.id).order_by(*order)

    
class CustomerDetailView(LoginRequiredMixin, DetailView):

    model = Customer
    template_name = 'core/customer_detail.html'


## using Django Rest Framework for update
'''

class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'core/customer_update.html'


    ### The same as model = Customer ###


    # def get_object(self):
        # self.object = Customer.objects.get(pk=self.kwargs['pk'])
        # print(self.object)
        # print('test')
        # return Customer.objects.get(pk=self.kwargs['pk'])

    # fields = field_choice['some']
    # initial = {'first_name' : Customer.objects.get(pk=self.kwargs['pk']).first_name}

    ### End ###
    
    basic_form = CustCreatePersonalInfoUpdate
    adress_form = CustCreateAdressForm
    workplace_form = CustomWorkplaceForm

    


    def get(self, request, pk):
        mode = self.request.GET.getlist('mode', default=None)
        object = Customer.objects.get(pk=self.kwargs['pk'])

        basic_form_inst = self.basic_form()
        adress_form_inst = self.adress_form()
        workplace_form_inst = self.workplace_form()
        
        # basic_initial = {}
        # for f in basic_form_inst.fields.keys():
        #     basic_initial[str(f)] = getattr(object, f)

        basic_initial = { str(f): getattr(object, f) for f in basic_form_inst.fields.keys() }
        adress_initial = { str(f): getattr(object.adress, f) for f in adress_form_inst.fields.keys() }
        workplace_initial = { str(f): getattr(object.workplace, f) for f in workplace_form_inst.fields.keys() }
        workplace_adress_initial = { str(f): getattr(object.workplace.adress, f) for f in adress_form_inst.fields.keys() }

        context_var = {
            'basic': { 
                'basic' : self.basic_form(initial=basic_initial) },
            'contact' : {
                'adress' : self.adress_form(initial=adress_initial),
                'form': self.basic_form(initial=basic_initial),
                },
            'workplace' : {
                'form': self.basic_form(initial=basic_initial)
                }
    }
        

        if mode[0] == 'basic' and len(mode) == 1:
            print('jeden')
            print(object)

            # print(obj)
            
            return render(request, self.template_name, context=context_var['basic'])
        elif mode[0] == 'contact' and len(mode) == 1:
            print('dwa')
            print(mode)
            print(request.GET)
            # return render(request, self.template_name, context=context_var['contact'])
            print(context_var)
            print(basic_initial)
            return HttpResponse(context_var['basic'], content_type='application/text')

        elif mode[0] == 'workplace' and len(mode) == 1:
            print('cztery')
            print(mode)
            print(request.GET)
            return render(request, self.template_name)
        
        else: 
            print('TRZY else wyszlo')
            print(request.GET)
            return render(request, self.template_name)




    def post(self, request, pk):
        object = Customer.objects.get(pk=self.kwargs['pk'])
        basic_form_post = self.basic_form(request.POST, instance=object)
        adress_form_post = self.adress_form(request.POST, instance=object.adress)
        workplace_form_post = self.workplace_form(request.POST, instance=object.workplace)
        workplace_adress_form_post = self.adress_form(request.POST, instance=object.workplace.adress)
        if basic_form_post.is_valid():
            basic_form_post.save()
            
        if adress_form_post.is_valid():
            adress_form_post.save()
        
        if workplace_form_post.is_valid():
            workplace_form_post.save()

        if workplace_adress_form_post.is_valid():
            workplace_adress_form_post.save()

        return HttpResponseRedirect(reverse('customer_detail', kwargs={'pk':pk}))
        # return redirect('customer_detail', pk=pk)

'''


class AddNewProductView(LoginRequiredMixin, View):

    add_product_form = AddNewProductForm
    template_name = 'core/add_product.html'
    initial = {'add_product': add_product_form }

    def get(self, request, id):    
        self.add_product_form(initial=self.initial)
        customer_instance = Customer.objects.get(id=id)
        return render(request, self.template_name, context={'add_product': self.add_product_form, 'customer_id': customer_instance.id})

    def post(self, request, id):
        customer_instance = Customer.objects.get(id=id)
        add_prod = self.add_product_form(request.POST)
        if add_prod.is_valid():
            s = add_prod.save(commit=False)
            s.owner = customer_instance
            s.save()
            return redirect('customer_detail', pk=id)
        else:
            return render(request, self.template_name, self.initial)

class jsonTestView(View):
    def get(self, request):

        pesel = 21241411111     


        cust_obj = Customer.objects.get(social_security_no_pesel=pesel)

        customer_data = serializers.serialize('json', {cust_obj})
        customer_adress = serializers.serialize('json', [cust_obj.adress])
        workplace_data = serializers.serialize('json', [cust_obj.workplace])
        workplace_adress_data = serializers.serialize('json', [cust_obj.workplace.adress])

        json_list = [customer_data, customer_adress, workplace_data, workplace_adress_data]
        data_2 = []
        for item in json_list:
            data_2.extend(json.loads(item))

        merged_json = json.dumps(data_2, indent=2)

        context = {

            'customer' : merged_json
        }

        # return render(request, 'core/test.html', context=context)
        # return JsonResponse(context, safe=False, json_dumps_params={'indent':'    '})
        return HttpResponse(merged_json, content_type='application/json')
    
