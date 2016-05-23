from repoze.catalog.indexes.field import CatalogFieldIndex
from repoze.catalog.indexes.text import CatalogTextIndex
from repoze.catalog.interfaces import ICatalog
from zope.component import createObject
from zope.component.factory import Factory
from zope.interface import implementer

@implementer(ICatalog)
def entity_catalog_factory_helper():
    # text indexes will be normalized to lower-case
    catalog = createObject(u"sparc.catalog.repoze.repoze_identified_catalog")
    catalog['name'] = CatalogFieldIndex('name')
    # Text indexes are case-insensitive and can be searched with wildcards
    catalog['name_text'] = CatalogTextIndex('name')
    catalog['description'] = CatalogTextIndex('description')
    catalog['details'] = CatalogTextIndex('details')
    return catalog

entityCatalogFactory = Factory(entity_catalog_factory_helper)