# -*- coding: utf-8 -*-
"""
Demo of unicode support in text and labels.
"""
from __future__ import unicode_literals
from bidi import algorithm as bidialg
import matplotlib.pyplot as plt


plt.title(bidialg.get_display(u'گراف الکی'))
plt.xlabel("محور الکی")
plt.ylabel('من اینجام')
plt.text(0.2, 0.8, 'گراف تست', rotation=45)
plt.text(0.4, 0.2, 'AVA (check kerning)')

plt.show()
