from django.db import models

# TODO - Add table to hold network query inputs for some or all attempts to
#    build a network, so you can reproduce later on.

#===============================================================================
# Abstract Models
#===============================================================================


# Labeled_Model abstract model
class Labeled_Model( models.Model ):

    '''
    Labeled_Model implements a label (intended to have no space), a name
       field, and a description field.  Many models have these fields
       together, so figured I'd just plunk them all in one place.
    '''

    #----------------------------------------------------------------------
    # fields
    #----------------------------------------------------------------------

    label = models.CharField( max_length = 255 )
    name = models.CharField( max_length = 255 )
    description = models.TextField( blank = True, null = True )

    # meta class so we know this is an abstract class.
    class Meta:
        abstract = True

    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------


    def __unicode__( self ):

        # return reference
        string_OUT = ''

        # declare variables
        string_OUT = str( self.id ) + " - " + self.name + " ( " + self.label + " )"
        
        return string_OUT
        
    #-- END method __unicode__() --#

#= END Labeled_Model Abstract Model ============================================


# Derived_Model abstract model
class Derived_Attribute_Model( Labeled_Model ):

    '''
    Labeled_Model implements a label (intended to have no space), a name
       field, and a description field.  Many models have these fields
       together, so figured I'd just plunk them all in one place.
    '''

    #----------------------------------------------------------------------
    # fields
    #----------------------------------------------------------------------

    # Inherited from Derived_Model
    #label = models.CharField( max_length = 255 )
    #name = models.CharField( max_length = 255 )
    #description = models.TextField( blank = True, null = True )
    attribute_type = models.ForeignKey( "Attribute_Type" )
    attribute_derivation_type = models.ForeignKey( "Attribute_Derivation_Type", blank = True, null = True )
    derived_from = models.CharField( max_length = 255, blank = True, null = True )
   

    # meta class so we know this is an abstract class.
    class Meta:
        abstract = True

    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------


    def __unicode__( self ):

        # return reference
        string_OUT = ''

        # declare variables
        string_OUT = str( self.id ) + " - " + self.name + " ( " + self.label + " ); derived from " + self.derived_from
        
        return string_OUT
        
    #-- END method __unicode__() --#
    
    
    def get_derivation_type_label( self ):
        
        # return reference
        value_OUT = ""
        
        # declare variables
        derivation_type = None
        
        # get derivation type
        derivation_type = self.attribute_derivation_type
        
        # got one?
        if ( derivation_type ):
            
            # yes. Get label.
            value_OUT = derivation_type.label
            
        #-- END check to make sure we have a derivation type.  --#
        
        return value_OUT
        
    #-- END method get_derivation_type_label() --#
    

#= END Derived_Model Abstract Model ============================================


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
        

#= END Dated_Model Abstract Model ==============================================


#===============================================================================
# Shared Models
#===============================================================================


# Attribute_Type model
class Attribute_Type( Labeled_Model ):

    '''
    Model Attribute_Type holds types of attributes, for use in allowing
       people to select against them when building networks.  This is a
       basic one - the types will be stuff like string, date, datetime,
       integer, real, etc.  I will probably make a fixture for this file,
       so it is automatically populated.  For now, this is entirely inherited
       from Labeled_Model.
    '''

#-- END Attribute_Type Model --#


# Attribute_Type model
class Attribute_Derivation_Type( Labeled_Model ):

    '''
    Model Derived_Attribute_Type holds derivation types for attributes.  To
       start, will just have property and method.  This can be used to guide
       the AttributeContainer when it is pulling in attribute values from an
       external source.  Used in combination with the derived_from field on the
       model that has a derived attribute type (should put the name of the
       property or method in that field).
    '''

#-- END Attribute_Type Model --#


#===============================================================================
# Node Models
#===============================================================================

# Node_Type model
class Node_Type( Labeled_Model ):

    '''
    Model NodeType holds types of nodes, so you can store many types of
       nodes in one node table, differentiating between them by their
       types.  Entirely inherited from Labeled_Model at the moment.
    '''

    # Inherited from Labeled_Model
    #label = models.CharField( max_length = 255 )
    #name = models.CharField( max_length = 255 )
    #description = models.TextField( blank = True, null = True )

