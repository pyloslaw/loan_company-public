from django.contrib import admin
from .models import (Customer, Adress, Workplace, Product, UserInfo,
                    Payment)
                    # ProductBankAccount)
# Register your models here.

admin.site.register(Adress)
admin.site.register(Workplace)





class ProductAdmin(admin.ModelAdmin):
    list_display = [
                    'id', 
                    'product_name', 
                    'created_date', 
                    'installments_dec',
                    'total_amount_dec',
                    'amount_requested',
                    'loan_period',
                    ]
    readonly_fields = ['created_date', 'id', 'days_since_create',
                    'total_amount_dec',
                    'installments_dec',
                    'installement_schedule', 
                    'installment_dict',
                    'get_payments',
                    # 'payments_amounts',
                    'paid_total',
                    'paid_by_day',
                    'inst_sch',
                    'payments_human',
                    'paid_by_day_human',
                    'create_schedule',
                    'schedule_human'                    
                    ]
'''
class ProductBankAccAdmin(admin.ModelAdmin):
    list_display = [
        'product',
        'account_no',
        # 'pay_installment'
    ]

    readonly_fields = [
        'paid_installments',
        'paid_total',
        # 'pay_installment',
        'paid_total'
    ]

'''

class PaymentAdmin(admin.ModelAdmin):
    readonly_fields = ['created_date']

class UserInfoAdmin(admin.ModelAdmin):
    readonly_fields = ['created_date', 'id']

class CustomerAdmin(admin.ModelAdmin):
    readonly_fields = ['created_date', 'id']

admin.site.register(Payment, PaymentAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(Customer, CustomerAdmin)
# admin.site.register(ProductBankAccount, ProductBankAccAdmin)