from django.db import models

# Create your models here.
# TODO - Add time stamps where appropriate (at least Node, Tie).
# TODO - Add table to hold network query inputs for some or all attempts to
#    build a network, so you can reproduce later on.


# Attribute_Type model
class Attribute_Type( models.Model ):

    '''
    Model Attribute_Type holds types of attributes, for use in allowing
       people to select against them when building networks.  This is a
       basic one - the types will be stuff like string, date, datetime,
       integer, real, etc.  I will probably make a fixture for this file,
       so it is automatically populated.
    '''

    #----------------------------------------------------------------------
    # fields
    #----------------------------------------------------------------------

    name = models.CharField( max_length=255 )
    description = models.TextField( blank = True, null = True )

    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------


    def __unicode__( self ):

        # return reference
        string_OUT = ''

        # declare variables
        string_OUT = str( self.id ) + " - " + self.name
        
        return string_OUT
        
    #-- END method __unicode__() --#

#-- END Attribute_Type Model --#


# Dated_Model abstract model
class Dated_Model( models.Model ):

    '''
    Dated_Model implements a date field and date range start and end date
       fields.  Not sure which of these will be needed where, but will make
       node, tie, and node and tie attribute values classes extend so each
       of these can be dated, and so dates can be used to pull in nodes,
       ties, or attribute values for a date or a date range.
    '''

    date = models.DateTimeField( blank = True, null = True )
    date_range_start = models.DateTimeField( blank = True, null = True )
    date_range_end = models.DateTimeField( blank = True, null = True )
    create_date = models.DateTimeField( auto_now_add = True )
    last_update = models.DateTimeField( auto_now = True )

    # meta class so we know this is an abstract class.
    class Meta:
        abstract = True

    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------


    def __unicode__( self ):
        
        # return reference
        string_OUT = ''
        prefix = ""
        
        string_OUT = self.id
        prefix = " - "
        
        if ( self.date ):
            string_OUT = prefix + "date: " + self.date.strftime( "%b %d, %Y" )
            prefix = ", "
            
        #-- END check for date field --#
            
        if ( self.range_start_date ):
            string_OUT = prefix + "range start date: " + self.range_start_date.strftime( "%b %d, %Y" )
            prefix = ", "
            
        #-- END check for range_start_date field --#

        if ( self.range_end_date ):
            string_OUT = prefix + "range end date: " + self.range_end_date.strftime( "%b %d, %Y" )
            prefix = ", "
            
        #-- END check for range_end_date field --#

        return string_OUT
        
    #-- END __unicode__() method --#
        

#= END Article_Person Model ======================================================


#================================================================================
# Nodes
#================================================================================

# Node_Type model
class Node_Type( models.Model ):

    '''
    Model NodeType holds types of nodes, so you can store many types of
       nodes in one node table, differentiating between them by their
       types.
    '''

    #----------------------------------------------------------------------
    # fields
    #----------------------------------------------------------------------

    name = models.CharField( max_length=255 )
    description = models.TextField( blank = True, null = True )

    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------


    def __unicode__( self ):

        # return reference
        string_OUT = ''

        # declare variables
        string_OUT = str( self.id ) + " - " + self.name
        
        return string_OUT
        
    #-- END method __unicode__() --#

#-- END Node_Type Model --#


# Node_Type_Attribute model - attributes that contain traits of a given type.
class Node_Type_Attribute( models.Model ):

    '''
    Model NodeTypeAttribute holds the names and traits of different
       attributes for each type.
    '''

    #----------------------------------------------------------------------
    # fields
    #----------------------------------------------------------------------

    name = models.CharField( max_length=255 )
    description = models.TextField( blank = True, null = True )
    node_type = models.ForeignKey( Node_Type )
    attribute_type = models.ForeignKey( Attribute_Type )
    
    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------


    def __unicode__( self ):

        # return reference
        string_OUT = ''

        # declare variables
        string_OUT = str( self.id ) + " - " + self.name
        
        return string_OUT
        
    #-- END method __unicode__() --#

#-- END Node_Type_Attribute Model --#


# Node_Type_Attribute_Valid_Value - valid values for a given type attribute.
class Node_Type_Attribute_Valid_Value( models.Model ):

    '''
    Model NodeTypeAttributeValidValue holds valid values for a given attribute.
       If none are associated with a given attribute, that attribute is a
       free-form text field.
    '''

    #----------------------------------------------------------------------
    # fields
    #----------------------------------------------------------------------

    node_type_attribute = models.ForeignKey( Node_Type_Attribute )
    value = models.CharField( max_length=255 )
    description = models.TextField( blank = True, null = True )

    
    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------


    def __unicode__( self ):

        # return reference
        string_OUT = ''

        # declare variables
        string_OUT = str( self.id ) + " - " + self.name
        
        return string_OUT
        
    #-- END method __unicode__() --#

#-- END Node_Type_Attribute_Valid_Value Model --#


# Node Model
class Node( Dated_Model ):

    '''
    Model Node is the base model for holding information on nodes.  Info. common
       to all nodes is contained in this class.  Values specific to different
       types of nodes are stored in NodeTypeAttributeValue.
    '''

    #----------------------------------------------------------------------
    # fields
    #----------------------------------------------------------------------

    node_type = models.ForeignKey( Node_Type )
    parent_node = models.ForeignKey( "Node", blank = True, null = True ) # (optional - if present, then this is a group as well as a node)
    original_id = models.CharField( max_length = 255, blank = True, null = True )
    original_table = models.CharField( max_length = 255, blank = True, null = True )
    description = models.TextField( blank = True, null = True )
    #more to come

    
    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------


    def __unicode__( self ):

        # return reference
        string_OUT = ''

        # declare variables
        string_OUT = str( self.id ) + " - " + self.name
        
        return string_OUT
        
    #-- END method __unicode__() --#

