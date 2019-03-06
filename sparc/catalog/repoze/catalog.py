from repoze.catalog.catalog import Catalog
from repoze.catalog.indexes.field import CatalogFieldIndex
from repoze.catalog.indexes.keyword import CatalogKeywordIndex
from repoze.catalog.interfaces import ICatalog
from persistent import Persistent
from repoze.catalog.document import DocumentMap
from zope.component.factory import Factory
from zope.interface import implementer
from zope.interface import providedBy
from zope.schema.fieldproperty import FieldProperty
from interfaces import ISparcRepozeCatalog

# A catalog based on sparc.entity.IIdentified
def index_interfaces_kw(object, default):
    provided = providedBy(object)
    interfaces = list(provided.flattened())
    if interfaces:
        return map(lambda i : i.__identifier__, interfaces)
    return default

@implementer(ICatalog)
def identifiedCatalogFactoryHelper():
    catalog = Catalog()
    catalog['id'] = CatalogFieldIndex('id')
    catalog['interfaces'] = CatalogKeywordIndex(index_interfaces_kw)
    return catalog
identifiedCatalogFactory = Factory(identifiedCatalogFactoryHelper)

@implementer(ISparcRepozeCatalog)
class SparcRepozeCatalog(object):
    
    def __init__(self, doc_map=None, catalog=None):
        self.doc_map = doc_map if doc_map else DocumentMap()
        self.catalog = catalog if catalog else Catalog()
    
    #ISparcRepozeCatalog
    doc_map = FieldProperty(ISparcRepozeCatalog['doc_map'])
    catalog = FieldProperty(ISparcRepozeCatalog['catalog'])
sparcRepozeCatalogFactory = Factory(SparcRepozeCatalog)

@implementer(ISparcRepozeCatalog)
class PersistentSparcRepozeCatalog(Persistent, SparcRepozeCatalog):
    pass
persistenSparcRepozeCatalogFactory = Factory(PersistentSparcRepozeCatalog)