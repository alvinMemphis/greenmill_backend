from rest_framework import serializers, fields
from greenadmin.models import GreenAdmin
from hubmanager.models import LogicHub, HubManager
 
 

class LogicHubSerializer(serializers.ModelSerializer):
    hubowner = serializers.PrimaryKeyRelatedField(
        queryset=GreenAdmin.objects.all(),
        required=False, 
        allow_null=True, 
        default=None
    )

    hubmanager = serializers.PrimaryKeyRelatedField(
        queryset=HubManager.objects.all(),
        required=False, 
        allow_null=True, 
        default=None
    )

    class Meta:
        model = LogicHub
        fields = ('hubname','hubowner', 'hubmanager')

    
    def validate_hubowner(self, value):
        return GreenAdmin.objects.get(user=self.context['request'].user) 



class AssignHubMangerSerializer(serializers.Serializer):
    
    hubname = serializers.CharField()
    
    hubowner = serializers.PrimaryKeyRelatedField(
        queryset=GreenAdmin.objects.all(),
        required=False, 
        allow_null=True, 
        default=None
    )

    hubmanager = serializers.PrimaryKeyRelatedField(
        queryset=HubManager.objects.all(),
        required=False, 
        allow_null=True, 
        default=None
    )

    class Meta:
        fields = ('hubname','hubowner', 'hubmanager')

    def validate(self, attrs):
    
        hubname = attrs.get('hubname')
        hubowner = GreenAdmin.objects.get(user=self.context['request'].user)
        # hubmanager = attrs.get('hubmanager')
        hubmanager = HubManager.objects.get(id=1)

        logichub = LogicHub.objects.filter(hubname=hubname, hubowner=hubowner)[0]
        if hubmanager is not None:
            logichub.hubmanager = hubmanager        
        logichub.save()

        return attrs
    



