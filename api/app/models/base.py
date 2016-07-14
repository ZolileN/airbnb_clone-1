'''Sets MySQL variable database with all configuration settings from the right
config file depending on the environment. For more information regarding the
peewee Model see: http://docs.peewee-orm.com/en/latest/peewee/models.html.
'''
from peewee import *
import os
import json
import datetime
from config import *


'''Create the MySQLDatabase database based on appropriate environmnent
variable.
'''
db = MySQLDatabase(DATABASE['database'],
                   host=DATABASE['host'],
                   port=DATABASE['port'],
                   user=DATABASE['user'],
                   charset=DATABASE['charset'],
                   passwd=DATABASE['password'])


class BaseModel(Model):
    '''A BaseModel class for other tables to inherit from.'''
    id = PrimaryKeyField(primary_key=True, unique=True)
    database = db
    created_at = DateTimeField(default=datetime.datetime
                                               .now()
                                               .strftime("%Y/%m/%d %H:%M:%S"))
    updated_at = DateTimeField(default=datetime.datetime
                                               .now()
                                               .strftime("%Y/%m/%d %H:%M:%S"))

    def save(self, *args, **kwargs):
        '''Overloading operator save that updates the current datetime before
        calling the parent save method. Model.save(self) is imperative to have.
        Without it, a new instance will not be added to the table.

        Keyword arguments:
        args -- A non-keyworded argument list.
        kwards -- A dict of keyword arguments passed to the function.
        '''
        self.updated_at = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        Model.save(self)

    class Meta:
        '''Meta configuration is passed on to subclasses. Define the database
        from which this class is created. Specify a default ordering by id.
        '''
        database = db
        order_by = ('id', )