#-- END Node_Type Model --#


# Node_Type_Attribute model - attributes that contain traits of a given type.
class Node_Type_Attribute( Derived_Attribute_Model ):

    '''
    Model NodeTypeAttribute holds the names and traits of different
       attributes for each type.
    '''

    #----------------------------------------------------------------------
    # fields
    #----------------------------------------------------------------------

    # Inherited from Derived_Attribute_Model
    #label = models.CharField( max_length = 255 )
    #name = models.CharField( max_length = 255 )
    #description = models.TextField( blank = True, null = True )
    #attribute_derivation_type = models.ForeignKey( "Attribute_Type" )
    #derive_type = models.ForeignKey( "Attribute_Derivation_Type", blank = True, null = True )
    #derived_from = models.CharField( max_length = 255, blank = True, null = True )
    node_type = models.ForeignKey( Node_Type )
    
    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------

    '''
    def __unicode__( self ):

        # return reference
        string_OUT = ''

        # declare variables
        string_OUT = str( self.id ) + " - " + self.name
        
        return string_OUT
        
    #-- END method __unicode__() --#
    '''

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
# Tie Models
#================================================================================

# Tie_Type model
class Tie_Type( Labeled_Model ):

    '''
    Model TieType holds types of ties, so you can store many types of
       ties in one tie table, differentiating between them by their
       types.
    '''

    #----------------------------------------------------------------------
    # fields
    #----------------------------------------------------------------------

    # Inherited from Labeled_Model
    #label = models.CharField( max_length = 255 )
    #name = models.CharField( max_length = 255 )
    #description = models.TextField( blank = True, null = True )

    directed = models.BooleanField( 'Is Directed?', default = True )

    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------

    '''
    def __unicode__( self ):

        # return reference
        string_OUT = ''

        # declare variables
        string_OUT = str( self.id ) + " - " + self.name
        
        return string_OUT
        
    #-- END method __unicode__() --#
    '''

#-- END Tie_Type Model --#


# Tie_Type_Attribute model - attributes that contain traits of a given type.
class Tie_Type_Attribute( Derived_Attribute_Model ):

    '''
    Model TieTypeAttribute holds the names and traits of different
       attributes for each type.
    '''

    #----------------------------------------------------------------------
    # fields
    #----------------------------------------------------------------------

    # Inherited from Derived_Attribute_Model
    #label = models.CharField( max_length = 255 )
    #name = models.CharField( max_length = 255 )
    #description = models.TextField( blank = True, null = True )
    #attribute_type = models.ForeignKey( "Attribute_Type" )
    #attribute_derivation_type = models.ForeignKey( "Attribute_Derivation_Type", blank = True, null = True )
    #derived_from = models.CharField( max_length = 255, blank = True, null = True )

    tie_type = models.ForeignKey( Tie_Type )
    
    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------

    '''
    def __unicode__( self ):

        # return reference
        string_OUT = ''

        # declare variables
        string_OUT = str( self.id ) + " - " + self.name
        
        return string_OUT
        
    #-- END method __unicode__() --#
    '''

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
    from_node = models.ForeignKey( Node, related_name = "ties_out_set" )
    to_node = models.ForeignKey( Node, related_name = "ties_in_set" )
    directed = models.BooleanField( 'Is Directed?', default = True )
    valid_node_types = models.ManyToManyField( Node_Type, blank = True, null = True )
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
       of traits for each tie of a given type.
    '''

    #----------------------------------------------------------------------
    # fields
    #----------------------------------------------------------------------

    tie = models.ForeignKey( Tie )
    tie_type_attribute = models.ForeignKey( Tie_Type_Attribute )
    value = models.TextField( blank = True, null = True )
    
    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------


    def __unicode__( self ):

        # return reference
        string_OUT = ''

        # declare variables
        string_OUT = str( self.id ) + " - " + self.value
        
        return string_OUT
        
    #-- END method __unicode__() --#

#= END Tie_Type_Attribute_Value Model ========================================================