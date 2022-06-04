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
but each Trip, only belongs to a specific courier (Many-To-One relationship)

# Wage Reduction Model
This is the second Income-Model that we have, it has 3 fileds (courier, date, reduction_amount) and courier is its foreign key, because a courier can have lot of
WageReductions but each WageReduction, only belongs to a specific courier (Many-To-One relationship)

# Wage Increment Model
This is the third Income-Model that we have, it has 3 fileds (courier, date, increment_amount) and courier is its foreign key, because a courier can have lot of
WageIncrements but each WageIncrement, only belongs to a specific courier (Many-To-One relationship)

# Daily Wage Model
It Has 3 fields (courier, date, wage). This Model is slightly different from three above models, because the only table which would be effected by 
changes in this model is the WeeklyWage Model (Which I'll explain it in next few lines). the other important difference about this model comparing to other models, is that it has a special constraint.
This constarint lies in two fileds of it, which are courier and date. in Other words we can not have two same rows in this table with same courier AND same date (This condition Would violate the logical and conceptual idea of ingerity of database) 