#-- END Node Model --#


# Node_Type_Attribute_Value - valid values for a given type.
class Node_Type_Attribute_Value( Dated_Model ):

    '''
    Model NodeTypeAttributeValue is a Model intended to hold the specific values
       of traits for each node of a given type.
    '''

    #----------------------------------------------------------------------
    # fields
    #----------------------------------------------------------------------

    node = models.ForeignKey( Node )
    node_type_attribute = models.ForeignKey( Node_Type_Attribute )
    value = models.TextField( blank = True, null = True )
    
    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------


    def __unicode__( self ):

        # return reference
        string_OUT = ''

        # declare variables
        string_OUT = str( self.id ) + " - " + self.name
        
        return string_OUT
        
    #-- END method __unicode__() --#

#-- END Node_Type_Attribute_Value Model --#


#================================================================================
# Ties
#================================================================================

# Tie_Type model
class Tie_Type( models.Model ):

    '''
    Model TieType holds types of ties, so you can store many types of
       ties in one tie table, differentiating between them by their
       types.
    '''

    #----------------------------------------------------------------------
    # fields
    #----------------------------------------------------------------------

    name = models.CharField( max_length=255 )
    description = models.TextField( blank = True, null = True )
    directed = models.BooleanField( 'Is Directed?', default = True )

    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------


    def __unicode__( self ):

        # return reference
        string_OUT = ''

        # declare variables
        string_OUT = str( self.id ) + " - " + self.name
        
        return string_OUT
        
    #-- END method __unicode__() --#

#-- END Tie_Type Model --#


# Tie_Type_Attribute model - attributes that contain traits of a given type.
class Tie_Type_Attribute( models.Model ):

    '''
    Model TieTypeAttribute holds the names and traits of different
       attributes for each type.
    '''

    #----------------------------------------------------------------------
    # fields
    #----------------------------------------------------------------------

    name = models.CharField( max_length=255 )
    description = models.TextField( blank = True, null = True )
    tie_type = models.ForeignKey( Tie_Type )
    attribute_type = models.ForeignKey( Attribute_Type )
    
    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------


    def __unicode__( self ):

        # return reference
        string_OUT = ''

        # declare variables
        string_OUT = str( self.id ) + " - " + self.name
        
        return string_OUT
        
    #-- END method __unicode__() --#

#-- END Tie_Type_Attribute Model --#


# Tie_Type_Attribute_Valid_Value - valid values for a given type attribute.
class Tie_Type_Attribute_Valid_Value( models.Model ):

    '''
    Model TieTypeAttributeValidValue holds valid values for a given attribute.
       If none are associated with a given attribute, that attribute is a
       free-form text field.
    '''

    #----------------------------------------------------------------------
    # fields
    #----------------------------------------------------------------------

    tie_type_attribute = models.ForeignKey( Tie_Type_Attribute )
    value = models.CharField( max_length=255 )
    description = models.TextField( blank = True, null = True )

    
    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------


    def __unicode__( self ):

        # return reference
        string_OUT = ''

        # declare variables
        string_OUT = str( self.id ) + " - " + self.name
        
        return string_OUT
        
    #-- END method __unicode__() --#

#= END Tie_Type_Attribute_Valid_Value Model ========================================================


# Tie Model
class Tie( Dated_Model ):

    '''
    Model Tie is the base model for holding information on ties.  Info. common
       to all ties is contained in this class.  Values specific to different
       types of ties for each tie are stored in TieTypeAttributeValue.
    '''

    #----------------------------------------------------------------------
    # fields
    #----------------------------------------------------------------------

    tie_type = models.ForeignKey( Tie_Type )
    original_id = models.CharField( max_length = 255, blank = True, null = True )
    original_table = models.CharField( max_length = 255, blank = True, null = True )
    description = models.TextField( blank = True, null = True )
    from_node = models.ForeignKey( Node, related_name = "ties_out" )
    to_node = models.ForeignKey( Node, related_name = "ties_in" )
    directed = models.BooleanField( 'Is Directed?', default = True )
    #more to come

    
    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------


    def __unicode__( self ):

        # return reference
        string_OUT = ''

        # declare variables
        string_OUT = str( self.id ) + " - " + self.name
        
        return string_OUT
        
    #-- END method __unicode__() --#

#= END Tie Model ========================================================


# Tie_Type_Attribute_Value - valid values for a given type.
class Tie_Type_Attribute_Value( Dated_Model ):

    '''
    Model TieTypeAttributeValue is a Model intended to hold the specific values
       of traits for each node of a given type.
    '''

    #----------------------------------------------------------------------
    # fields
    #----------------------------------------------------------------------

    node = models.ForeignKey( Node )
    node_type_attribute = models.ForeignKey( Node_Type_Attribute )
    value = models.TextField( blank = True, null = True )
    
    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------


    def __unicode__( self ):

        # return reference
        string_OUT = ''

        # declare variables
        string_OUT = str( self.id ) + " - " + self.name
        
        return string_OUT
        
    #-- END method __unicode__() --#

#= END Tie_Type_Attribute_Value Model ========================================================