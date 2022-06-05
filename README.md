# Miare-Couriers-Income-System
This Projects Stores and Updates dynamic data about the daily and weekly income of a Miare Courier. 

# Structure and Models:
There are 6 models that represent different entities in the system,
Im going to describe these entities and their connection. 

# Courier Model
We represent couriers with a model called "Courier".
This Model only has one filed (name) and acts as a foreign key for all other tables.

# Income-Models
There are three factors that would have direct impact on daily and weekly income that a courier has.
We represent them as 3 seprate models and informally call them "Income-Models", because they can change couriers income :

# Trip Model
This is the first Income-Model that we have, it has 3 fileds (courier, date, wage) and courier is its foreign key, because a courier can have lot of Trips
but each Trip, only belongs to a specific courier (Many-To-One relationship). Every time we save a new intance of this object in database, we have to also add its instance.wage to its related day in dailywage table. if there were no records already in DailyWage, We Create a new one.

# WageReduction Model
This is the second Income-Model that we have, it has 3 fileds (courier, date, reduction_amount) and courier is its foreign key, because a courier can have lot of
WageReductions but each WageReduction, only belongs to a specific courier (Many-To-One relationship). Every time we save a new intance of this object in database, we have to also substract its instance.reduction_amount from its related day in dailywage table. if there were no records already in DailyWage, We Create a new one.

# WageIncrement Model
This is the third Income-Model that we have, it has 3 fileds (courier, date, increment_amount) and courier is its foreign key, because a courier can have lot of
WageIncrements but each WageIncrement, only belongs to a specific courier (Many-To-One relationship). Every time we save a new intance of this object in database, we have to also add its instance.increment_amount to its related day in dailywage table. if there were no records already in DailyWage, We Create a new one.

# DailyWage Model
It Has 3 fields (courier, date, wage). This Model is slightly different from three above models, because its wage record is in fact the sum of all the "Incom-Models" wages in a specific day. whenever we try to add a Trip or WageReduction or WageIncrement to database, we have to add this new record's income to the DailyWage.wage (Except WageReduction, in this case we have to substract it from that day wages). 
the only table which would be affected by changes in this model is the WeeklyWage Model (Which I'll explain it in next few lines). the other important difference about this model in comparing to other models, is that it has a special constraint.
This constarint lies in two fileds of it, which are courier and date. in Other words we can not have two same rows in this table with same courier AND same date (This condition Would violate the logical and conceptual idea of ingerity of database) 

# WeeklyWage Model
The Last Model in our system,It has three fields (courier, saturday_date, wage). It aggregates all wages of the days of the same week, from dailywage table and save the result in wage field. Therefore every time we update our dailywage table we need to update weeklywage table too. The last important thing that we shoud consider is that courier and saturday fields are constraint, so we can't have two rows in the table which are in the same week and are for a same courier!


# WorkFlow
# HOW TO UPDATE DAILYWAGE TABLE?
Users only have access to make new "Income-Models"(which were Trip or WageIncrement or WageReduction). after they created one instance from one of these three 
models, next step is to check if we have a related dailywage record or not, if we didn't have any dailywage record which had the same courier as our instance.courier and same date as our instance.date, we would create such a daily record with these properties and save it, and if we had a dailywage record which had the same courier as our instance.courier and same date as our instance.date, we update this instance.wage and save it. All three "Income-Models" have methods to perform this action after there was made a new instance from one of them.

# HOW TO UPDATE WEEKLYWAGE TABLE?
Whenever we update DailyWage, we have to update the WeeklyWage table too, that is why there is a method inside DailyWage model and if after making a new DailyWge instance, we call it, it would check all the week changes in the same week as DailyWage new insatnce's week and updates WeeklyWage.

# Saving_flow_manager(), Serializers, Viewsets and ......
I would continue to make this documention more complete...