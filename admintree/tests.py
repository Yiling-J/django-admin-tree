from django.test import TestCase

from .models import Tree, TreeNode, TreePath


class TreeTest(TestCase):

    def test_tree(self):
        response = self.client.get("/tree/")
        self.assertEqual(response.status_code, 404)
        tree = Tree.objects.create(name='T1')
        tree2 = Tree.objects.create(name='T2')
        node1 = TreeNode.objects.create(title='n1', type='Object')
        node2 = TreeNode.objects.create(title='n2', type='Object')
        node3 = TreeNode.objects.create(title='n3', type='Object')
        node4 = TreeNode.objects.create(title='n4', type='Object')
        TreePath.objects.create(node_from=tree.start_node, node_to=node1, order=0, tree=tree)
        TreePath.objects.create(node_from=tree.start_node, node_to=node2, order=1, tree=tree)
        TreePath.objects.create(node_from=node1, node_to=node3, order=0, tree=tree)
        TreePath.objects.create(node_from=tree2.start_node, node_to=node4, order=0, tree=tree2)

        response = self.client.get("/tree/T1/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]['Title'], node1.title)
        self.assertEqual(len(response.json()[0]['Children']), 1)
        self.assertEqual(response.json()[0]['Children'][0]['Title'], node3.title)
        self.assertEqual(response.json()[1]['Title'], node2.title)
        response = self.client.get("/tree/T2/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['Title'], node4.title)
