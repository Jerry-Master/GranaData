---
layout: post
title:  "Modelling a padel match with Hidden Markov Models (Part 2)"
author: jose
categories: [ Hidden Markov Model ]
featured: false
hidden: false
comments: false
share: false
use_math: true
image: assets/images/HMM/padel_court.png
# time_read: 5
---

In my [last post]({{site.baseurl}}/HMM-padel){:target="_blank"} I explained the usefulness of Hidden Markov Models for predicting the outcome of a padel match with only a few observations. There I also showed how easy it was to implement everything in Python, but I left the most important part: the HMM itself. Today we are going to learn how to design a HMM to predict the result of a point. This is going to be an iterative process. The final model, as you will see, is a monstruosity. But step by step we are goint to build it succesfully. "Rome wasn't made in a day".

## Inspiration and design

Before diving into the details, let me explain how I tackled this problem. I think the creative process is worth mentioning. If you just want the details, you can skip this section. Before starting to code or thinking on my own for the solution of a problem I always research for similar problems that are already solved so that I can get some inspiration. In this case, it turned out that somebody had already designed a HMM for tenis. In [this article](https://ieeexplore.ieee.org/document/1423025){:target="_blank"}, they present a HMM for following the state of a tennis match. The observations in this article were poorly defined, but the hidden states wer very clear. I could get an idea of what I had to do by just looking at this image.

<p class="text-center"><img src="{{site.baseurl}}/assets/images/HMM/hmm-tenis.png" alt="tenisHMM" /></p>

This graph is just depicting visually the rules of tenis. In our case we just have to show the rules of padel with a similar graph. If you look carefully you will see that the white boxes represent hidden states with an obvious observation. For padel there will be more of them because apart from bouncing on the ground, the ball can bounce on the walls, which makes the graph more complex but the idea is the same. Another helpful diagram on the same article represented the same graph but organised in several subgraphs.

<p class="text-center"><img src="{{site.baseurl}}/assets/images/HMM/hmm-tenis2.png" alt="tenisHMM2" /></p>

What's interesting here is that those four subgraphs will be the same for padel. The high-level view of the process (top) is exactly the same. That's part of the job which is already done. We just have to change the internal representation between those four subgraphs and maintain the interconnections.

What about designing graphs? What is the software I used for that? You may say. Well, it is actually a pen and a lot of papers. No matter how well developed graph visualizations software are, drawing a simple graph by hand will always be faster than coding it. Of course, when the project keeps growing and the graphs becomes massive you will need those software tools which I will mention later. But at the beginning, just take a pen and start drawing. In the other sections I will present diagrams made with a computer because they are visually more pleasant and you will understand them better. Nevertheless, here is one of the graphs I painted by hand, in case you are curious.

<p class="text-center"><img src="{{site.baseurl}}/assets/images/HMM/hand.jpg" alt="hand-diagram" /></p>


## The hidden states' graph

For a HMM we need the transition and emission matrices. The transition matrix is going to be the adjacency matrix of the transitions graph. That graph is simply a representation of the rules of the game. I am going to distinguish two main parts in that rules. The rules for the serve and the rules for the normal game. The reason for creating two distinct graphs is because the effect of the ball going out or touching the net is different at the beginning.

### Serve

What happens when a player is on their serve? It can go in, it can go out or it can touch the net. And if it touches the net, it can then go in or out. Let's ignore when it goes in without touching the net for the moment. How would you represent the 1st serve? Like this?

<p class="text-center"><img src="{{site.baseurl}}/assets/images/HMM/first.png" alt="1st-serve" /></p>

Did you think about the init state? Remember, this model is a realistic one. In practice you don't know when is the point starting. Therefore, you need a special state for waiting until you have enough evidence that the match has begun. If you look closely, you will see that there is a self-loop on the init state. That is how we represent a waiting state in a HMM, by a self-loop. Now, let's pass to the 2nd-serve. How would you design it?

<p class="text-center"><img src="{{site.baseurl}}/assets/images/HMM/second.png" alt="2nd-serve" /></p>

Exactly the same as the first service. The simpler, the better. We are ignoring when the ball goes in and the game continues. We are just focusing on when the ball goes out or to the net. The rest of the details will be added later on. For now let's just focus on what we have. We have a graph with several nodes, each representing a state. What do we need? Consistent labels across the whole graph. One of the limitations of the HMM is that you have to fulfill the Markov property. Which means that the state representing going out after the 1st-serve is different than the state of going out after the 2nd-serve. So they need different names. In my case, I just added a suffix number when that happened. That way, going out in the first service is 'out1' and after the second is 'out2'. Another state that repeats a lot across the graph is the 'in' state. For that one adding a suffix number is not enough, so I added a more descriptive suffix. For instance, going in after touching the net in the first serve is 'in-net1'. This is a decision that could have been made of many ways, but I decided to make it like this. 

Okay, let's now talk about what happens when the ball actually goes in and the game continues. To keep it simple, let's focus on what happens before any player hits the ball. And let's call this the ace model. As the name states it, one of the things than can happen is an ace. What characterizes an ace? The fact that the ball touches the ground again before any player hitting it. Try to draw the scheme for the ace model. Keep in mind that before touching again the ground it can hit the walls. And also bare in mind that there are two types of walls. What are the connections among those states? Which combinations are valid and which not? Here is my solution for that problem, omitting the connections to the states Point-server and Point-receiver representing the end of the game.

<p class="text-center"><img src="{{site.baseurl}}/assets/images/HMM/ace.png" alt="ace" /></p>

Did you thought of the 'time-out' state? Again, this is a real model so it has to deal with real problems. And one of them is that you miss the observation that characterizes the end of the game. If that happens you can only know the game has finished by time. That's why you need a state to represent the end of the game by time. Later on when defining the emissions it will be made more clear why this state is needed. Most of the extra states are created so that when an observation is wrong, there is still a path in the graph to the end. Otherwise, the model will give an error and doesn't return anything. Observe also that there are two 'in' states. Can you imagine why? The state 'in1' is when the ball goes in on the first serve, and 'in2' on the second. Since we have to maintain the Markov property, those two states are different although they have the same emissions and are identical to us.

Before going to the next block, which is when a player hits the ball and the game actually starts, let me explain how I made this pictures and how you can code graphs on Python. With the library {% ihighlight python %}networkx{% endihighlight %} you can do many thing on graphs, it has implemented almost every algorithm that exists related to graphs. In this project we only use it to define the graphs. The syntax is pretty straighforward, you define a {% ihighlight python %}DiGraph{% endihighlight %} which stands for directed graph, and add nodes and edges with the functions {% ihighlight python %}add_nodes_from{% endihighlight %} and {% ihighlight python %}add_edges_from{% endihighlight %}. After that, you can save the model in {% ihighlight python %}gml{% endihighlight %} format and open it with [Gephi](https://gephi.org/){:target="_blank"}. That's it. Here is the code for the three models presented above.

```python
folder_path = 'graphs/'

""" First serve model """
first = nx.DiGraph()
first.add_nodes_from([
    ("init", {"hidden": True}),
    ("1st-serve", {"hidden": True}),
    ("net1", {"hidden": True}),
    ("out1", {"hidden": True}),
    ("in-net1", {"hidden": True}),
])
first.add_edges_from([
    ("init", "1st-serve"), ("init", "init"),
    ("1st-serve","net1"), ("1st-serve","out1"),
    ("net1","in-net1"), ("net1","out1"),
    ("in-net1","1st-serve")
])
nx.write_gml(first, folder_path + 'first.gml')

""" Second serve model """
second = nx.DiGraph()
second.add_nodes_from([
    ("2nd-serve", {"hidden": True}),
    ("net2", {"hidden": True}),
    ("out2", {"hidden": True}),
    ("in-net2", {"hidden": True}),
])
second.add_edges_from([
    ("2nd-serve","net2"), ("2nd-serve","out2"),
    ("net2","in-net2"), ("net2","out2"),
    ("in-net2","2nd-serve")
])
nx.write_gml(second, folder_path + 'second.gml')

""" Ace model """
ace = nx.DiGraph()
ace.add_nodes_from([
    ("in1", {"hidden": True}),
    ("in2", {"hidden": True}),
    ("time-out", {"hidden": True}),
    ("ground", {"hidden": True}),
    ("wall-outer1", {"hidden": True}),
    ("wall-outer2", {"hidden": True}),
    ("wall-inner1", {"hidden": True}),
    ("wall-inner2", {"hidden": True}),
])
ace.add_edges_from([
    ("in1", "time-out"), ("in1", "ground"), ("in1", "wall-outer1"), ("in1", "wall-inner1"),
    ("in2", "time-out"), ("in2", "ground"), ("in2", "wall-outer1"), ("in2", "wall-inner2"),
    ("wall-outer1", "time-out"), ("wall-outer1", "ground"), ("wall-outer1", "wall-outer2"),
    ("wall-outer2", "time-out"), ("wall-outer2", "ground"),
])
nx.write_gml(ace, folder_path + "ace.gml")
```

[Gephi](https://gephi.org/){:target="_blank"} has some handy features that make posible visualize big graphs. Concretely, you can use the Force Atlas distribution to reorder the nodes by simulating forces proportional to the number of edges they have. It has many parameters you can try, but I normally just click on execute and wait a few seconds for convergence.

<p class="text-center"><img src="{{site.baseurl}}/assets/images/HMM/atlas.png" alt="Force Atlas" /></p>

Then, on the previsualization tab, you can create the diagrams I showed you. It has many options, like curved edges. I don't use that feature for this post because for complex graphs it can be messy. But for some graphs I think is prettier with curvy edges. Other things to adapt are the font size and the size of the arrows. With a bit of practice you can create nice figures quite fast.

<p class="text-center"><img src="{{site.baseurl}}/assets/images/HMM/previs.png" alt="Previsualization" /></p>



### Rally

### Interconnections

## The observations' graph

## Implementing the graphs on NetworkX

