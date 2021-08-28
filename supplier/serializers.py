from rest_framework import serializers, fields
from supplier.models import Package, Supplier


class PackageSerializer(serializers.ModelSerializer):
    orderstat = fields.ChoiceField(Package.ORDER_TYPE_STATUS)
    supplier = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(),
        required=False, 
        allow_null=True, 
        default=None
    )

    class Meta:
        model = Package
        fields = ('packagename','supplier', 'delivery_date', 'orderstat', 'to_customer_name', 'to_customer_email')

    
    def validate_supplier(self, value):
        return self.context['request'].user







