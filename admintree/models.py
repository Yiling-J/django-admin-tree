from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save


class Tree(models.Model):
    name = models.CharField(max_length=50)
    start_node = models.ForeignKey('TreeNode', blank=True, null=True)

    @staticmethod
    def signal_create_start_node(sender, instance, created, **kwargs):
        if created:
            instance.start_node = TreeNode.objects.create(title=instance.name, type='Root')
            instance.save()

    def __unicode__(self):
        return self.name


class TreeNode(models.Model):
    TYPE_CHOICE = (
        ('Object', 'Object'),
        ('Root', 'Root')
    )

    title = models.CharField(max_length=200, null=True, blank=True)
    type = models.CharField(max_length=200, choices=TYPE_CHOICE, default='None')
    child = models.ManyToManyField('self', through='TreePath', through_fields=('node_from', 'node_to'), symmetrical=False)

    def __unicode__(self):
        return self.title


class TreePath(models.Model):
    node_from = models.ForeignKey(TreeNode, related_name='children')
    node_to = models.ForeignKey(TreeNode, null=True, blank=True)
    order = models.IntegerField(default=0)
    tree = models.ForeignKey(Tree)

    def __unicode__(self):
        return self.node_from.title


post_save.connect(Tree.signal_create_start_node, sender=Tree)
