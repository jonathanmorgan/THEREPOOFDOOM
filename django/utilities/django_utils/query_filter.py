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

class QueryFilterHelper():

    '''
    This class requires the django application.  It contains methods for using
       values in parameters to add filters to Django QuerySets
    '''

    #---------------------------------------------------------------------------
    # CONSTANTS-ish
    #---------------------------------------------------------------------------


    # names of parameters
    


    #---------------------------------------------------------------------------
    # __init__() method
    #---------------------------------------------------------------------------

    
    def __init__( self ):
        
        '''
        Constructor
        '''
        
        self.m_queryset = None        

    #-- END constructor --#


    #---------------------------------------------------------------------------
    # properties, in alphabetical order
    #---------------------------------------------------------------------------


    def get_queryset( self ):
    
        '''
        Returns QuerySet stored in internal instance variable.
        ''' 
        
        # return reference
        value_OUT = None
        
        value_OUT = self.m_queryset
        
        return value_OUT
    
    #-- END add_date_filter() --#


    def set_queryset( self, value_IN ):
    
        '''
        Accepts and stores QuerySet in internal instance variable.
        ''' 
        
        # return reference
        self.m_queryset = value_IN
    
    #-- END add_date_filter() --#


    queryset = property( get_queryset, set_queryset )


    #---------------------------------------------------------------------------
    # instance methods, in alphabetical order
    #---------------------------------------------------------------------------


    def add_date_filter( self, date_field_name_IN, start_date_IN, end_date_IN ):
    
        '''
        Accepts name of date field we want to filter, and optional start and end
           dates.  Depending on which date values are passed in, creates a date
           filter on column name in date_field_name_IN and appends it to the
           nested QuerySet, then updates the nested QuerySet instance so it
           points to the updated QuerySet and also returns the new QuerySet.
           
        Preconditions: assumes that there is a QuerySet nested in the instance.
        
        Postconditions: replaces existing QuerySet with newly filtered one at
           conclusion of execution.
           
        Parameters:
        - date_field_name_IN - String field name of date field we are filtering on.
        - start_date_IN - datetime.datetime instance that contains the start date and time from which we want to start filtering.  If empty, does not specify a start date.
        - end_date_IN - datetime.datetime instance that contains the end date and time at which we want to end filtering.  If empty, goes to present.           

        Returns:
        - QuerySet - updated QuerySet, also stored in the instance.
        '''
        
        # return reference
        queryset_OUT = None
        
        # Declare variables
        my_queryset = None
        
        # make sure we have a QuerySet.
        my_queryset = self.queryset
        
        # got a queryset?
        if ( my_queryset ):
            
            # make sure we have a field name and either a start or an end date.
            if ( ( date_field_name_IN ) and ( ( start_date_IN ) or ( end_date_IN ) ) ):
        
                # got both dates?
                if ( ( start_date_IN ) and ( end_date_IN ) ):
                
                    # yes - do a range.
                    #writeup_queryset = writeup_queryset.filter( createtime__range = ( start_date_IN, end_date_IN ) )
                    filter_params = {}
                    filter_params[ date_field_name_IN + "__range" ] = ( start_date_IN, end_date_IN )
                    my_queryset = my_queryset.filter( **filter_params )
                    
                    # store updated QuerySet
                    self.queryset = my_queryset
                    
                elif ( start_date_IN ):
                
                    # just start date - do gte
                    #writeup_queryset = writeup_queryset.filter( createtime__gte = start_date_IN )
                    filter_params = {}
                    filter_params[ date_field_name_IN + "__gte" ] = start_date_IN
                    my_queryset = my_queryset.filter( **filter_params )
                    
                    # store updated QuerySet
                    self.queryset = my_queryset
                    
                elif ( end_date_IN ):
                
                    # just end date - do lte
                    #writeup_queryset = writeup_queryset.filter( createtime__lte = end_date_IN )
                    filter_params = {}
                    filter_params[ date_field_name_IN + "__lte" ] = end_date_IN
                    my_queryset = my_queryset.filter( **filter_params )
                    
                    # store updated QuerySet
                    self.queryset = my_queryset
                    
                #-- END conditional over date range values.
                
            #-- END check to see if we have enough info. to filter. --#
        
        #-- END check to see if we have a queryset --#

        # return it also
        queryset_OUT = self.queryset
        
        return queryset_OUT
    
    #-- END add_date_filter() --#


    def set_order_by( self, order_by_list_IN ):
    
        '''
        Accepts List of string order by directives that we want to place on the
           nested QuerySet.  Adds them in the order they are listed in the List.
           For more details, see:
           http://docs.djangoproject.com/en/dev/ref/models/querysets/#order-by
           If empty list or None passed in, clears out the order_by.
           
        Preconditions: assumes that there is a QuerySet nested in the instance.
        
        Postconditions: replaces existing QuerySet with newly ordered one at
           conclusion of execution.
           
        Parameters:
        - order_by_list_IN - List of string order by directives that we want to place on the nested QuerySet, in the order we want them.  If empty list or None passed in, clears out the order_by.

        Returns:
        - QuerySet - updated QuerySet, also stored in the instance.
        '''
        
        # return reference
        queryset_OUT = None
        
        # Declare variables
        my_queryset = None
        
        # make sure we have a QuerySet.
        my_queryset = self.queryset
        if ( my_queryset ):
        
            # Got a list?       
            if ( ( order_by_list_IN ) and ( len( order_by_list_IN ) > 0 ) ):
        
                # add the order_by values.
                my_queryset = my_queryset.order_by( *order_by_list_IN )
                
            else:
            
                # nothing passed in, so empty out order_by.
                my_queryset = my_queryset.order_by()
                    
            #-- END check to see if we have enough info. to filter. --#
            
            self.queryset = my_queryset
            
        #-- END check to make sure we have a QuerySet.
        
        # return it also
        queryset_OUT = self.queryset
        
        return queryset_OUT
    
    #-- END set_order_by() --#


#-- END class QueryFilterHelper --#