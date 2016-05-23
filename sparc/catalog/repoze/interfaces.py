from zope.interface import Interface
from zope import schema

class IDocumentMap(Interface):
    """Marker for repoze.catalog.document.DocumentMap objects"""

class IRepozeCatalog(Interface):
    """Marker for repoze.catalog.catalog.Catalog objects"""

class ISparcRepozeCatalog(Interface):
    """Container for a Repoze catalog and related document id mapper"""
    doc_map = schema.Field(
            title = u'Repoze Document Map',
            description = u'A document map for the catalog indexes',
            required = True,
            constraint = lambda o: IDocumentMap.providedBy(o)
            )
    catalog = schema.Field(
            title = u'Repoze Catalog',
            description = u'A Repoze catalog',
            required = True,
            constraint = lambda o: IRepozeCatalog.providedBy(o)
            )

class IFieldMapFromRepozeCatalogindexes(Interface):
    """Create field map from catalog indexes"""
    def __call__(catalog):
        """"Returns IDirectoryFieldIndexMap generated from ISparcRepozeCatalog 
            catalog index names
        
        The catalog indexes will be iterated through.  indexes whose names do not 
        end with:
            _facet
            _field
            _keyword
            _path
            _path2
            _text
        will be added to the field map. directly.  Those matching any entry in the
        above list will be added to a field named with the preceding string before
        the starting '_'.
        """