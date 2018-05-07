# coding: utf-8
from __future__ import unicode_literals

import factory
from factory.django import DjangoModelFactory
from models import Tree, TreeNode, TreePath


class TreeFactory(DjangoModelFactory):
    class Meta:
        model = Tree


class TreeNodeFactory(DjangoModelFactory):
    class Meta:
        model = TreeNode

    title = factory.Sequence(lambda n: 'node %d' % n)
    type = 'DishCharEnglishName'


class TreePathFactory(DjangoModelFactory):
    class Meta:
        model = TreePath
