from django.http import JsonResponse as Response
from django.shortcuts import get_object_or_404
from django.views import View as APIView
import json

from models import Tree, TreeNode, TreePath


class TreeUpdateView(APIView):

    @staticmethod
    def node(id):
        return TreeNode.objects.get(id=id)

    def build_path(self, path, tree=None):
        path_json = path.get('children')
        pnode = self.node(path.get('id'))
        if path_json:
            for order, node in enumerate(path_json):
                cnode = self.node(node.get('id'))
                TreePath.objects.create(node_from=pnode, node_to=cnode, tree=tree, order=order)
                self.build_path(node, tree)
        else:
            pass

    def post(self, request):
        data = json.loads(request.body)
        for path in data:
            if not path.get('ignore'):
                name = path.get('name')
                tree = Tree.objects.get(name=name)
                TreePath.objects.filter(tree=tree).delete()
                self.build_path(path, tree)
        return Response({})


def path_to_json(path, tree):
    node = path.node_to
    result = {
        'Type': node.type,
        'Title': node.title,
    }
    children = [path_to_json(c, tree) for c in node.children.filter(tree=tree)]
    children = list(filter(None, children))
    if children:
        result['Children'] = children
        result.pop('Type')
    else:
        result['Children'] = None
    return result


class TreeView(APIView):

    def get(self, request, name):
        """ Get tree. """
        tree = get_object_or_404(Tree, name=name)
        root_path = tree.start_node.children.filter(tree=tree)
        dicts = []
        for n in root_path:
            result = path_to_json(n, tree)
            if result:
                dicts.append(result)
        return Response(dicts, safe=False)
