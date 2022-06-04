from rest_framework.mixins import (ListModelMixin, RetrieveModelMixin, CreateModelMixin)
from rest_framework.viewsets import GenericViewSet
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.db import transaction
from .models import (Courier,
                     Trip,
                     WageReduction,
                     WageIncrement,
                     DailyWage,
                     WeeklyWage)

from .serializers import (CourierSerializer,
                          TripSerializer,
                          WageReductionSerializer,
                          WageIncrementSerializer,
                          DailyWageSerializer, 
                          WeeklyWageSerializer, 
                          DateRangeSerializer)


def saving_flow_manager(income_obj) -> bool:
    """
    A fucntion to save objects with classes that,
    Affect income(Trip, WageIncrement, WageReduction),
    And then update DailyWage and WeeklyWage table, respectively.
    Its only parameter, is the 'income-model' object,
    which can be an instance of Trip or WageIncrement or WageReduction.
    Returns True if all savings, are commited successfully. otherwise returns False.
    """

    try :
        # RollBack all database changes if an update goes wrong
        with transaction.atomic(durable=True):
            income_obj.save()
            new_dailywage = income_obj.update_dailywage()
            new_dailywage.update_weeklywage()
    except:
        # DB changes have been ignored, sending a flag to handle the exception
        return False

    # All savings are commmited successfully
    return True


class CustomViewSet1(ListModelMixin ,RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    # A customViewSet, which other ViewSets inherit from,
    # This one can do the followings:
    # 1-Gets all instances 2-Gets one insatnce 3-Creates a new instance
    pass


class CustomViewSet2(ListModelMixin ,RetrieveModelMixin, GenericViewSet):
    # A customViewSet, which DailyWageViewSet inherit from,
    # This one can do the followings:
    # 1-Gets all instances 2-Gets one insatnce
    pass


class CourierViewSet(CustomViewSet1):
    """This class handles post and get requests, related to Courier table"""
    serializer_class = CourierSerializer
    queryset = Courier.objects.all()


class TripViewSet(CustomViewSet1):
    """This class handles post and get requests, related to Trip table"""
    serializer_class = TripSerializer
    queryset = Trip.objects.all()

    # This method Ooerrides create method, 
    # so we would have control on the flow of saving new objects
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Making new trip object based on valid serilizer parameters
        trip = Trip(courier=serializer.validated_data['courier'],
                    date=serializer.validated_data['date'],
                    wage=serializer.validated_data['wage'])
        
        # Saving new Trip object, then updating DailyWage and WeeklyWage table
        save_result = saving_flow_manager(trip)
        if save_result == False :
            return Response("The creation of Trip object FAILED.")
        else:
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class WageReductionViewSet(CustomViewSet1):
    """This class handles post and get requests, related to WageReduction table"""
    serializer_class = WageReductionSerializer
    queryset = WageReduction.objects.all()

    # This method Ooerrides create method, 
    # so we would have control on the flow of saving new objects
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Making new WageReduction object based on valid serilizer parameters
        wage_reduction = WageReduction(courier=serializer.validated_data['courier'],
                                      date=serializer.validated_data['date'],
                                      reduction_amount=serializer.validated_data['reduction_amount'])
        
        # Saving new WageReduction object, then updating DailyWage and WeeklyWage table
        save_result = saving_flow_manager(wage_reduction)
        if save_result == False :
            return Response("The creation of WageReduction object FAILED.")
        else:
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class DailyWageViewSet(CustomViewSet2):
    """This class handles get requests, related to DailyWage table"""
    serializer_class = DailyWageSerializer
    queryset = DailyWage.objects.all()


class WageIncrementViewSet(CustomViewSet1):
    """This class handles post and get requests, related to WageIncrement table"""
    serializer_class = WageIncrementSerializer
    queryset = WageIncrement.objects.all()

    # This method Ooerrides create method, 
    # so we would have control on the flow of saving new objects
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Making new WageIncrement object based on valid serilizer parameters
        wage_increment = WageIncrement(courier=serializer.validated_data['courier'],
                                      date=serializer.validated_data['date'],
                                      increment_amount=serializer.validated_data['increment_amount'])
        
        # Saving new WageIncrement object, then updating DailyWage and WeeklyWage table
        save_result = saving_flow_manager(wage_increment)
        if save_result == False :
            return Response("The creation of WageIncrement object FAILED.")
        else:
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class WeeklyWageView(APIView):
    """This class's goal is to make output, based on from_date and to_date"""

    # A post function, so the api user, 
    # Can send from_date and to_date, to server and see the result in response 
    def post(self, request):
        serializer = DateRangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        date_1 = serializer.validated_data['from_date']
        date_2 = serializer.validated_data['to_date']

        final_weeklywage_records = []
        weeklywage_records = WeeklyWage.objects.all()
        for record in weeklywage_records:
            if record.saturday_date >= date_1 and record.saturday_date <= date_2:
                final_weeklywage_records.append(record)
        
        serializer = WeeklyWageSerializer(final_weeklywage_records, many=True)
        
        return Response(serializer.data)
