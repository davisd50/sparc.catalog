from repoze.catalog.indexes.field import CatalogFieldIndex
from repoze.catalog.indexes.keyword import CatalogKeywordIndex
from repoze.catalog.indexes.text import CatalogTextIndex
from repoze.catalog.interfaces import ICatalog
from zope.component import createObject
from zope.component.factory import Factory
from zope.interface import implementer
from zope.interface import providedBy
from zope.interface.exceptions import DoesNotImplement
from sparc.entity import IEntity
from interfaces import IDocumentMap


class KeywordIndexRelatedEntities(object):
    """Return keyword index for entities found is object attributes
    
    Related entities will also be indexed.
    """
    def __init__(self, catalog, doc_map):
        self.catalog = catalog
        self.doc_map = doc_map
    def index_doc(self, object):
        doc_id = self.doc_map.docid_for_address(object.getId())
        if not doc_id:
            doc_id = self.doc_map.add(object.getId())
        self.catalog.index_doc(doc_id, object)
    def __call__(self, object, default):
        entities = []
        for iface in list(providedBy(object).flattened()):
            for name in iface:
                attr = getattr(object, name, None)
                if IEntity.providedBy(attr):
                    self.index_doc(attr)
                    entities.append(attr.getId())
                elif not isinstance(attr, basestring):
                    try:
                        for item in getattr(object, name, []):
                            if IEntity.providedBy(item):
                                self.index_doc(item)
                                entities.append(item.getId())
                    except TypeError: # catches non-iterables
                        pass
        return entities

@implementer(ICatalog)
def entity_catalog_factory_helper(doc_map=None):
    if doc_map and not IDocumentMap.providedBy(doc_map):
        raise DoesNotImplement(IDocumentMap)
    catalog = createObject(u"sparc.catalog.repoze.repoze_identified_catalog")
    catalog['name'] = CatalogFieldIndex('name')
    # Text indexes are case-insensitive and can be searched with wildcards
    catalog['name_text'] = CatalogTextIndex('name')
    catalog['description'] = CatalogTextIndex('description')
    catalog['details'] = CatalogTextIndex('details')
    index_entities = KeywordIndexRelatedEntities(catalog, doc_map)
    if doc_map:
        catalog['entities'] = CatalogKeywordIndex(index_entities)
    return catalog

entityCatalogFactory = Factory(entity_catalog_factory_helper)