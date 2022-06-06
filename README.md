# **Miare-Couriers-Income-System**
This Projects Stores and Updates dynamic data about the daily and weekly income of a Miare Courier. 

# Set Up
1. First clone the project into your local machine.  

2. After cloning the project, make a new virtual environment and activate it, then install required packages by using the following command:
```
pip install -r requirements.txt
```  

3. Now make a .env file with the "SECRET_KEY" variable in it, assign your secret key to this var (You can use djecrety tool to make one!)"
```
SECRET_KEY =<YOUR_SECRET_KEY>
```

4. Run a migration command:
```
python manage.py migrate
```

5. Finally run the server by using the following command:
```
python manage.py runserver
```

6. THERE YOU GO 🎉

# Structure and Models
There are 6 models that represent different entities in the system:
1. Courier Model
2. Trip Model
3. WageReduction Model
4. WageIncremnt Model
5. DailyWage Model
6. WeeklyWage Model

## Courier Model
We represent couriers with a model called "Courier".
This Model only has one filed (name) and acts as a foreign key for all other tables.

## **_Income-Model_**
There are three factors that would have direct impact on daily and weekly income that a courier has.  
We represent them as 3 separate models and informally we call them "Income-Models", because they can change courier's income.

## Trip Model
This is the first Income-Model that we have, it has 3 fields (courier, date, wage) and courier is its foreign key, because a courier can have lot of Trips
but each Trip, only belongs to a specific courier (Many-To-One relationship).  
Every time we save a new intance of this object in database, we have to also add instance.wage to its related day in dailywage table. if there were no records already in DailyWage, We Create a new one.

## WageReduction Model
This is the second Income-Model that we have, it has 3 fileds (courier, date, reduction_amount) and courier is its foreign key, because a courier can have lot of
WageReductions but each WageReduction, only belongs to a specific courier (Many-To-One relationship).  
Every time we save a new intance of this object in database, we have to also substract instance.reduction_amount from its related day in dailywage table. if there were no records already in DailyWage, We Create a new one.

## WageIncrement Model
This is the third Income-Model that we have, it has 3 fileds (courier, date, increment_amount) and courier is its foreign key, because a courier can have lot of
WageIncrements but each WageIncrement, only belongs to a specific courier (Many-To-One relationship).  
Every time we save a new intance of this object in database, we have to also add instance.increment_amount to its related day in dailywage table. if there were no records already in DailyWage, We Create a new one.

## DailyWage Model
It Has 3 fields (courier, date, wage).  
This Model is slightly different from above 3 models, because its wage field is in fact the sum of Trip.wage, WageReduction.reduction_amount and WageIncrement,increment_amount in a specific day.  
whenever we try to add a Trip or WageReduction or WageIncrement to database, we have to add this new record's income to the DailyWage.wage (When we add a WageReduction instance, we have to substract it from that day wages).  
The only table which would be affected by changes in this model is WeeklyWage Model. This model has a special constraint.
This constarint lies within two fields of it, which are courier and date. in Other words we can not have two same rows in this table with same courier AND same date (This condition Would violate the logical and conceptual idea of integrity of database, system will raise an IntegrityError exception when it happens.) 

## WeeklyWage Model
The Last Model in our system, It has three fields (courier, saturday_date, wage).  
It aggregates wages of days in the same week from dailywage table, and save the result in the wage field. Therefore every time we update our dailywage table we need to update weeklywage table too. The last important thing that we shoud consider is that courier and saturday fields are constraint, so we can't have two rows in the table which are in the same week and are for a same courier! system will raise an IntegrityError exception when it happens.

# WorkFlow
## HOW TO UPDATE DAILYWAGE TABLE?
Users of the api, only can make new objects that are related to "Income-Models" (which were Trip or WageIncrement or WageReduction).  
after they created one instance from one of these three models, next step is to check if we have a related dailywage record or not.  
if we didn't have any dailywage record which had the same courier as our instance.courier and same date as our instance.date, we would create a new daily record with these properties and save it.  
on the other hand if we had a dailywage record which had the same courier as our instance.courier and same date as our instance.date, we update this instance.wage and save it in the database.  
All three "Income-Models" have methods to perform this action after there was made a new instance from one of them.

## HOW TO UPDATE WEEKLYWAGE TABLE?
Whenever we update DailyWage, we have to update the WeeklyWage table too.  
that is why there is a method inside DailyWage model. If after making a new DailyWge instance we call this method, it would check all changes in the same week as DailyWage new insatnce's week and updates WeeklyWage table. If we had any record in the WeeklyWage table which was in the same week as new DailyWage instance's week, there is no need to make a new row in WeeklyWage table, we just update it, but if we had a record in the same week, we make a new row in the WeeklyWage tabel.

## Saving_flow_manager()
This special function acts as a flow manager, so we can be sure that if anything goes wrong in the process of saving a new income for the courier, the database will rollback and ignore the incomplete changes. if the chnages were successful, it returns True and if not it returns False. We produce meaningful API errors by using this returned values.

# Serializers, Viewsets and...
I would continue to make this documention more complete...
