"""
Some utilities
"""
import pickle
from . import admin_settings

def getBlobProperties(item, fieldName):
    props = getattr(item, fieldName + admin_settings.BLOB_FIELD_META_SUFFIX, None)
    if props:
        return pickle.loads(props)
    else:
        return None
