from zope.schema.fieldproperty import FieldProperty
from zope.component.factory import Factory
from zope import interface
from interfaces import IDirectoryFieldIndexMap

@interface.implementer(IDirectoryFieldIndexMap)
class DirectoryFieldIndexMap(object):
    
    def __init__(self, map=None):
        self.map = map if map else {}
    map = FieldProperty(IDirectoryFieldIndexMap['map'])
directoryFieldIndexMapFactory = Factory(DirectoryFieldIndexMap)