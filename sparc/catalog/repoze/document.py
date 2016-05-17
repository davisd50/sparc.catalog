from repoze.catalog.document import DocumentMap
from zope.component.factory import Factory
from zope.interface import implementer
from interfaces import IDocumentMap

@implementer(IDocumentMap)
def repoze_documentmap_factory_helper():
    return DocumentMap() # implements IDocumentMap via zcml directive

repozeDocumentmapFactory = Factory(repoze_documentmap_factory_helper)