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
import logging

# imports from same package
from network_builder.attributes.attribute_container import AttributeContainer

# other network_builder imports.
from network_builder.models import Node, Node_Type_Attribute_Value

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
       
    Limitations:
    - only works for one NodeType at a time.
    - doesn't yet know what to do with attributes that have same label,
        different date ranges (for now, make different attributes for each
        date range).
    
    To use:
    - 1) Make sure to place a Node_Type model instance in the source_type
        attribute so an instance with no nested Node can still pull in attribute
        definitions.
    - 2) You have to call populate_attribute_definitions() to get attribute
        definitions - there is no magic that does this automatically when you
        set a type (yet).
    '''
    
    #===========================================================================
    # constants-ish
    #===========================================================================


    # parameters for looking up nodes.
    PARAM_NODE_ORIGINAL_ID = "original_id"
    PARAM_NODE_TYPE_LABEL = "node_type_label"
    
    # parameters for loading nodes
    PARAM_NODE_INSTANCE = "node_instance"
    PARAM_SOURCE_INSTANCE = "source_instance"
    PARAM_LOAD_ATTRIBUTE_VALUES_FLAG = "load_attr_values"

    
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
    
    #-- END get_node() --#


    def set_node( self, value_IN ):
    
        '''
        Accepts and stores attribute source instance in internal instance
           variable.
        ''' 
        
        # define variables
        my_node_type = None
        my_node_type_label = ""
        
        # set value
        self.attribute_store = value_IN
        
        # set type from node.  Got a type?
        my_node_type = value_IN.node_type
        if ( my_node_type ):
            
            # got a node type.  Store it in store_type.
            self.store_type = my_node_type                
            
        #-- END check to see if node type. --#
    
    #-- END set_node() --#


    node = property( get_node, set_node )


    #============================================================================
    # methods
    #============================================================================
    
    def __unicode__( self ):
        
        # return reference
        string_OUT = ""
        
        if ( self.store_type ):
        
            # got one. Use it in string.
            string_OUT = str( self.store_type )
            
        #-- END check to see if type --#
        
        if ( self.attribute_source ):
            
            # we have a nested attribute source - call its __unicode__ method.
            string_OUT += " - " + str( self.attribute_source )
            
        #-- END check to see if nested attribute source --#
        
        return string_OUT
        
    #-- END __unicode__() method --#


    def load_attribute_values( self, params_IN ):

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
            
            #logging.debug( "*** values in database: " + str( my_node_attribute_values.count() ) + " ***" )
            
            # loop over values, adding each to the attribute_values dictionary.
            for current_attribute_value in my_node_attribute_values:
                
                # get attribute label.
                current_attribute = current_attribute_value.node_type_attribute
                current_attribute_label = current_attribute.label
                
                # get current value.
                current_value = current_attribute_value.value
                
                # store.
                self.set_attribute_value( current_attribute_label, current_value )
                
            #-- END loop over attribute values for current node. --#
            
            # set the loaded flag to true.
            self.attrs_loaded = True
           
        else:
            
            # error - need a node to populate stuff.
            status_OUT = "ERROR - can't load attribute values without a source node."
        
        #-- END check to see if we have a node. --#
        
    #-- END method load_attribute_values() --#
    
    
    def load_node( self, params_IN ):
    
        '''
        Accepts set of parameters that should include an original ID and a node
           type.  Uses those to search for and load a Node into this instance.
           If can't find a matching node, returns an error message describing the
           problem.
           
        Preconditions: None.
        
        Postconditions: If success, resets instance, then stores node inside this
           instance.
           
        Parameters:
        - params_IN - parameter dictionary, expected to contain:
            - PARAM_NODE_INSTANCE ("node_instance") - node instance to use to load this object.
            - PARAM_SOURCE_INSTANCE ("source_instance" ) - instance to be used to derive values. If flag is set to derive, you must pass the source in to this method, else the reset will clear out existing source and any attempt to derive will fail since source will have been emptied.
            - PARAM_NODE_ORIGINAL_ID ("original_id") - original ID of entity whose node we are looking up.
            - PARAM_NODE_TYPE_LABEL ("node_type_label") - type of node we are trying to find.

        Returns:
        - String - status message (status_OUT).  "Success!" if success, else error message on error.
        '''
        
        # return reference
        status_OUT = "Success!"
        
        # declare variables
        node_IN = None
        source_IN = None
        my_node_QS = None
        my_node = None
        got_node = False
        result = None

        # got params?
        if ( params_IN ):
        
            # yes.  Look for node and source instances.
            # node
            if ( NodeAttributeContainer.PARAM_NODE_INSTANCE in params_IN ):
            
                # got one.  pull it out.
                node_IN = params_IN[ NodeAttributeContainer.PARAM_NODE_INSTANCE ]
                
            #-- END check for node --#
            
            # source
            if ( NodeAttributeContainer.PARAM_SOURCE_INSTANCE in params_IN ):
            
                # got one.  pull it out.
                source_IN = params_IN[ NodeAttributeContainer.PARAM_SOURCE_INSTANCE ]
            
            #-- END check for source --#
            
        
        #-- END check to see if params coming in. --#
        
        # first, see if there is a node already provided.
        if ( node_IN ):
        
            # reset container and store node.
            self.reset_container()
            self.node = node_IN
            got_node = True
        
        else:

            # try a search for node using params passed in.
            my_node_QS = self.node_search( params_IN )
            
            # got anything back?
            if ( my_node_QS.count() == 1 ):
            
                # yes.  One thing.  Store it.
                my_node = my_node_QS.get()
                self.reset_container()
                self.node = my_node
                got_node = True
                
            elif ( my_node_QS.count() > 1 ):
            
                # yes, but more than one.  Use first, return error.
                my_node = my_node_QS[ 0 ]
                self.reset_container()
                self.node = my_node
                got_node = True
                status_OUT = "ERROR - more than one node returned for parameters passed in.  Using first: " + str( my_node )
                
            else:
            
                # nothing returned.
                status_OUT = "No node found for parameters."
                got_node = False
    
            #-- END check to see if we found any matching nodes. --#            

        #-- END check to see if node already there for us.
        
        # got a node?
        if ( got_node == True ):
        
            # yes.  got source?
            if ( source_IN ):
            
                # yes.  store it.
                self.attribute_source = source_IN
            
            #-- END check to see if source --#
            
            # load attribute values.
            result = self.populate_attribute_values( params_IN )
            #logging.debug( "*** after call to populate_attribute_values(), result: " + str( result ) + " ***" )
            
        #-- END check to see if got node. --#
        
        return status_OUT
    
    #-- END method load_node() --#
    

    def node_search( self, params_IN ):
        
        '''
        Accepts params array, so we can look up node by more things later.  For
           now, just accepts original ID and node_type_label, tries to retrieve
           a node for those values.
        
        Preconditions: none.
        
        Postconditions: when done, if success, node is stored in this instance
           as well as returned.
           
        Parameters
        - params_IN - parameter dictionary, with expected values:
            - PARAM_NODE_ORIGINAL_ID ("original_id") - original ID of entity whose node we are looking up.
            - PARAM_NODE_TYPE_LABEL ("node_type_label") - type of node we are trying to find.
        
        Returns
        - QuerySet - returns QuerySet - calling program has to figure out how to interpret, process it.
        '''

        # return reference
        node_QS_OUT = None
        
        # declare variables
        original_id_IN = -1
        node_type_label_IN = ""
        
        # got params?
        if ( params_IN ):

            # Get node QuerySet.
            node_QS_OUT = Node.objects.all()
            
            # pull in known parameters
            # original_id
            if ( NodeAttributeContainer.PARAM_NODE_ORIGINAL_ID in params_IN ):
            
                # we have a date column name.
                original_id_IN = params_IN[ NodeAttributeContainer.PARAM_NODE_ORIGINAL_ID ]
                
                # got original ID?
                if ( original_id_IN ):
                    
                    # yes - add filter.
                    node_QS_OUT = node_QS_OUT.filter( original_id = original_id_IN )
                    
                #-- END check to see if original ID passed in.
            
            #-- END check to see if date column name --#            
            
            # node type label
            if ( NodeAttributeContainer.PARAM_NODE_TYPE_LABEL in params_IN ):
            
                # we have a date column name.
                node_type_label_IN = params_IN[ NodeAttributeContainer.PARAM_NODE_TYPE_LABEL ]
                
                # got node type label?
                if ( node_type_label_IN ):
                    
                    # yes - add filter.
                    node_QS_OUT = node_QS_OUT.filter( node_type__label = node_type_label_IN )
                    
                #-- END check to make sure we have input parameters.
            
            #-- END check to see if date column name --#            
                        
        #-- END check to see if parameters passed in. --#
        
        return node_QS_OUT
        
    #-- END method node_search() --#


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
        Accepts params_IN parameter dictionary.  Uses nested type to retrieve
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
        
        # first, see if nested node_type.  If so, use it.
        if ( self.store_type ):
        
            # have a nested type instance.
            my_node_type = self.store_type
            
        else:
        
            # not stored - try retrieving from current node.
            my_node = self.node
            
            if ( my_node ):
            
                # got a node.  Pull in attribute values for the node's type.
                my_node_type = my_node.node_type
                
            #-- END check to see if node. --#
            
        #-- END check to see if nested type. --#
        
        # got node type?
        if ( my_node_type ):
        
            # get attributes - Node_Type_Attribute instances (call .all() to get
            #    QuerySet).
            type_attributes = my_node_type.node_type_attribute_set.all()
            
            # call method on parent object to store.
            self.store_attribute_definitions( type_attributes )
            
        else:
            
            # no type. Error.
            status_OUT = "ERROR - No node type nested, and nested node doesn't have a type.  Can't get attribute definitions without a type."
        
        #-- END check to see if node type. --#
            
        return status_OUT

    #-- END method populate_attribute_definitions() --#


    def populate_attribute_values( self, params_IN ):

        # return reference
        status_OUT = "Success!"
        
        # declare variables
        my_node = None
        do_derive = AttributeContainer.DEFAULT_DERIVE_FLAG
        do_overwrite = AttributeContainer.DEFAULT_OVERWRITE_FLAG
        
        my_node_attribute_values = None
        current_attribute_value = None
        current_attribute = None
        current_attribute_label = None
        current_value = None
        
        # get node
        my_node = self.node
        
        # got node?
        if ( my_node ):
        
            # got params?
            if ( params_IN ):
            
                #logging.debug( "*** in populate_attribute_values() - got parameters - " + str( params_IN ) + " ***" )
                
                # yes.  Got parameters we care about?
                # derive flag
                if ( AttributeContainer.PARAM_DERIVE_FLAG in params_IN ):
                    
                    # yes.  Get value.
                    do_derive = params_IN[ AttributeContainer.PARAM_DERIVE_FLAG ]
                    
                else:
                
                    # no. Use default.
                    do_derive = AttributeContainer.DEFAULT_DERIVE_FLAG
                
                #-- END check for derive flag. --#
                
                # overwrite flag
                if ( AttributeContainer.PARAM_OVERWRITE_FLAG in params_IN ):
                    
                    # yes.  Get value.
                    do_overwrite = params_IN[ AttributeContainer.PARAM_OVERWRITE_FLAG ]
                    
                else:
                
                    # no. Use default.
                    do_overwrite = AttributeContainer.DEFAULT_OVERWRITE_FLAG
                
                #-- END check for derive flag. --#
                
            #-- END check to see if params passed in.
                
            # regardless, load attribute values for node from database.
            self.load_attribute_values( params_IN )
            
            #logging.debug( "*** do_derive = " + str( do_derive ) + ", attribute_values = " + str( self.attribute_values ) + " ***" )
            #logging.debug( "*** in NAC, self.attribute_source = " + str( self.attribute_source ) + " ***" )
            
            # do we derive, also?
            if ( do_derive == True ):
            
                # also derive values.  Parameters will have overwrite flag if
                #    applicable, so just pass on the params dictionary.
                status_OUT = self.derive_attribute_values( params_IN )
                
            #-- END check to see if we try deriving in addition to just loading.
            
        else:
            
            # error - need a node to populate stuff.
            status_OUT = "ERROR - can't populate attributes without a source node."
        
        #-- END check to see if we have a node. --#
        
        return status_OUT
        
    #-- END method populate_attribute_values() --#
    
    
    def save_attribute_values( self, params_IN = {} ):
        
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
        do_overwrite = AttributeContainer.DEFAULT_OVERWRITE_FLAG
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
        
            # got any parameters?
            if ( params_IN ):
        
                # see if we have an overwrite flag value
                if ( AttributeContainer.PARAM_OVERWRITE_FLAG in params_IN ):
                    
                    # got a value - use it.
                    do_overwrite = params_IN[ AttributeContainer.PARAM_OVERWRITE_FLAG ]
                    
                else:
                    
                    # no value.  Leave set to False.
                    do_overwrite = AttributeContainer.DEFAULT_OVERWRITE_FLAG
                    
                #-- END check to see if we are overwriting. --#
                
            #-- END check to see if params passed in. --#
            
            # now, get list of definitions, values.
            my_definitions = self.attribute_definitions
            my_values = self.attribute_values
            
            # loop over definitions
            for current_attribute, current_definition in my_definitions.items():
                
                # get ID of current attribute's type.
                current_attribute_type_id = current_definition.id
                
                # get attribute value model instance from node.
                current_attribute_value_QS = my_node.node_type_attribute_value_set.filter( node_type_attribute__id = current_attribute_type_id )
                
                if ( current_attribute_value_QS.count() > 0 ):
                    
                    # just for kicks, see if greater than 1.
                    if ( current_attribute_value_QS.count() > 1 ):
                        
                        # more than one value.  Not sure what to do... Will have
                        #    to figure this out eventually.
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
                                current_attribute_value_model = current_attribute_value_QS.get()
                                
                                # update.
                                current_attribute_value_model.value = current_attribute_value
                                
                                # save
                                current_attribute_value_model.save()
                                
                            #-- END check to see if not missing. --#
                            
                        #-- END check to see if overwrite. --#
                        
                    #-- END check to see just how many values there are (should only be one?) --#
                    
                else:
                    
                    # no value for this attribute yet.  Add one.
                    # got value?
                    current_attribute_value = self.get_attribute_value( current_attribute, "missing" )
                    if ( current_attribute_value != "missing" ):
                        
                        # yes, add it.
                        # - what is this??? - current_attribute_model.node_type_attribute_set.create( node_type_attribute_id = current_attribute_type_id, value = current_attribute_value )
                        my_node.node_type_attribute_value_set.create( node_type_attribute = current_definition, value = current_attribute_value )
                        
                    #-- END check to see if value present. --# 
                    
                #-- END check to see if value already exists.
                
            #-- END loop over definitions. --#
                
        #-- END check to make sure we have a node. --#
        
        return status_OUT        
        
    #-- END method save_attribute_values() --#


#-- END class AttributeContainer --#