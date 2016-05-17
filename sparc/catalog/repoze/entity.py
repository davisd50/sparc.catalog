from repoze.catalog.catalog import Catalog
from repoze.catalog.indexes.field import CatalogFieldIndex
from repoze.catalog.indexes.text import CatalogTextIndex
from repoze.catalog.interfaces import ICatalog
from zope.component.factory import Factory
from zope.interface import implementer

@implementer(ICatalog)
def entity_catalog_factory_helper():
    catalog = Catalog()
    catalog['id'] = CatalogFieldIndex('id')
    catalog['name'] = CatalogFieldIndex('name')
    catalog['name_text'] = CatalogTextIndex('name')
    catalog['description'] = CatalogTextIndex('description')
    catalog['details'] = CatalogTextIndex('details')
    return catalog

entityCatalogFactory = Factory(entity_catalog_factory_helper)