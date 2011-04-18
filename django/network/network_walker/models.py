from django.db import models

# Create your models here.
# TODO - Add time stamps where appropriate (at least Node, Tie).
# TODO - Add table to hold network query inputs for some or all attempts to
#    build a network, so you can reprodice later on.

#================================================================================
# Nodes
#================================================================================

# NodeType model
class NodeType( models.Model ):

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

#-- END NodeType Model --#


# NodeTypeAttribute model - attributes that contain traits of a given type.
class NodeTypeAttribute( models.Model ):

    '''
    Model NodeTypeAttribute holds the names and traits of different
       attributes for each type.
    '''

    #----------------------------------------------------------------------
    # fields
    #----------------------------------------------------------------------

    name = models.CharField( max_length=255 )
    description = models.TextField( blank = True, null = True )
    node_type = models.ForeignKey( NodeType )
    
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

#-- END NodeTypeAttribute Model --#


# NodeTypeAttributeValidValue - valid values for a given type attribute.
class NodeTypeAttributeValidValue( models.Model ):

    '''
    Model NodeTypeAttributeValidValue holds valid values for a given attribute.
       If none are associated with a given attribute, that attribute is a
       free-form text field.
    '''

    #----------------------------------------------------------------------
    # fields
    #----------------------------------------------------------------------

    node_type_attribute = models.ForeignKey( NodeTypeAttribute )
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

#-- END NodeTypeAttributeValidValue Model --#


# Node Model
class Node( models.Model ):

    '''
    Model Node is the base model for holding information on nodes.  Info. common
       to all nodes is contained in this class.  Values specific to different
       types of nodes are stored in NodeTypeAttributeValue.
    '''

    #----------------------------------------------------------------------
    # fields
    #----------------------------------------------------------------------

    node_type = models.ForeignKey( NodeType )
    parent_node = models.ForeignKey( Node, blank = True, null = True ) # (optional - if present, then this is a group as well as a node)
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


# NodeTypeAttributeValue - valid values for a given type.
class NodeTypeAttributeValue( models.Model ):

    '''
    Model NodeTypeAttributeValue is a Model intended to hold the specific values
       of traits for each node of a given type.
    '''

    #----------------------------------------------------------------------
    # fields
    #----------------------------------------------------------------------

    node = models.ForeignKey( Node )
    node_type_attribute = models.ForeignKey( NodeTypeAttribute )
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

#-- END NodeTypeAttributeValue Model --#


#================================================================================
# Ties
#================================================================================

# TieType model
class TieType( models.Model ):

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

#-- END TieType Model --#


# TieTypeAttribute model - attributes that contain traits of a given type.
class TieTypeAttribute( models.Model ):

    '''
    Model TieTypeAttribute holds the names and traits of different
       attributes for each type.
    '''

    #----------------------------------------------------------------------
    # fields
    #----------------------------------------------------------------------

    name = models.CharField( max_length=255 )
    description = models.TextField( blank = True, null = True )
    tie_type = models.ForeignKey( TieType )
    
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

#-- END TieTypeAttribute Model --#


# TieTypeAttributeValidValue - valid values for a given type attribute.
class TieTypeAttributeValidValue( models.Model ):

    '''
    Model TieTypeAttributeValidValue holds valid values for a given attribute.
       If none are associated with a given attribute, that attribute is a
       free-form text field.
    '''

    #----------------------------------------------------------------------
    # fields
    #----------------------------------------------------------------------

    tie_type_attribute = models.ForeignKey( TieTypeAttribute )
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

#= END TieTypeAttributeValidValue Model ========================================================


# Tie Model
class Tie( models.Model ):

    '''
    Model Tie is the base model for holding information on ties.  Info. common
       to all ties is contained in this class.  Values specific to different
       types of ties for each tie are stored in TieTypeAttributeValue.
    '''

    #----------------------------------------------------------------------
    # fields
    #----------------------------------------------------------------------

    tie_type = models.ForeignKey( TieType )
    original_id = models.CharField( max_length = 255, blank = True, null = True )
    original_table = models.CharField( max_length = 255, blank = True, null = True )
    description = models.TextField( blank = True, null = True )
    from_node = models.ForeignKey( Node )
    to_node = models.ForeignKey( Node )
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


# TieTypeAttributeValue - valid values for a given type.
class TieTypeAttributeValue( models.Model ):

    '''
    Model TieTypeAttributeValue is a Model intended to hold the specific values
       of traits for each node of a given type.
    '''

    #----------------------------------------------------------------------
    # fields
    #----------------------------------------------------------------------

    node = models.ForeignKey( Node )
    node_type_attribute = models.ForeignKey( NodeTypeAttribute )
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

#= END TieTypeAttributeValue Model ========================================================