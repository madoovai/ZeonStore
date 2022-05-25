from rest_framework import serializers

from store.models import Product


class ProductSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    articul = serializers.CharField(max_length=255)
    discount_price = serializers.IntegerField()
    old_price = serializers.IntegerField()
    description = serializers.CharField()
    fabric_structure = serializers.CharField()
    discount = serializers.IntegerField()
    collection_id = serializers.IntegerField()
    favorite = serializers.BooleanField()

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.articul = validated_data.get('articul', instance.articul)
        instance.discount_price = validated_data.get('discount_price', instance.discount_price)
        instance.old_price = validated_data.get('old_price', instance.old_price)
        instance.description = validated_data.get('description', instance.description)
        instance.fabric_structure = validated_data.get('fabric_structure', instance.fabric_structure)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.collection_id = validated_data.get('collection_id', instance.collection_id)
        instance.favorite = validated_data.get('favorite', instance.favorite)

        instance.save()
        return instance