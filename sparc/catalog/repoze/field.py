from zope.component import createObject
from zope.interface import implements
from interfaces import IFieldMapFromRepozeCatalogindexes

class FieldMapFromRepozeCatalogindexes(object):
    implements(IFieldMapFromRepozeCatalogindexes)
    def __call__(self, catalog):
        fm = createObject(u"sparc.catalog.field_map")
        for index in catalog:
            _matched = ''
            for suffix in \
                    ['_facet', '_field', '_keyword', '_path', '_path2', '_text']:
                if index.endswith(suffix):
                    _matched = index[0:-len(suffix)]
                    break
            field = _matched if _matched else index
            if field not in fm.map:
                fm.map[field] = set([index])
            else:
                fm.map[field].add(index)
        return fm