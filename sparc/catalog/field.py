from zope.schema.fieldproperty import FieldProperty
from zope.component.factory import Factory
from zope.interface import implements
from interfaces import IDirectoryFieldIndexMap

class DirectoryFieldIndexMap(object):
    implements(IDirectoryFieldIndexMap)
    
    def __init__(self, map=None):
        self.map = map if map else {}
    map = FieldProperty(IDirectoryFieldIndexMap['map'])
directoryFieldIndexMapFactory = Factory(DirectoryFieldIndexMap)