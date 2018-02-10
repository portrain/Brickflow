import pathlib
import networkx as nx
import pygraphviz as pgv
from ruamel.yaml import YAML


class Step:
    def __init__(self, start, end, bag, next):
        self.start = start
        self.end = end
        self.bag = bag
        self.next = next

    @classmethod
    def from_dict(cls, item):
        return cls(start=item['start'],
                   end=item['end'],
                   bag=item['bag'],
                   next=item['next'])

    @property
    def meta_dict(self):
        return {
            'end': self.end,
            'bag': self.bag,
            'next': self.next
        }

    @property
    def label(self):
        return f'From: {self.start} \nTo: {self.end} \nBag: {self.bag}'


class Plan:
    def __init__(self):
        self._title = ''
        self._graph = None
        self._bag_colors = []
        self._shapes = {}

    @property
    def is_loaded(self):
        return self._graph is not None

    def load(self, path):
        yaml = YAML(typ='safe')
        plan_dict = yaml.load(pathlib.Path(path))

        self._title = plan_dict['title']
        self._bag_colors = plan_dict['bagcolors']
        self._shapes = plan_dict['shapes']

        self._graph = nx.DiGraph()
        for group in plan_dict['groups']:
            new_step = Step.from_dict(group)

            # existing nodes are overwritten with new attributes
            if new_step.start in self._graph.nodes:
                self._graph.nodes[new_step.start]['label'] = new_step.label
                self._graph.nodes[new_step.start]['color'] = self._bag_colors[new_step.bag - 1]
                for key, value in self._shapes['integration'].items():
                    self._graph.nodes[new_step.start][key] = value
            else:
                self._graph.add_node(new_step.start,
                                     label=new_step.label,
                                     color=self._bag_colors[new_step.bag - 1],
                                     **{k: v for k, v in self._shapes['independent'].items()})

            # 'next' nodes that don't exist yet are created with blank attributes
            if new_step.next not in self._graph.nodes:
                self._graph.add_node(new_step.next)

            # create the edge pointing from the new node to the next node
            self._graph.add_edge(new_step.start, new_step.next)

    def validate(self):
        if self.is_loaded:
            return nx.is_directed_acyclic_graph(self._graph)

    def to_topological_dict(self):
        if self.validate():
            result = []
            for node in nx.lexicographical_topological_sort(self._graph, key=lambda x: str(x)):
                next_nodes = list(self._graph.successors(node))
                result.append({node: next_nodes[0] if len(next_nodes) > 0 else None})
            return result

    def plot(self, path, *, layout='neato', format=None):
        if self.validate():
            agraph = nx.nx_agraph.to_agraph(self._graph)

            agraph.graph_attr['label'] = self._title
            agraph.graph_attr['labelloc'] = 't'
            agraph.graph_attr['overlap'] = 'scale'
            agraph.graph_attr['sep'] = '+20,20'
            agraph.graph_attr['pad'] = '1.0'

            agraph.node_attr['shape'] = 'folder'
            agraph.node_attr['margin'] = '0.3,0.3'
            agraph.node_attr['penwidth'] = '3'

            agraph.edge_attr['penwidth'] = '2'

            plot_graph = pgv.AGraph(str(agraph), strict=False, directed=True)
            plot_graph.draw(path=path, format=format, prog=layout)
