from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from common.drf.serializers import MethodSerializer
from common.utils import get_object_or_none
from orgs.mixins.serializers import BulkOrgResourceModelSerializer
from ..models import Account, AccountType


__all__ = ['AccountSerializer']


class AccountSerializer(BulkOrgResourceModelSerializer):
    type_display = serializers.CharField(
        source='type.name', read_only=True, label=_('Type display')
    )
    safe_display = serializers.CharField(
        source='safe.name', read_only=True, label=_('Safe display')
    )
    attrs = MethodSerializer()

    class Meta:
        model = Account
        fields = [
            'id', 'name', 'username', 'secret', 'address', 'type', 'type_display', 'attrs',
            'is_privileged', 'comment', 'safe', 'safe_display',
        ]
        extra_kwargs = {
            'secret': {'read_only': True}
        }

    def get_attrs_serializer(self):
        if isinstance(self.instance, Account):
            account_type = self.instance.type
        else:
            tp = self.context['request'].query_params.get('account_type')
            account_type = get_object_or_none(AccountType, name=tp)

        if account_type:
            serializer_class = account_type.construct_serializer_cls_by_fields_definition()
            serializer = serializer_class()
        else:
            serializer = serializers.JSONField()

        return serializer
