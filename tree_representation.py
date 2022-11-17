import collections
import plotly.graph_objects as go
from igraph import Graph, EdgeSeq
from Tree import TreeNode


def levelOrder(root: TreeNode, k):
    if not root:
        return []
    q = collections.deque([root])
    res = []
    level = 0
    while q:
        temp = []
        size = len(q)
        for i in range(size):
            node = q.popleft()
            if node == None:
                node = TreeNode()
                node.set_score(10000)
            if node.get_value() == str(10000):
                temp.append('')
            else:
                temp.append(node.get_value())
            children = node.get_children()
            for child in children:
                if level < k:
                    q.append(child)
        level += 1
        res.extend(temp)
    return res


def tree_rep(root: TreeNode, k):

    v_label = levelOrder(root, k)
    nr_vertices = len(v_label)

    G = Graph.Tree(nr_vertices, 7) # 2 stands for children number
    lay = G.layout_reingold_tilford(mode="in", root={0})

    position = {k: lay[k] for k in range(nr_vertices)}
    Y = [lay[k][1] for k in range(nr_vertices)]
    M = max(Y)

    es = EdgeSeq(G) # sequence of edges
    E = [e.tuple for e in G.es] # list of edges

    L = len(position)
    Xn = [position[k][0] for k in range(L)]
    Yn = [2*M-position[k][1] for k in range(L)]
    Xe = []
    Ye = []
    for edge in E:
        Xe+=[position[edge[0]][0],position[edge[1]][0], None]
        Ye+=[2*M-position[edge[0]][1],2*M-position[edge[1]][1], None]

    labels = v_label
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=Xe,
                       y=Ye,
                       mode='lines',
                       line=dict(color='rgb(210,210,210)', width=1),
                       hoverinfo='none'
                       ))
    fig.add_trace(go.Scatter(x=Xn,
                      y=Yn,
                      mode='markers',
                      name='bla',
                      marker=dict(symbol='circle-dot',
                                    size=18,
                                    color='#6175c1',    #'#DB4551',
                                    line=dict(color='rgb(50,50,50)', width=1)
                                    ),
                      text=labels,
                      hoverinfo='text',
                      opacity=0.8
                      ))

    axis = dict(showline=False,  # hide axis line, grid, ticklabels and  title
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                )

    fig.update_layout(title='Tree with Reingold-Tilford Layout',
                      annotations=make_annotations(labels, position, M, position, v_label),
                      font_size=12,
                      showlegend=False,
                      xaxis=axis,
                      yaxis=axis,
                      margin=dict(l=40, r=40, b=85, t=100),
                      hovermode='closest',
                      plot_bgcolor='rgb(248,248,248)'
                      )
    fig.show()


def make_annotations(labels, position, M,  pos, text, font_size=10, font_color='rgb(250,250,250)'):
    L=len(pos)
    if len(text)!=L:
        raise ValueError('The lists pos and text must have the same len')
    annotations = []
    for k in range(L):
        annotations.append(
            dict(
                text=labels[k], # or replace labels with a different list for the text within the circle
                x=pos[k][0], y=2*M-position[k][1],
                xref='x1', yref='y1',
                font=dict(color=font_color, size=font_size),
                showarrow=False)
        )
    return annotations

