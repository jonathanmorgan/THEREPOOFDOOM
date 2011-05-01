'''
Created on Apr 26, 2011

@author: jonathanmorgan
'''
__author__="jonathanmorgan"
__date__ ="$Apr 26, 2011 12:31:35 AM$"

if __name__ == "__main__":
    print "You can not execute QueryFilterHelper on its own.  Use it as part of another python program."

#===============================================================================
# imports (in alphabetical order by package, then by name)
#===============================================================================

# Python base modules
#import logging

# imports from same package
import AttributeContainer

# other network_builder imports.
from network_builder.models import Node_Type_Attribute_Value

class NodeAttributeContainer( AttributeContainer ):

    '''
    Class that extends AttributeContainer, to hold attributes of a specific
       node.  If you set a type value, will limit to just the attributes for
       the specified type.
       
    Contains the following:
    - dictionary to hold map of string attribute labels to their corresponding
       network_builder Node_Type_Attribute model instances (in parent -
       attribute_definitions).
    - property to hold node we are currently interacting with (node,
       uses parent property attribute_store).
    - method to retrieve attributes for type.
    - method to retrieve node for a given external ID.
    - method to populate attribute value dictionary from nested node's
       attributes.
    - method to place nested attribute values in database (with flag to tell
       whether to overwrite all or just update those that are not present in
       database).
    
    To use:
    - Make sure to populate the ATTR_TO_PROPERTY_MAP and ATTR_TO_METHOD_MAP with
       the mappings of attributes to properties and methods in the instance
       that will be nested.  If type is specified, you can call method
       populate_attribute_definitions to pull in all attributes defined in
       network_builder for that type, but you'll still have to tell this class
       how to derive them from the source you place inside (so you still have to
       populate the maps named above).
    '''
    
    #===========================================================================
    # constants-ish
    #===========================================================================

    
    #===========================================================================
    # __init__() method.
    #===========================================================================
    

    def __init__( self ):
        
        '''
        Constructor
        '''
        
        # always call parent init.
        super( NodeAttributeContainer, self ).__init__()
             

    #-- END constructor --#


    #===========================================================================
    # properties, in alphabetical order
    #===========================================================================


    #---------------------------------------------------------------------------
    # node
    #---------------------------------------------------------------------------


    def get_node( self ):
    
        '''
        Returns attribute source instance stored in internal instance
           variable.
        ''' 
        
        # return reference
        value_OUT = None
        
        value_OUT = self.attribute_store
        
        return value_OUT
    
    #-- END get_atttribute_source() --#


    def set_node( self, value_IN ):
    
        '''
        Accepts and stores attribute source instance in internal instance
           variable.
        ''' 
        
        # define variables
        my_node_type = None
        my_node_type_label = ""
        
        # set value
        self.attribute_source = value_IN
        
        # set type from node.  Got a type?
        my_node_type = value_IN.node_type
        if ( my_node_type ):
            
            # we have a node type.  Try to get label.
            my_node_type_label = my_node_type.label
            
            # got a label?
            if ( my_node_type_label ):
                
                # got a label.  Store it in type.
                self.type = my_node_type_label
                
            #-- END check to see if node type label. --#
            
        #-- END check to see if node type. --#
    
    #-- END set_attribute_source() --#


    node = property( get_node, set_node )


    #============================================================================
    # methods
    #============================================================================
    
    def __unicode__( self ):
        
        # return reference
        string_OUT = ""
        
        string_OUT = self.type
        
        if ( self.attribute_source ):
            
            # we have a nested attribute source - call its __unicode__ method.
            string_OUT += " - " + str( self.attribute_source )
            
        #-- END check to see if nested attribute source --#
        
        return string_OUT
        
    #-- END __unicode__() method --#


    def populate_attribute_container( self, params_IN ):
        
        '''
        Accepts parameters dict.  Verifies that there is a nested node.  If so,
           calls first populate_attribute_definitions(), then
           populate_attribute_values() to initialize this instance.
        
        Preconditions: node property must contain a Node model instance.
        
        Postconditions: when done, attribute_values and attribute_definitions
           will have been initialized from the nested node.
           
        Parameters
        - params_IN - parameter dictionary.
        
        Returns
        - String status message.  "Success!" if things are OK, description of problem if things are not OK.
        
        '''

        # return reference
        status_OUT = "Success!"
        
        # declare variables
        my_node = None
        
        # get node
        my_node = self.node
        
        # got node?
        if ( my_node ):
            
            # got a node.  populate definitions
            self.populate_attribute_definitions( params_IN )
            
            # and populate attribute values
            self.populate_attribute_values( params_IN )
        
        else:
            
            # error - need a node to populate stuff.
            status_OUT = "ERROR - can't populate attribute container without a source node."
        
        #-- END check to see if we have a node. --#
        
        return status_OUT
        
    #-- END method populate_attribute_container() --#


    def populate_attribute_definitions( self, params_IN ):
        
        '''
        Accepts params_IN parameter dictionary.  Uses nested node to retrieve
           all associated Node Type Attributes for the node's type.  Once it
           gets attributes, passes them to parent store_attribute_definitions()
           method for actual storage.
        '''

        # return reference
        status_OUT = "Success!"
        
        # declare variables
        my_node = None
        my_node_type = None
        type_attributes = None
        
        # get node
        my_node = self.node
        
        # got node?
        if ( my_node ):
            
            # got a node.  Pull in attribute values for the node's type.
            my_node_type = my_node.node_type
            
            # got type?
            if ( my_node_type ):
                
                # get attributes - Node_Type_Attribute instances.
                type_attributes = my_node_type.node_type_attribute_set
                
                # call method on parent object to store.
                self.store_attribute_definitions( type_attributes )
                
            else:
                
                # no type. Error.
                status_OUT = "ERROR - node doesn't have a type.  Can't get attribute definitions without a type."
            
            #-- END check to see if node type. --#
            
        else:
            
            # error - need a node to populate stuff.
            status_OUT = "ERROR - can't populate attributes without a source node."
        
        #-- END check to see if we have a node. --#
        
    #-- END method populate_attribute_definitions() --#


    def populate_attribute_values( self, params_IN ):

        # return reference
        status_OUT = "Success!"
        
        # declare variables
        my_node = None
        my_node_attribute_values = None
        current_attribute_value = None
        current_attribute = None
        current_attribute_label = None
        current_value = None
        
        # get node
        my_node = self.node
        
        # got node?
        if ( my_node ):
            
            # got a node.  Pull in attribute values for the node's type.
            my_node_attribute_values = my_node.node_type_attribute_value_set.all()
            
            # loop over values, adding each to the attribute_values dictionary.
            for current_attribute_value in my_node_attribute_values:
                
                # get attribute label.
                current_attribute = current_attribute_value.node_type_attribute
                current_attribute_label = current_attribute.label
                
                # get current value.
                current_value = current_attribute_value.value
                
                # store.
                set_attribute_value( current_attribute_label, current_value )
                
            #-- END loop over attribute values for current node. --#
            
            # set the loaded flag to true.
            self.attrs_loaded = True
           
        else:
            
            # error - need a node to populate stuff.
            status_OUT = "ERROR - can't populate attributes without a source node."
        
        #-- END check to see if we have a node. --#
        
    #-- END method populate_attribute_values() --#
    
    
    def save_attribute_values( self, params_IN ):
        
        '''
        Accepts params dictionary.  Accepts flag that says whether to overwrite
           or not.  Grabs list of attribute definitions.  Loops, and for each,
           gets value from attribute_values and loads the value for the current
           attribute from the database.  If not found in database, makes new
           model instance and adds it to node.  If value found, checks overwrite
           flag.  If overwrite, updates value and saves.  If not, moves on.
           
        For future - this will break down when we add multiple instances of same
           attribute for different time frames.  Need to figure out how to deal
           with that.
           
        Preconditions: there must be a nested node, and there must be attribute
           values.
           
        Postconditions: updates the database with new attribute values.
        
        Parameters:
        - params_IN - parameter dictionary that can include:
            - AttributeContainer.PARAM_OVERWRITE_FLAG ("overwrite_flag") - if True, will refresh all values. If false, will just store attributes not already in the database. 
        '''
        
        # return reference
        status_OUT = "Success!"
        
        # declare variables
        my_node = None
        do_overwrite = False
        my_definitions = None
        my_values = None
        current_attribute = ""
        current_definition = None
        current_attribute_type_id = -1
        current_attribute_QS = None
        current_attribute_model = None
        current_attribute_value = ""
        error_message = ""
        
        # get node
        my_node = self.node
        
        # got node?
        if ( my_node ):
        
            # see if we have an overwrite flag value
            if ( AttributeContainer.PARAM_OVERWRITE_FLAG in params_IN ):
                
                # got a value - use it.
                do_overwrite = params_IN[ AttributeContainer.PARAM_OVERWRITE_FLAG ]
                
            else:
                
                # no value.  Leave set to False.
                do_overwrite = False
                
            #-- END check to see if we are overwriting. --#
            
            # now, get list of definitions, values.
            my_definitions = self.attribute_definitions
            my_values = self.attribute_values
            
            # loop over definitions
            for current_attribute, current_definition in my_definitions:
                
                # get ID of current attribute's type.
                current_attribute_type_id = current_definition.id
                
                # get attribute value model instance from node.
                current_attribute_QS = my_node.node_type_attribute_value_set.filter( node_type_attribute_id = current_attribute_type_id )
                
                if ( current_attribute_QS.count() > 0 ):
                    
                    # just for kicks, see if greater than 1.
                    if ( current_attribute_QS.count() > 1 ):
                        
                        # more than one.  Not sure what to do...  Will have to
                        #   figure this out eventually.
                        error_message = "More than one value in database for " + current_attribute + ".  Not sure what to do."
                        if ( status_OUT == "Success!" ):
                            
                            # if status was success, replace with error.
                            status_OUT = error_message
                        
                        else:
                            
                            # status already an error.  Append semi-colon and space, then another error.
                            status_OUT += "; " + error_message
                        
                    else:
                        
                        # just the one.  Are we overwiting?
                        if ( do_overwrite == True ):
                            
                            # we are - retrieve model, update value, and save.
                            # got value?
                            current_attribute_value = self.get_attribute_value( current_attribute, "missing" )
                            if ( current_attribute_value != "missing" ):
                                
                                # yes, we have the value.  Get the model instance.
                                current_attribute_model = current_attribute_QS.get()
                                
                                # update.
                                current_attribute_model.value = current_attribute_value
                                
                                # save
                                current_attribute_mode.save()
                                
                            #-- END check to see if not missing. --#
                            
                        #-- END check to see if overwrite. --#
                        
                    #-- END check to see just how many values there are (should only be one?) --#
                    
                else:
                    
                    # no value for this attribute yet.  Add one.
                    # got value?
                    current_attribute_value = self.get_attribute_value( current_attribute, "missing" )
                    if ( current_attribute_value != "missing" ):
                        
                        # yes, add it.
                        current_attribute_model.node_type_attribute_set.create( node_type_attribute_id = current_attribute_type_id, value = current_attribute_value )
                        
                    #-- END check to see if value present. --# 
                    
                #-- END check to see if value already exists.
                
            #-- END loop over definitions. --#
                
        #-- END check to make sure we have a node. --#
        
        return status_OUT        
        
    #-- END method save_attribute_values() --#


#-- END class AttributeContainer --#