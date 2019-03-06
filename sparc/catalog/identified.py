from zope import interface
from zope import component
from zope import schema
from zope.schema.fieldproperty import FieldProperty

try:
    from sparc.entity import IIdentified
except ImportError: 
    class IIdentified(interface.Interface):
        """Object that is identifiable"""
        def getId():
            """Return object ascii identifier"""
        id = schema.ASCIILine(
                title = u'Identifier',
                description = u'ASCII identifier for object',
                readonly = True,
                required = True
                )

@interface.implementer(IIdentified)
@component.adapter(interface.Interface)
class Identified(object):
    
    id = FieldProperty(IIdentified['id'])
    
    def __init__(self, context):
        self.id = getattr(context, 'id', '')
    
    def getId(self):
        return self.id