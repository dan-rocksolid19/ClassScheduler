'''
These functions and variables are made available by LibrePy
Check out the help manual for a full list

createUnoService()      # Implementation of the Basic CreateUnoService command
getUserPath()          # Get the user path of the currently running instance
thisComponent          # Current component instance
getDefaultContext()    # Get the default context
MsgBox()               # Simple msgbox that takes the same arguments as the Basic MsgBox
mri(obj)               # Mri the object. MRI must be installed for this to work
doc_object             # A generic object with a dict_values and list_values that are persistent

To import files inside this project, use the 'librepy' keyword
For example, to import a file named config, use the following:
from librepy import config
'''

from librepy.peewee.db_model.base_model import BaseModel
from librepy.peewee.peewee import * 

class FertilizerCmdCtrSettings(BaseModel):
    setting_key = CharField(unique=True)
    setting_value = CharField(null=True)
    
    class Meta:
        table_name = 'fertilizer_cmd_ctr_settings'

class Category(BaseModel):
    name = CharField(unique=True)
    
    class Meta:
        table_name = 'categories'

class Subcategory(BaseModel):
    parent = ForeignKeyField(Category, backref='subcategories')
    name = CharField()
    
    class Meta:
        table_name = 'subcategories'
        indexes = (
            (('parent', 'name'), True),
        )

class JobName(BaseModel):
    name = CharField(unique=True)
    
    class Meta:
        table_name = 'job_names'

class Product(BaseModel):
    category = ForeignKeyField(Category, backref='products')
    subcategory = ForeignKeyField(Subcategory, backref='products', null=True)
    name = CharField()
    active_ingredient = CharField(null=True)
    standard_rate = DecimalField(null=True, max_digits=10, decimal_places=2)
    standard_rate_unit = CharField(null=True)
    epa_reg_no = CharField(null=True)
    notes = TextField(null=True)

    rate_basis = CharField(default='acre')

    class Meta:
        table_name = 'products'

class Field(BaseModel):
    field_number = CharField()
    name = CharField()
    acres = DecimalField(null=True)
    crops = CharField(null=True)
    notes = TextField(null=True)
    
    class Meta:
        table_name = 'fields'
        indexes = (
            (('field_number',), True),
        )

class BusinessInfo(BaseModel):
    id = IntegerField(primary_key=True, constraints=[SQL('DEFAULT 1')])
    business_name = CharField()
    street_address = CharField()
    city = CharField()
    state = CharField()
    zip_code = CharField()
    phone = CharField()
    
    class Meta:
        table_name = 'business_info'
        constraints = [SQL('CHECK (id = 1)')]

class MeasurementUnit(BaseModel):
    symbol = CharField(unique=True)
    name = CharField()
    base_unit = CharField()
    conversion_factor = FloatField()
    is_system = BooleanField(default=False)
    is_selected = BooleanField(default=False)
    display_order = IntegerField(default=0)
    unit_type = CharField(default='volume')
    
    class Meta:
        table_name = 'measurement_units'
        indexes = (
            (('unit_type',), False),
        )

class Job(BaseModel):
    job_name = CharField()
    job_date = DateField()
    gpa_rate = DecimalField(null=True, max_digits=10, decimal_places=2)
    tank_size = DecimalField(null=True, max_digits=10, decimal_places=2)
    
    class Meta:
        table_name = 'jobs'

class JobWeather(BaseModel):
    job = ForeignKeyField(Job, backref='weather_conditions', on_delete='CASCADE')
    temperature = DecimalField(null=True, max_digits=5, decimal_places=1)
    wind_speed = CharField(null=True)
    wind_direction = CharField(null=True)
    sky_condition = CharField(null=True)
    
    class Meta:
        table_name = 'job_weather'

class JobField(BaseModel):
    job = ForeignKeyField(Job, backref='job_fields', on_delete='CASCADE')
    field = ForeignKeyField(Field, backref='job_fields', on_delete='CASCADE')
    
    class Meta:
        table_name = 'job_fields'
        indexes = (
            (('job', 'field'), True),
        )

class JobBatch(BaseModel):
    job = ForeignKeyField(Job, backref='batches', on_delete='CASCADE')
    batch_number = IntegerField()
    gallons = DecimalField(null=True, max_digits=10, decimal_places=2)
    acres = DecimalField(null=True, max_digits=10, decimal_places=2)
    
    class Meta:
        table_name = 'job_batches'
        indexes = (
            (('job', 'batch_number'), True),
        )

class JobProduct(BaseModel):
    job = ForeignKeyField(Job, backref='job_products', on_delete='CASCADE')
    product = ForeignKeyField(Product, backref='job_products', on_delete='CASCADE')
    rate = DecimalField(null=True, max_digits=10, decimal_places=2)
    rate_unit = CharField(null=True)
    total_amount = DecimalField(null=True, max_digits=10, decimal_places=2)
    rate_basis = CharField(default='acre')
    
    class Meta:
        table_name = 'job_products'
        indexes = (
            (('job', 'product'), True),
        )

class JobBatchProduct(BaseModel):
    job_batch = ForeignKeyField(JobBatch, backref='batch_products', on_delete='CASCADE')
    job_product = ForeignKeyField(JobProduct, backref='batch_products', on_delete='CASCADE')
    amount = DecimalField(null=True, max_digits=10, decimal_places=2)
    gallons = DecimalField(null=True, max_digits=10, decimal_places=2)
    
    class Meta:
        table_name = 'job_batch_products'
        indexes = (
            (('job_batch', 'job_product'), True),
        )