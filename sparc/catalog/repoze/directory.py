from BTrees.OOBTree import OOBTree
from repoze.catalog.query import And
from repoze.catalog.query import Or
from repoze.catalog.query import Eq
from zope import interface
from zope import component
from sparc.catalog import IDirectory
from sparc.catalog import IDirectoryFieldIndexMap
from .. import IIdentified
from interfaces import ISparcRepozeCatalog

@interface.implementer(IDirectory)
@component.adapter(ISparcRepozeCatalog, IDirectoryFieldIndexMap)
class SparcDirectory(object):
    
    def __init__(self, catalog, fields):
        self.catalog = catalog
        self._fields = fields
        self._doc_map = catalog.doc_map
        self._catalog = catalog.catalog # this is the actual Repoze catalog
        self._map = OOBTree() # keys are IIdentified.id, values are the object
    
    #IDirectory
    def __setitem__(self, key, value):
        """Update IIdentified in directory.  key is IIdentified.id"""
        if key != IIdentified(value).getId():
            raise KeyError("expected key to match value.getId()")
        
        doc_id = self._doc_map.docid_for_address(key)
        if doc_id:
            self._catalog.reindex_doc(doc_id, value)
        else:
            doc_id = self._doc_map.add(key)
            self._catalog.index_doc(doc_id, value)
        self._map[key] = value

    def add(self, value):
        """Add IIdentified in directory, silently replaces any conflict."""
        self[IIdentified(value).getId()] = value

    def update(self, value, fields=()):
        """Update IIdentified in directory.  If fields, then only these fields 
        are updated if possible.  If value is not in directory, it is added"""
        # repoze catalogs don't seem to offer this capability...so we'll update
        # all the indexes
        self.add(value)

    def __delitem__(self, key):
        """Remove IIdentified.id from directory"""
        doc_id = self._doc_map.docid_for_address(key)
        if not doc_id:
            if key in self._map:
                raise LookupError("internal data structure is corrupt, unable to find document id")
            raise KeyError(key)
        self._catalog.unindex_doc(doc_id)
        self._doc_map.remove_docid(doc_id)
        del self._map[key]

    def remove(self, value):
        """Remove IIdentified from directory.  KeyError raised if IIdentified not in directory"""
        del self[IIdentified(value).getId()]
    
    def discard(self, value):
        """Remove IIdentified from directory if present."""
        try:
            self.remove(value)
        except KeyError:
            pass
    
    #IDirectoryLookup
    def __getitem__(self, key):
        """Return IIdentified for given key (IIdentified.id)"""
        return self._map[key]
    def __contains__(self, key):
        """True if key (IIdentified.id) is in directory"""
        return key in self._map
    def contains(self, value):
        """True if IIdentified is in directory"""
        return IIdentified(value).getId() in self._map
        
    def __iter__(self):
        """Generator of all readable & available keys (IIdentified.id) in directory"""
        for key in self._map:
            yield key
    
    def values(self, interfaces=None):
        """Generator of all readable & available IIdentified objects in directory
        
        If interfaces is given, then result is filtered for objects providing
        the given interfaces.
        """
        if not interfaces:
            for key in self._map:
                yield self._map[key]
        else:
            query = Or(*[Eq('interfaces', iface.__identifier__) for \
                                                         iface in interfaces])
            results = self._catalog.query(query)
            for doc_id in results[1]:
                yield self._map[self._doc_map.address_for_docid(doc_id)]
    
    def fields(self):
        """Return list of field names that are indexed and searchable"""
        return [f for f in self._fields.map if f != 'interfaces']
    
    def search(self, term, fields=None, interfaces=None):
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
        fields = fields if fields else self._fields.map.keys()
        interfaces = interfaces if interfaces else []
        query_fields = []
        for field in fields:
            for index in self._fields.map[field]:
                # for searching, it seemed that we'd have to pick between
                # Eq() for most indexes, but use Contains() for text...but
                # testing showed that Eq() for text indexes acts like you'd
                # expect Contains().  So we'll use Eq() for all index types
                query_fields.append(Eq(index, term))
        query_ifaces = [Eq('interfaces', iface.__identifier__) for \
                                                        iface in interfaces]
        query = Or(*query_fields) if not query_ifaces else \
                                                And(Or(*query_fields), \
                                                    Or(*query_ifaces))
        results = self._catalog.query(query)
        for doc_id in results[1]:
            yield self._map[self._doc_map.address_for_docid(doc_id)]
    