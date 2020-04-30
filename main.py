from model import itemScheme
from datetime import datetime

conceptParent = itemScheme.Concept()
conceptChild = itemScheme.Concept()
code = itemScheme.Code()


a = conceptChild.__class__
b = conceptParent.__class__

c = a == b

conceptChild.parent = conceptParent


a = conceptChild