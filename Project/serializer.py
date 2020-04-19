from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from Project.models import *
#
# class FileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = File
#         fields = "__all__"



class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = "__all__"
class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = "__all__"

class AdverticementSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    class Meta:
        model = Adverticements
        fields = "__all__"

class AdsSerializer(serializers.ModelSerializer):
    ads_img = SerializerMethodField()
    class Meta:
        model = Ads
        fields = "__all__"

    def get_ads_img(self, obj):
        newobj = Adverticements.objects.filter(range=obj.age,gender=obj.gender)
        if newobj.exists():
            response = AdverticementSerializer(newobj, many=True)
            return response.data
        else:
            print("0 ads ")
            return 0
