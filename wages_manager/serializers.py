from rest_framework import serializers

from .models import ( 
    Courier,
    Trip,
    WageReduction,
    WageIncrement,
    DailyWage,
    WeeklyWage
)


class CourierSerializer(serializers.ModelSerializer):
    """This class Serializes all fileds of Courier model"""
    class Meta:
        model = Courier
        fields = '__all__'


class TripSerializer(serializers.ModelSerializer):
    """This class Serializes all fileds of Trip model"""
    class Meta:
        model = Trip
        fields = '__all__'


class WageReductionSerializer(serializers.ModelSerializer):
    """This class Serializes all fileds of WageRedcution model"""
    class Meta:
        model = WageReduction
        fields = '__all__'


class WageIncrementSerializer(serializers.ModelSerializer):
    """This class Serializes all fileds of WageIncrement model"""
    class Meta:
        model = WageIncrement
        fields = '__all__'


class DailyWageSerializer(serializers.ModelSerializer):
    """This class Serializes all fileds of DailyWage model"""
    class Meta:
        model = DailyWage
        fields = '__all__'


class WeeklyWageSerializer(serializers.ModelSerializer):
    """This class Serializes all fileds of WeeklyWage model"""
    courier = CourierSerializer()

    class Meta:
        model = WeeklyWage
        fields = '__all__'


class DateRangeSerializer(serializers.Serializer):
    """This class from_date and to_date fields"""
    from_date = serializers.DateField()
    to_date = serializers.DateField()