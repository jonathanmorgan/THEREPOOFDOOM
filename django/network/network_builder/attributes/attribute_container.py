'''
Created on Apr 30, 2011

@author: jonathanmorgan
'''
__author__="jonathanmorgan"
__date__ ="$Apr 30, 2011 09:31:35 AM$"

if __name__ == "__main__":
    print "You can not execute AttributeContainer on its own.  Use it as part of another python program."

#===============================================================================
# imports (in alphabetical order by package, then by name)
#===============================================================================

# Python base modules
import logging

# network_builder imports

# django-utils imports
from django_utils import query_filter

class AttributeContainer( object ):

    '''
    Parent class for any type of things that has a set of attributes.  Will
       create a child class here for nodes and ties for network_builder.  Could
       also re-use this for other objects, too, if you wanted to.
       
    Contains the following:
    - variable to hold map of attributes to object properties.
    - variable to hold map of attributes to object methods.
    - constants that contain shared parameter names (for parameter dictionaries
       used throughout).
    - dictionary that holds attribute values, and methods for interacting with
       the dictionary (get value, update value).
    - object instance that is source of attribute values.
    - dictionary to hold map of attribute label to attribute definition.
    - object instance that is used to store the attributes (details left up to
       child class).
    
    To use:
    - Make sure to populate the ATTR_TO_PROPERTY_MAP and ATTR_TO_METHOD_MAP with
       the mappings of attributes to properties and methods in the instance
       that will be nested.
    '''
    
    #===========================================================================
    # constants-ish
    #===========================================================================
    
    # parameters to hold derivation types.
    DERIVE_TYPE_PROPERTY = "property"
    DERIVE_TYPE_METHOD = "method"
    
    # Parameters for limiting QuerySets.
    PARAM_DATE_COLUMN = query_filter.QueryFilterHelper.PARAM_DATE_COLUMN
    PARAM_START_DATE = query_filter.QueryFilterHelper.PARAM_START_DATE
    PARAM_END_DATE = query_filter.QueryFilterHelper.PARAM_END_DATE
    PARAM_ORDER_BY = query_filter.QueryFilterHelper.PARAM_ORDER_BY
    
    # Parameters for controlling how we derive properties
    PARAM_OVERWRITE_FLAG = "overwrite_flag"
    
    # Parameters for how we create list of attributes.
    PARAM_DERIVE_FLAG = "derive_flag"
    
    # default value constants.
    DEFAULT_OVERWRITE_FLAG = False
    DEFAULT_DERIVE_FLAG = False
    

    #===========================================================================
    # __init__() method.
    #===========================================================================
    

    def __init__( self ):
        
        '''
        Constructor
        '''
        
        # variables (for now...)
        self.store_type = None
        self.attrs_loaded = False
        
        # properties
        self.m_attr_values_dict = {}
        self.m_attr_source_instance = None
        self.m_attr_store_instance = None
        
        # place to map attribute labels to attribute definitions - definition
        #    can be whatever you want. In node and tie children, this will
        #    contain either Node_Type_Attribute or Tie_Type_Attribute instances.
        self.m_attr_defs_dict = {}

             

    #-- END constructor --#


    #===========================================================================
    # properties, in alphabetical order
    #===========================================================================


    #---------------------------------------------------------------------------
    # attribute_definitions
    #---------------------------------------------------------------------------

    def get_attribute_definitions( self ):
    
        '''
        Returns attribute definitions dictionary stored in internal instance
           variable.
        ''' 
        
        # return reference
        value_OUT = None
        
        value_OUT = self.m_attr_defs_dict
        
        if ( not value_OUT ):
            
            # set it to an empty dict, store, then do a recursive get call, then
            #    return the result.
            value_OUT = {}
            self.set_attribute_definitions( value_OUT )
            value_OUT = self.m_attr_defs_dict
            
        #-- END check to see if there is anything in m_attr_defs_dict.
        
        return value_OUT
    
    #-- END get_attribute_definitions() --#


    def set_attribute_definitions( self, value_IN ):
    
        '''
        Accepts and stores attribute definitions dictionary in internal instance
           variable.
        ''' 
        
        # set value
        self.m_attr_defs_dict = value_IN
    
    #-- END set_attribute_definitions() --#


    attribute_definitions = property( get_attribute_definitions, set_attribute_definitions )


    #---------------------------------------------------------------------------
    # attribute_source
    #---------------------------------------------------------------------------


    def get_attribute_source( self ):
    
        '''
        Returns attribute source instance stored in internal instance
           variable.
        ''' 
        
        # return reference
        value_OUT = None
        
        value_OUT = self.m_attr_source_instance
        
        return value_OUT
    
    #-- END get_attribute_source() --#


    def set_attribute_source( self, value_IN ):
    
        '''
        Accepts and stores attribute source instance in internal instance
           variable.
        ''' 
        
        # set value
        self.m_attr_source_instance = value_IN
    
    #-- END set_attribute_source() --#


    attribute_source = property( get_attribute_source, set_attribute_source )


    #---------------------------------------------------------------------------
    # attribute_store
    #---------------------------------------------------------------------------


    def get_attribute_store( self ):
    
        '''
        Returns attribute source instance stored in internal instance
           variable.
        ''' 
        
        # return reference
        value_OUT = None
        
        value_OUT = self.m_attr_store_instance
        
        return value_OUT
    
    #-- END get_attribute_store() --#


    def set_attribute_store( self, value_IN ):
    
        '''
        Accepts and stores attribute source instance in internal instance
           variable.
        ''' 
        
        # set value
        self.m_attr_store_instance = value_IN
    
    #-- END set_attribute_store() --#


    attribute_store = property( get_attribute_store, set_attribute_store )


    #---------------------------------------------------------------------------
    # attribute_values
    #---------------------------------------------------------------------------

    def get_attribute_values( self ):
    
        '''
        Returns attribute values dictionary stored in internal instance
           variable.
        ''' 
        
        # return reference
        value_OUT = None
        
        value_OUT = self.m_attr_values_dict
        
        return value_OUT
    
    #-- END get_attribute_values() --#


    def set_attribute_values( self, value_IN ):
    
        '''
        Accepts and stores attribute values dictionary in internal instance
           variable.
        ''' 
        
        # set value
        self.m_attr_values_dict = value_IN
    
    #-- END set_attribute_values() --#


    attribute_values = property( get_attribute_values, set_attribute_values )


    #============================================================================
    # methods
    #============================================================================
    
    def __unicode__( self ):
        
        # return reference
        string_OUT = ""
        
        # got a type?
        if ( self.store_type ):
        
            # yes - add label.
            string_OUT = str( self.store_type )
            
        #-- END check to see if type. --#
        
        if ( self.attribute_source ):
            
            # we have a nested attribute source - call its __unicode__ method.
            string_OUT += " - " + str( self.attribute_source )
            
        #-- END check to see if nested attribute source --#
        
        return string_OUT
        
    #-- END __unicode__() method --#
    

    def create_attribute_name_list( self, prefix_IN ):
        
        '''
        For exporting a given container's information, returns the list of
           attribute names for attributes contained in ATTR_TO_PROPERTY_MAP and
           ATTR_TO_METHODS_MAP.  The combination of these two should be all the
           attributes defined for the object currently nested.  Not just pulling
           names from attribute_values, in case we are iterating and different
           source instances have different sets of attributes set.
           
        Preconditions: none.
        
        Postconditions: list is sorted alphabetically by name.
        
        Parameters:
        - prefix_IN - string prefix to append to the front of each header. 
        '''
        
        # return reference
        header_list_OUT = []
        
        # declare variables.
        my_prefix = ""
        my_definitions = None
        current_property_name = ""
        current_attribute_name = ""
        
        # got a prefix?
        if ( prefix_IN ):
            
            my_prefix = prefix_IN
            
        else:
            
            my_prefix = ""
            
        #-- END setting prefix value.
        
        # first add attributes mapped to properties.
        my_definitions = self.attribute_definitions
        
        # got any definitions?
        if ( my_definitions ):
    
            # yes. Loop over them.    
            for current_attribute_name in sorted( my_definitions ):
            
                # append value to list.
                header_list_OUT.append( my_prefix + current_attribute_name )
                
            #-- END loop over list of properties --#
            
        else:
        
            # no error.  Log message.
            logging.error( "*** In create_attribute_name_list(), no definitions loaded.  Load the definitions first. ***" )
            
        #-- END check to see if definitions. --#
        
        # sort list- always sort alphabetically by name.
        header_list_OUT = sorted( header_list_OUT )

        return header_list_OUT
        
    #-- END method create_attribute_name_list() --#


    def create_attribute_value_list( self, params_IN ):
        
        '''
        For exporting a given user's information, makes a list of the values for
           the current user's properties contained in the EXPORT_PROPERTY_LIST
           list and derived attributes contained in the EXPORT_ATTRIBUTE_LIST
           list.
           
        Preconditions: need to have loaded this model instance from database.
        
        Postconditions: also stores the attribute values in an internal variable, so they are 
        '''
        
        # return reference
        list_OUT = []
        
        # declare variables.
        do_derive = AttributeContainer.DEFAULT_DERIVE_FLAG
        attribute_name_list = None
        current_property_name = ""
        current_attribute_name = ""
        current_value = ""
        
        # got params?
        if ( params_IN ):

            # do we derive?
            if ( AttributeContainer.PARAM_DERIVE_FLAG in params_IN ):
                
                # parameter is present.  Set variable from it.
                do_derive = params_IN[ AttributeContainer.PARAM_DERIVE_FLAG ]
                
            #-- END check to see if derive flag parameter is present. --#
            
        else:
        
            # leave as default.
            do_derive = AttributeContainer.DEFAULT_DERIVE_FLAG
            
        #-- END check to see if params passed in.
        
        # so, again, do we derive?
        if ( do_derive == True ):
            
            # derive any un-populated attribute values.
            self.derive_attribute_values( params_IN )
            
        #-- END check to see if we derive attributes --#
        
        # get list of attribute names, in alphabetical order.
        attribute_name_list = self.create_attribute_name_list( "" )
        
        # next, loop over attribute names, adding each to output.
        for current_attribute_name in attribute_name_list:
            
            # do a getattr
            current_value = self.get_attribute_value( current_attribute_name, "" )
            
            # append value to list.
            list_OUT.append( current_value )
            
        #-- END loop over list of attribute names --#
        
        return list_OUT
        
    #-- END method create_attribute_value_list() --#


    def derive_attribute_value( self, attr_name_IN, params_IN ):
        
        '''
        Accepts attribute name and parameters that need to be passed to routine
           that generates the attribute value (if it is a method, not a
           property).  Figures out if attribute is derived from a property or
           a method, does the appropriate thing for the type of property to make
           a value, then returns the resulting value.
           
        Preconditions: need to have a nested source instance, and need to have
           populated the maps of attributes to property and method names inside
           that source.
        
        Postconditions: none. 
        
        Parameters:
        - attr_name_IN - name of attribute whose value we want.
        - params_IN - parameters you want to pass to the method that generates the attribute value (if the attribute is made by a method - if not, this is ignored).
        '''
        
        # return reference
        value_OUT = None 
        
        # declare variables.
        my_attribute_source = None
        my_definitions = None
        attribute_type = None
        derivation_type_label = ""
        current_derived_from = ""
        method_object = None
        current_value = ""
        
        # get source instance
        my_attribute_source = self.attribute_source
        
        # get attribute definitions
        my_definitions = self.attribute_definitions
        
        # got a source?
        if ( my_attribute_source ):
            
            # got an attribute name?
            if ( attr_name_IN ):
                
                # see if it is mapped to a definition.
                if ( attr_name_IN in my_definitions ):
                    
                    # yup - grab the definition and get the label.
                    attribute_type = my_definitions[ attr_name_IN ]
                    
                    # get label
                    derivation_type_label = attribute_type.get_derivation_type_label()

                    # got a label?  If not, no way to derive.  Punt and move on.
                    if ( derivation_type_label ):
                        
                        # See if type is property.
                        if ( derivation_type_label == AttributeContainer.DERIVE_TYPE_PROPERTY ):
                            
                            # it is.  Get property.
                            current_derived_from = attribute_type.derived_from
                            
                            # got a derived_from?
                            if ( current_derived_from ):
                                
                                # yes.  retrieve property.
                                value_OUT = getattr( my_attribute_source, current_derived_from, None )
                                
                            #-- END check to see if got a property name. --#
                            
                        elif( derivation_type_label == AttributeContainer.DERIVE_TYPE_METHOD ):
                    
                            # it is a method.  Retrieve method from source.
                            current_derived_from = attribute_type.derived_from
                            
                            # got a derived_from?
                            if ( current_derived_from ):
                                
                                # yes.  Use it as method name.
                                method_object = getattr( my_attribute_source, current_derived_from, None )
                                
                                # anything returned?
                                if ( method_object ):
                                    
                                    # invoke the method
                                    value_OUT = method_object( params_IN )
                                    
                                #-- END method invocaton. --#
                            
                            #-- END check to see if derived_from --# 

                        #-- END check to see what type of attribute we are getting. --#
                    
                    #-- END check to see if we have a label. --#
                
                #-- END check to see if we have a definition. --#
                
            #-- END check to make sure we have an attribute name --#
            
        #-- END check for having an attribute source. --#
        
        return value_OUT
        
    #-- END method derive_attribute_value() --#


    def derive_attribute_values( self, params_IN ):
        
        '''
        Loops over attributes contained in the EXPORT_ATTRIBUTE_LIST list and
           for each, calls the method associated with that attribute in the
           ATTR_TO_METHOD_MAP dictionary.  Stores results in nested
           attribute_values dictionary.  One parameter is a flag telling
           whether we want to overwrite attributes that have already been
           derived.
           
        Preconditions: need to have loaded this model instance from database.
        
        Postconditions: stores the attribute values in an internal variable, so they are 
        '''
        
        # return reference
        status_OUT = "Success!" 

        # declare variables.
        my_attribute_source = None
        do_overwrite = AttributeContainer.DEFAULT_OVERWRITE_FLAG
        attribute_name_list = None
        my_values = None
        current_attr_name = ""
        do_update = False
        current_value = ""
        
        # get source instance
        my_attribute_source = self.attribute_source
        
        # got a source?
        if ( my_attribute_source ):
        
            # got params?
            if ( params_IN ):
            
                # yes.  are we overwriting, or just adding values not already present?
                if ( AttributeContainer.PARAM_OVERWRITE_FLAG in params_IN ):
                    
                    # got a value - use it.
                    do_overwrite = params_IN[ AttributeContainer.PARAM_OVERWRITE_FLAG ]
                    
                else:
                    
                    # no value.  Leave set to False.
                    do_overwrite = AttributeContainer.DEFAULT_OVERWRITE_FLAG
                    
                #-- END check to see if we are overwriting. --#
                
            else:
            
                # no params.  Use default of False.
                do_overwrite = AttributeContainer.DEFAULT_OVERWRITE_FLAG
                
            #-- END check to see if params or not. --#
            
            # grab attribute names and values
            attribute_name_list = self.create_attribute_name_list( "" )
            my_values = self.attribute_values
            
            # iterate over names.  For each, see if value is in our values map.
            #  
            for current_attr_name in attribute_name_list:
                
                # initialize loop variables
                do_update = False
                
                # are we updating?
                if ( do_overwrite == False ):
                
                    # no overwriting.  See if attribute present in values.
                    if ( current_attr_name in my_values ):
                        
                        # yup, it is there - do not update.
                        do_update = False
                        
                    else:
                        
                        # not there.  Do update.
                        do_update = True
                        
                    #-- END check to see if we update.
                    
                else:
                    
                    # we are overwriting - always do update.
                    do_update = True
                    
                #-- END check to see if we are overwriting) --#
                
                #logging.debug( "*** In derive_attribute_values(), attribute: " + current_attr_name + "; do_update = " + str( do_update ) + " ***" )
                
                # update?
                if ( do_update == True ):
                    
                    # we are updating. derive value and store it.
                    current_value = self.derive_attribute_value( current_attr_name, params_IN )
                    self.set_attribute_value( current_attr_name, current_value, True )
                    
                #-- END check to see if update or not. --#
                
            #-- END loop over attribute names. --#
        
        else:
            
            # output an error message.
            status_OUT = "Could not derive values because no source object present."
        
        #-- END check for having an attribute source. --#
        
        return status_OUT
        
    #-- END method derive_attribute_values() --#


    def get_attribute_value( self, attr_name_IN, default_IN ):
        
        '''
        Retrieves value from attribute_values dictionary for attr_name_IN.
           If name not present as key in dictionary, returns value in default_IN
           or None if no value set.
           
        Preconditions: none.
        
        Postconditions: none.
           
        Parameters:
        - attr_name_IN - name of attribute we are updating.
        - default_IN - default value we want to return if attribute not present.
        
        Returns:
        - value in attribute_values for name passed in, or default passed in/None if name not in dictionary. 
        '''
        
        # return reference
        value_OUT = None
        
        # declare variables
        my_values = None
        
        # is attribute already in the dictionary?
        my_values = self.attribute_values
        if ( attr_name_IN in my_values ):
            
            # yes.  return it.
            value_OUT = my_values[ attr_name_IN ]
                
        else:
            
            # no - got a default value?
            if( default_IN ):
                
                # yes. Return it.
                value_OUT = default_IN
                
            else:
                
                # no.  Return None.
                value_OUT = None
 
            #-- END check to see if default or not. --#

        #-- END check to see if attribute already in nested dictionary.
                 
        return value_OUT
        
    #-- END method get_attribute_value() --#


    def reset_container( self ):
        
        '''
        Resets all internal variables to empty.
        '''
        
        #self.attribute_definitions = {}
        self.attribute_source = None
        self.attribute_store = None
        self.attribute_values = {}
        self.attrs_loaded = False
        self.store_type = None
        
    #-- END method reset_container() --#


    def set_attribute_value( self, attr_name_IN, attr_value_IN, overwrite_existing_IN = True ):
        
        '''
        Stores value in attr_value_IN in dictionary entry for attr_name_IN in
           the nested attribute_values dictionary.  If overwrite_existing_IN
           is true, will overwrite existing with new value.  If false, will
           not overwrite.  Returns the value in the dictionary (either value
           passed in, or the old value if overwrite false and there was already
           a value.
           
        Preconditions: need to have loaded this model instance from database.
        
        Postconditions: Updates the attribute_values dictionary. Returns the
           value in the dictionary (either value passed in, or the old value
           if overwrite false and there was already a value).
           
        Parameters:
        - attr_name_IN - name of attribute we are updating.
        - attr_value_IN - value we want to set for the attribute.
        - overwrite_existing_IN - boolean, if true, overwrite with new value regardless, if false, do not overwrite if there is already a value.
        
        Returns:
        - value in attribute_values at end of method call, or None if error. 
        '''
        
        # return reference
        value_OUT = None 
        
        # declare variables.
        my_values = None
        do_overwrite = False
        
        # check on overwrite.
        if ( ( overwrite_existing_IN ) and ( overwrite_existing_IN == True ) ):
            
            # we do overwrite
            do_overwrite = True
            
        #-- END check to see if we overwrite.
        
        # get values
        my_values = self.attribute_values
        
        # got a name?
        if ( attr_name_IN ):
            
            # is attribute already in the dictionary?
            if ( attr_name_IN in self.attribute_values ):
                
                # yes.  Do we overwrite?
                if ( do_overwrite == True ):
                    
                    # write it!
                    self.attribute_values[ attr_name_IN ] = attr_value_IN
                    value_OUT = attr_value_IN
                    
                else:
                    
                    # don't overwrite!  return what is in the dictionary.
                    value_OUT = self.attribute_values[ attr_name_IN ]
            
                #-- END check to see if overwrite or not.
                
            else:
                
                # no - just add it.
                self.attribute_values[ attr_name_IN ] = attr_value_IN
                value_OUT = attr_value_IN
                
            #-- END check to see if attribute already in nested dictionary.
                 
        #-- END check to see if attribute name passed in. --#
        
        return value_OUT
        
    #-- END method set_attribute_value() --#


    def store_attribute_definitions( self, attribute_type_QS_IN ):

        '''
        Accepts attribute type list.
        '''

        # return reference
        status_OUT = "Success!"
        
        # declare variables
        my_definitions = None
        current_attribute = None
        current_attribute_label = None
        
        # got QuerySet?
        if ( attribute_type_QS_IN ):
            
            # got a QuerySet.  Get the map of attribute labels to definitions.
            my_definitions = self.attribute_definitions
            
            # Loop over QuerySet.
            for current_attribute in attribute_type_QS_IN:
                
                # get label
                current_attribute_label = current_attribute.label
                
                # store attribute type in dictionary, mapped to label.
                my_definitions[ current_attribute_label ] = current_attribute
            
            #-- END loop over attribute types passed in.
                       
        else:
            
            # error - need a node to populate stuff.
            status_OUT = "ERROR - no QuerySet passed in, can't store attribute definitions if none passed in."
        
        #-- END check to see if we have a node. --#
        
        return status_OUT
        
    #-- END method store_attribute_definitions() --#


#-- END class AttributeContainer --#