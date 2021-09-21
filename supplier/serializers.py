from rest_framework import serializers, fields
from supplier.models import Package, Supplier

from person.models import GreenUser

class SupplierSerializer(serializers.ModelSerializer):

    

    class Meta:
        model = GreenUser

        fields = ('email', 'user_name','user_type','date_joined')
        def create(self, validated_data):
            mvalid = validated_data.copy()
            mvalid.pop('user_type')
            mvalid['user_type'] = 'supplier'
            user = GreenUser.objects.create_user(user_type='supplier',**mvalid)
            user.user_type='supplier'
            user.set_password("boystomen")
            user.save()
            return user

    def get_auth_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        return str(refresh.access_token)

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

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('orderstat')
        # Unless the application properly enforces that this field is
        # always set, the following could raise a `DoesNotExist`, which
        # would need to be handled.
        
        instance.orderstat = profile_data
        instance.save()
        return instance









