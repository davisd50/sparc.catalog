from zope import schema
from zope.interface import Interface

def _check_fm(fm):
    """Check Field Index map value types"""
    if not isinstance(fm, dict): return False
    for f in fm:
        if not isinstance(f, basestring): return False
        if not isinstance(fm[f], set): return False
        for m in fm[f]:
            if not isinstance(m, fm[f]): return False
    return True

class IDirectoryFieldIndexMap(Interface):
    """A map of field names to related index(es)
    
    This is expected to support all methods provided by a Python dictionary.
    Keys are string field names.  Values are sets of index names (strings) that
    should be referenced when searching the field name
    """
    map = schema.Dict(
            title = u'Field map',
            description = u'Keys are string field names, values are a set of '\
                            u'string index names',
            required = True,
            constraint = _check_fm
            )
    

class IDirectoryLookup(Interface):
    """A lookup directory for a sparc.entity.IIdentified objects"""
    def __getitem__(key):
        """Return IIdentified for given key (IIdentified.id)"""
    def __contains__(key):
        """True if key (IIdentified.id) is in directory"""
    def contains(value):
        """True if IIdentified is in directory"""
    def __iter__():
        """Generator of all readable & available keys (IIdentified.id) in directory"""
    def values(interfaces=None):
        """Generator of all readable & available IIdentified objects in directory
        
        If interfaces is given, then result is filtered for objects providing
        the given interfaces.
        """
    def fields():
        """Return list of field names that are indexed and searchable"""
    def search(term, fields=None, interfaces=None):
        """Search the directory
        
        Args:
            term: Term to search for
            fields: Iterable of fields to search against.  In most cases, a 
                    field identifies a list of indexes that will be search.
                    see IDirectoryFieldIndexMap and field.py for more
                    information.
            interfaces: Iterable of interfaces (objects, not strings) to 
                        filter results by.  All interfaces will be searched
                        by default.
        
        Returns:
            generator of IIdentified objects matching search criteria
        """

class IDirectory(IDirectoryLookup):
    """A writable directory for sparc.entity.IIdentified objects"""
    def __setitem__(key, value):
        """Update IIdentified in directory.  key is IIdentified.id"""
    def add(value):
        """Add IIdentified in directory, silently replaces any conflict."""
    def update(value, fields=()):
        """Update IIdentified in directory.  If fields, then only these fields 
        are updated if possible.  If value is not in directory, it is added"""
    def __delitem__(key):
        """Remove IIdentified.id from directory"""
    def remove(value):
        """Remove IIdentified from directory.  KeyError raised if IIdentified not in directory"""
    def discard(value):
        """Remove IIdentified from directory if present."""