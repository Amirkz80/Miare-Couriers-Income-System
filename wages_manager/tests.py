from django.test import TestCase
from wages_manager.models import *
from datetime import date

class TripTestCase(TestCase):
    """A class to test functionality of Trip class"""
    def setUp(self) -> None:
        courier = Courier(name="John doe")
        courier.save()

        # A Trip instance to test how update_dailywage(),
        # Makes new dailywage record based on its date and courier
        self.trip_1 = Trip(courier=courier, wage=15)
        self.trip_1.save()

        # A Trip instance to test how update_dailywage(),
        # Updates existing record with same courier and date
        self.trip_2 = Trip(courier=courier, wage=7)
        self.trip_2.save()
        
    def test_update_dailyWage_method(self):
        """The update_dailywage method should update DailyWage records correctly"""

        # Makes new dailywage record
        updated_dailywage_obj = self.trip_1.update_dailywage()
        self.assertEqual(15, updated_dailywage_obj.wage)

        # Updates existing dailywage record
        updated_dailywage_obj = self.trip_2.update_dailywage()        
        self.assertEqual(22, updated_dailywage_obj.wage)


class WageReductionTestCase(TestCase):
    """A class to test functionality of WageReduction class"""
    def setUp(self) -> None:
        courier = Courier(name="John doe")
        courier.save()

        # A WageReduction instance to test how update_dailywage(),
        # Makes new dailywage record based on its date and courier
        self.wage_reduction_1 = WageReduction(courier=courier, reduction_amount=8)
        self.wage_reduction_1.save()

        # A WageReduction instance to test how update_dailywage(),
        # Updates existing record with same courier and date
        self.wage_reduction_2 = WageReduction(courier=courier, reduction_amount=41)
        self.wage_reduction_2.save()
        
    def test_update_dailywage_method(self):
        """The update_dailywage method should update DailyWage records correctly"""

        # Makes new dailywage record
        updated_dailywage_obj = self.wage_reduction_1.update_dailywage()
        self.assertEqual(-8, updated_dailywage_obj.wage)

        # Updates existing dailywage record
        updated_dailywage_obj = self.wage_reduction_2.update_dailywage()        
        self.assertEqual(-49, updated_dailywage_obj.wage)


class WageIncrementTestCase(TestCase):
    """A class to test functionality of WageIncrement class"""
    def setUp(self) -> None:
        courier = Courier(name="John doe")
        courier.save()

        # A WageIncrement instance to test how update_dailywage(),
        # Makes new dailywage record based on its date and courier
        self.wage_increment_1 = WageIncrement(courier=courier, increment_amount=300)
        self.wage_increment_1.save()

        # A WageIncrement instance to test how update_dailywage(),
        # Updates existing record with same courier and date
        self.wage_increment_2 = WageIncrement(courier=courier, increment_amount=16)
        self.wage_increment_2.save()
        
    def test_update_dailywage_method(self):
        """The update_dailywage method should update DailyWage records correctly"""

        # Makes new dailywage record
        updated_dailywage_obj = self.wage_increment_1.update_dailywage()
        self.assertEqual(300, updated_dailywage_obj.wage)

        # Updates existing dailywage record
        updated_dailywage_obj = self.wage_increment_2.update_dailywage()        
        self.assertEqual(316, updated_dailywage_obj.wage)

