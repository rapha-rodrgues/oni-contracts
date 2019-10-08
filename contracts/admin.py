from django.contrib import admin
from contracts.models import Contract, Payment, Bank


class PaymentInline(admin.StackedInline):
    model = Payment
    can_delete = False
    verbose_name_plural = 'Payment'
    fk_name = 'contract_id'


class ContractAdmin(admin.ModelAdmin):
    inlines = (PaymentInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(ContractAdmin, self).get_inline_instances(request, obj)


admin.site.register(Contract, ContractAdmin)
admin.site.register(Bank)
admin.site.register(Payment)
