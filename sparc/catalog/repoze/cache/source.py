from sparc.cache import ICachableItem

class CachableSourceForDirectoryMixin(object):
    #implements(ICachableSource)
    #adapts(IDirectory)
    """implementers to set which interfaces should be filter for in the 
    directory.  There must be an available adapter that will convert these
    object into a ICachableItem.
    
    There is a ICachableItem adapter for sparc.entity.IEntity objects available
    in the sparc.cache package.
    """
    interfaces = ()
    _key = 'id'
    
    def __init__(self, context):
        self.context = context

    def key(self):
        """Returns string identifier key that marks unique item entries (e.g. 
        primary key fieldname)
        """
        return self._key
    
    def items(self):
        """Returns an iterable of available ICachableItem in the ICachableSource"""
        for item in self.context.values(interfaces=self.interfaces):
            yield ICachableItem(item)
    
    def getById(self, Id):
        """Returns ICachableItem that matches Id or None if not found"""
        items = list(self.context.search(Id, fields=(id,), interfaces=self.interfaces))
        if len > 1:
            raise LookupError('Did not expect to find more than one search result for given Id')
        return items[0] if items else None
    
    def first(self):
        """Returns the first ICachableItem available in the ICachableSource or None"""
        items = self.items()
        return items.next()