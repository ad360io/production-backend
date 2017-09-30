from rest_framework import serializers
from qchain_backend.models import Agent, Website, Adspace, Ad, Contract, \
Stat, RequestForAdv

class AdspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adspace
        fields = "__all__"

class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = "__all__"

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"

class RequestForAdvSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestForAdv
        fields = "__all__"

class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = "__all__"

class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = "__all__"
