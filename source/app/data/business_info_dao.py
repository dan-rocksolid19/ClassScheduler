'''
These functions and variables are made available by LibrePy
Check out the help manual for a full list

createUnoService()      # Implementation of the Basic CreateUnoService command
getUserPath()           # Get the user path of the currently running instance
thisComponent           # Current component instance
getDefaultContext()     # Get the default context
MsgBox()                # Simple msgbox that takes the same arguments as the Basic MsgBox
mri(obj)                # Mri the object. MRI must be installed for this to work
doc_object              # A generic object with a dict_values and list_values that are persistent

To import files inside this project, use the 'librepy' keyword
For example, to import a file named config, use the following:
from librepy import config
'''

from librepy.peewee.peewee import IntegrityError
from librepy.peewee.db_model.model import BusinessInfo
from librepy.app.data.base_dao import BaseDAO

class BusinessInfoDAO(BaseDAO):
    """
    Data Access Object for BusinessInfo entity (singleton).
    
    This DAO automatically uses whatever database the BusinessInfo model is bound to,
    ensuring consistency and preventing connection leaks.
    
    Inherits efficient connection management from BaseDAO:
    - Single operations automatically manage connections
    - Multiple operations can share a connection using context:
      
      with business_dao.database.connection_context():
          info = business_dao.get_business_info()
          business_dao.update_business_info(...)
    """
    
    def __init__(self, logger):
        """
        Initialize the BusinessInfoDAO.
        
        Args:
            logger: Logger instance for this DAO
            
        Note:
            The database connection is automatically obtained from the BusinessInfo model's
            metadata, ensuring this DAO always uses the same database as the model.
        """
        super().__init__(BusinessInfo, logger)
    
    def get_business_info(self):
        """
        Get the business information record.
        Since this is a singleton, there should only be one record.
        
        Returns:
            BusinessInfo: The business info object, or None if not found
        """
        return self.get_by_id(1, "fetching business info record")
    
    def create_business_info(self, business_name, street_address, city, state, zip_code, phone):
        """
        Create the business information record if it doesn't exist.
        Since this is a singleton, this should only be called if no record exists.
        
        Args:
            business_name: Name of the business
            street_address: Street address
            city: City
            state: State
            zip_code: ZIP code
            phone: Phone number
            
        Returns:
            BusinessInfo: The created business info object, or None if creation failed
        """
        try:
            business_name_val = self.validate_string_field(business_name, "business_name", required=False)
            street_address_val = self.validate_string_field(street_address, "street_address", required=False)
            city_val = self.validate_string_field(city, "city", required=False)
            state_val = self.validate_string_field(state, "state", required=False)
            zip_code_val = self.validate_string_field(zip_code, "zip_code", required=False)
            phone_val = self.validate_string_field(phone, "phone", required=False)
            
            return self.safe_execute(
                "creating business info record",
                lambda: BusinessInfo.create(
                    business_name=business_name_val,
                    street_address=street_address_val,
                    city=city_val,
                    state=state_val,
                    zip_code=zip_code_val,
                    phone=phone_val
                ),
                reraise_integrity=False
            )
        except IntegrityError:
            self.logger.error("Business info record already exists")
            return None
        except Exception as e:
            self.logger.error(f"Error creating business info: {str(e)}")
            return None
    
    def update_business_info(self, business_name, street_address, city, state, zip_code, phone):
        """
        Update the business information record.
        
        Args:
            business_name: Name of the business
            street_address: Street address
            city: City
            state: State
            zip_code: ZIP code
            phone: Phone number
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            business_info = self.get_by_id(1, "fetching business info record for update")
            
            if not business_info:
                self.logger.error("Business info record not found for update")
                return False
            
            business_name_val = self.validate_string_field(business_name, "business_name", required=False)
            street_address_val = self.validate_string_field(street_address, "street_address", required=False)
            city_val = self.validate_string_field(city, "city", required=False)
            state_val = self.validate_string_field(state, "state", required=False)
            zip_code_val = self.validate_string_field(zip_code, "zip_code", required=False)
            phone_val = self.validate_string_field(phone, "phone", required=False)
            
            def update_func():
                business_info.business_name = business_name_val
                business_info.street_address = street_address_val
                business_info.city = city_val
                business_info.state = state_val
                business_info.zip_code = zip_code_val
                business_info.phone = phone_val
                business_info.save()
                return True
            
            result = self.safe_execute(
                "updating business info record",
                update_func,
                default_return=False
            )
            
            if result:
                self.logger.info("Updated business information successfully")
            
            return result
        except Exception as e:
            self.logger.error(f"Error updating business info: {str(e)}")
            return False
    
    def ensure_business_info_exists(self):
        """
        Ensure that a business info record exists.
        If no record exists, creates one with empty values.
        
        Returns:
            BusinessInfo: The business info object, or None if creation failed
        """
        business_info = self.get_by_id(1, "checking if business info record exists")
        if not business_info:
            business_info = self.safe_execute(
                "creating default business info record",
                lambda: BusinessInfo.create(
                    business_name="My Business",
                    street_address="",
                    city="",
                    state="",
                    zip_code="",
                    phone=""
                ),
                reraise_integrity=False
            )
        return business_info 