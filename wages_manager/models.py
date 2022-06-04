# The application model part, consists of 6 models.
# A Courier which is a foreign key for all other models,
# Then we have Trip, WageRedcution and WageIncrement,
# These three models can affect total income of a courier.
# Therefore we would sometimes,
# call them 'Income-models' in here and other sections.
# And at last but not least we have Dailywage and WeeklyWage table
# These two tables will be updated each time an Income-model changes.


from django.db import models
from datetime import timedelta, date


class Courier(models.Model):
    """Represents the Courier entity"""
    name = models.CharField(max_length=70)

    def __str__(self):
        """Returns a string format of the model"""
        return f"{self.name.title()}" 


class Trip(models.Model):
    """Represents the trip entity"""
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    wage = models.PositiveIntegerField(default=0)

    def update_dailywage(self):
        """
        Updates existing or creates new objects in the DailyWage table,
        Then saves these new or updated objects in DailyWage table
        """
        
        updated_dailywage, is_created = DailyWage.objects.get_or_create(
            courier=self.courier,
            date=self.date,
            defaults={"wage" : self.wage}
        )
        # Update wage amount, if updated_dailywage is not a new record
        if not is_created:
            updated_dailywage.wage += self.wage
            updated_dailywage.save()

        return updated_dailywage

    def __str__(self):
        """Returns a string format of the model"""
        return f"({self.courier}, {self.date}, {self.wage})"


class WageReduction(models.Model):
    """Represents the wage reductions entity"""
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    reduction_amount = models.IntegerField(default=0)

    def update_dailywage(self):
        """
        Updates existing or creates new objects in the DailyWage table,
        Then saves these new or updated objects in DailyWage table
        """
        
        updated_dailywage, is_created = DailyWage.objects.get_or_create(
            courier=self.courier,
            date=self.date,
            defaults={"wage" : -abs(self.reduction_amount)}
        )
        # Update wage amount, if updated_dailywage is not a new record
        if not is_created:
            updated_dailywage.wage -= (abs(self.reduction_amount))
            updated_dailywage.save()

        return updated_dailywage

    def __str__(self):
        """Returns a string format of the model"""
        return f"({self.courier}, {self.date}, {self.reduction_amount})"
    

class WageIncrement(models.Model):
    """Represents the wage Increments entity"""
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    increment_amount = models.PositiveIntegerField(default=0)

    def update_dailywage(self):
        """
        Updates existing or creates new objects in the DailyWage table,
        Then saves these new or updated objects in DailyWage table
        """

        updated_dailywage, is_created = DailyWage.objects.get_or_create(
            courier=self.courier,
            date=self.date,
            defaults={"wage" : self.increment_amount}
        )
        # Update wage amount, if updated_dailywage is not a new record
        if not is_created:
            updated_dailywage.wage += self.increment_amount
            updated_dailywage.save()

        return updated_dailywage

    def __str__(self):
        """Returns a string format of the model"""
        return f"({self.courier}, {self.date}, {self.increment_amount})"


class DailyWage(models.Model):
    """Data about the income that each courier had during a specific day"""
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    date = models.DateField()
    wage = models.IntegerField(default=0)

    # Calling update_dailywage() concurrently may lead 
    # To a race condition which causes data redundancy. 
    # To prevent this, we define unique courier and date fields
    
    class Meta:
        """Set courier and date together, as unique feilds"""
        constraints = [
            models.UniqueConstraint(
                fields=["courier", "date"],
                name="unique_courier_and_date",
            )
        ]

    def update_weeklywage(self):
        """
        Updates existing or creates new objects in the WeeklyWage table,
        Then saves these new or updated objects in WeeklyWage table
        """

        # We need to find the date of the saturday,
        # Which this new record's week starts with

        # DailyWage record's weekday is itself, saturday
        if self.date.weekday() == 5:
            saturday_date = self.date
        # DailyWage record's weekday is sunday
        elif self.date.weekday() == 6:
            saturday_date = self.date - timedelta(days=1)
        # DailyWage record's weekday is between monday and friday
        else:
            saturday_date = self.date - timedelta(days=self.date.weekday()+2)

        updated_weeklywage, is_created = WeeklyWage.objects.get_or_create(
            courier=self.courier,
            saturday_date=saturday_date,
            defaults={"wage" : self.wage}
        )

        if not is_created:
            date = ''
            total_wage = 0
            # We should calculate sum of wages of all the days,
            # That are in the same week with instance's week
            for i in range(0,7):
                date = saturday_date + timedelta(days=i)
                day_total_wage = DailyWage.objects.filter(courier=self.courier, date=date).aggregate(models.Sum('wage'))['wage__sum']
                
                if day_total_wage != None:
                    total_wage += day_total_wage

            updated_weeklywage.wage = total_wage
            updated_weeklywage.save()

    def __str__(self):
        """Returns a string format of the model"""
        return f"({self.courier}, {self.date}, {self.wage})"


class WeeklyWage(models.Model):
    """Data about the income that each courier had during a specific week"""
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    saturday_date = models.DateField()
    wage = models.IntegerField(default=0)

    class Meta:
        """Set courier and saturday_date together, as unique feilds"""
        constraints = [
            models.UniqueConstraint(
                fields=["courier", "saturday_date"],
                name="unique_courier_and_saturday_date",
            )
        ]

    def __str__(self):
        """Returns a string format of the model"""
        return f"({self.courier}, {self.saturday_date}, {self.wage})"