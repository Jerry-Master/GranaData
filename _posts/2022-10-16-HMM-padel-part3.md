---
layout: post
title:  "Modelling a padel match with Hidden Markov Models (Part 3)"
author: jose
categories: [ Hidden Markov Model ]
featured: false
hidden: false
comments: false
share: false
use_math: false
image: assets/images/HMM/padel_court.png
time_read: 6
---

In [part I]({{site.baseurl}}/HMM-padel){:target="_blank"} and [part II]({{site.baseurl}}/HMM-padel-part2){:target="_blank"} of this series I have talked about what is a Hidden Markov Model, why it is useful for modelling a padel match, and how to design it properly. Today the topic is about testing the model. Testing a machine learning model is the basis for deploying it. Here I will be explaining how to test in python and guide you through our HMM example. 

## PyTest

Testing in python can be done with several libraries. One of the most popular ones is {% ihighlight python %}pytest{% endihighlight %}. There are many good tutorials out there about how to use it, like [this one](https://towardsdatascience.com/getting-started-unit-testing-with-pytest-9cba6d366d61){:target="_blank"}. And if you have a project on your hands and have specific needs, you can always go and have a look at [their documentation](https://docs.pytest.org/en/6.2.x/contents.html){:target="_blank"}. For this post I will pass very briefly on the funcionalities that we need for testing the HMM.

In pytest you have files that contain the word 'test' on it. Those files contain functions that also have the string 'test' in their names. And those functions must have code that yields {% ihighlight python %}True{% endihighlight %} of {% ihighlight python %}False{% endihighlight %} depending on whether they pass the test. To run the tests you just execute {% ihighlight python %}pytest{% endihighlight %} on the command line and the library does the rest of the job for you. This is the big picture, let's define now what are going to be our tests. 

Our tests are going to have a sequence of observations as input and we are going to check for the result of the match. That is the final goal of the HMM. The difference is that here we are going to deal with simple scenarios where we know for sure the result. That way we can check that the HMM is at least well implemented. We cannot check if the design is going to work in a real-world scenario, but we can check that it works in ideal scenarios. If your model breaks in an environment where you control the input, then something is clearly wrong in the code. However, if it breaks in production it may be that the model hypothesis about the world are wrong. That's why you need these tests, to detect bugs prior to analysing the correctness of the model itself.

Once the tests are designed, it's time to implement them. For that, {% ihighlight python %}pytest{% endihighlight %} comes with two main features that make the process easier. 

### Parameterization

In {% ihighlight python %}pytest{% endihighlight %} you can parameterize the input. When testing a function, several input-output pairs are used to ensure that the function produces the desired result. Using a different file for each input-output pair would be an inconvenience. Instead, you can specify several input-output pairs for a given test. Consider the following test where we are interested in knowing if the HMM correctly detects an ace:

```python
def test_ace(sequence, indexers, hmm, hidden_states):
    indexer_hidden, indexer_obs = indexers
    sequences = [[indexer_obs[obs] for obs in sequence]]
    decoded_seq = hmm.decode(sequences)
    decoded_seq = [hidden_states[idx] for idx in decoded_seq[0]]
    assert('Point-server' in decoded_seq)
```

The parameter sequence is a list of observations that corresponds to an ace. Without parameterization we would have to specify a different test function for each sequence that represents an ace. With parameterization we can reuse the function. In {% ihighlight python %}pytest{% endihighlight %} that features is implemented with decorators. For those of you who don't know python enough, a decorator is basically a function of functions. Here it takes the test function as input and creates a parameterized test function as output. Syntactically it is coded like this:

```python
@pytest.mark.parametrize("sequence", [
    ### Ace examples
    ])
def test_ace(sequence, indexers, hmm, hidden_states):
    indexer_hidden, indexer_obs = indexers
    sequences = [[indexer_obs[obs] for obs in sequence]]
    decoded_seq = hmm.decode(sequences)
    decoded_seq = [hidden_states[idx] for idx in decoded_seq[0]]
    assert('Point-server' in decoded_seq)
```

You only have to add the decorator on top of the function. If you recall the problem at hands, which sequences could possibly represent an ace? Let's see some examples:

```python
### ace in first service ###
['player-hit', *['flying'] * 10, 'bounce-ground-receiver', *['flying'] * 10, 
    'bounce-ground-receiver', *['flying'] * 100, 'end'],
    # Bounce on wall
['player-hit', *['flying'] * 10, 'bounce-ground-receiver', *['flying'] * 10,
    'bounce-wall-outer', *['flying'] * 10, 'end'], 
    # Bounce on wall twice
['player-hit', *['flying'] * 10, 'bounce-ground-receiver', *['flying'] * 10,
    'bounce-wall-outer', *['flying'] * 10, 'bounce-wall-outer', *['flying'] * 10, 'end'],

### ace in second service ###
    # Bounce on wall
['player-hit', *['flying'] * 10, 'bounce-ground-server', *['flying'] * 10, 
    'player-hit', *['flying'] * 10, 'bounce-ground-receiver', *['flying'] * 10, 
    'bounce-wall-outer', *['flying'] * 10, 'end'],
    # Bounce on wall twice
['player-hit', *['flying'] * 10, 'bounce-ground-server', *['flying'] * 10, 
    'player-hit', *['flying'] * 10, 'bounce-ground-receiver', *['flying'] * 10, 
    'bounce-wall-outer', *['flying'] * 10, 'bounce-wall-outer', *['flying'] * 10, 'end']
```

Basically, whenever there are two consecutive bounces on the other side after the first player has hit the ball we have an ace. When an ace happens the server wins, therefore we have to check that the last hidden state correspond to the server winning. If that doesn't happens, then our HMM isn't working. Passing this test doesn't prove that the HMM works, but by adding more and more tests we at least know that our model is robust to all those cases. 

### Fixtures

Have you wondered how do you pass parameters to a test? In the previous section I talk about parameterizing with a decorator. But what about the rest of the parameters? Not every parameter is part of the input. There are parameters that are part of the function itself. For instance, the parameter {% ihighlight python %}hmm{% endihighlight %}. How does {% ihighlight python %}pytest{% endihighlight %} know where to look for that object? 

At the beginning I said that you just have to run {% ihighlight python %}pytest{% endihighlight %} in the command line. You don't specify parameters to the internal test functions directly. Instead, you use fixtures. A fixture is another decorator provided by {% ihighlight python %}pytest{% endihighlight %}. In this case, you decorate a function that returns the parameter you want to use later on. Let's look at an example by specifying the fixture for the {% ihighlight python %}hmm{% endihighlight %} object. Suppose that you have a function in your code (not your test, your real code) that initialized the {% ihighlight python %}hmm{% endihighlight %} and returns it. Then, you would convert that function to a fixture this way:

```python
@pytest.fixture()
def hmm():
    return read_hmm()
```

That's everything you have to do in order for every other function to know where to look for the {% ihighlight python %}hmm{% endihighlight %} object. The same would be needed for the {% ihighlight python %}indexers{% endihighlight %} and {% ihighlight python %}hidden_states{% endihighlight %} that in my case are just dictionaries to convert from strings of states to the internal identifiers that the HMM uses. 

## Noisy tests

To end this post I'll show you some concrete tests I designed for my HMM. They are a bit different than the rest of the tests. When evaluating the HMM I said that we give ideal scenarios as input to the tests. But it is possible to give noisy scenarios too, if you control the noise. There are no rules for writing tests, they just serve to check that your code does what you want it to do. And if I want my HMM to be robust to noise, I can test for it. 

When I talk about noise in this problem it would be missing some observation or having repeated observations for the same hidden state. We designed our model so that it would work even on those cases. So if I provide a series of noisy observations, it must predict correctly the result. For example, in the following code there is the test for two cases where the server fails on the second service. However, the first hit is repeated and some bounces are repeated too. This series of observations doesn't correspond to an ideal one, but the model should correctly predict the result.

```python
@pytest.mark.parametrize("sequence", [
    ### Fail in second service ###
    # Bounce in and then on inner wall
    ['player-hit','flying', 'flying', 'player-hit', *['flying'] * 13, 
     'bounce-ground-server', 'flying', 'bounce-ground-server', *['flying'] * 9, 
     'player-hit', *['flying'] * 10, 'bounce-ground-receiver', *['flying'] * 4, 
     'bounce-wall-inner', *['flying'] * 10, 'end'],
     # Bounce out
    ['player-hit', *['flying'] * 15, 'bounce-ground-server', *['flying'] * 10,
     'player-hit', 'player-hit', *['flying'] * 12, 'bounce-ground-server', *['flying'] * 10, 'end']
])
def test_fail_noise(sequence, indexers, hmm, hidden_states):
    indexer_hidden, indexer_obs = indexers
    sequences = [[indexer_obs[obs] for obs in sequence]]
    decoded_seq = hmm.decode(sequences)
    decoded_seq = [hidden_states[idx] for idx in decoded_seq[0]]
    assert('Point-receiver' in decoded_seq)
```

You can also have tests that don't pass on purpose. I call this one 'impossible_noise_test':

```python
""" Test designed to make the model fail """
@pytest.mark.parametrize("sequence", [
    [*['flying'] * 3, 'bounce-ground-server', *['flying'] * 3,
    'bounce-ground-server', *['flying'] * 3,'player-hit', # Bounces in the ground badly detected as player-hit
    *['flying'] * 3, 'bounce-ground-server', # Badly detected bounce
    'bounce-ground-receiver', *['flying'] * 5, 'player-hit', *['flying'] * 4, # Well detected serve
    'bounce-ground-server', 'bounce-ground-server', 'bounce-ground-server', # Same bounce 
    *['flying'] * 5, 'player-hit', # Well detected response
    *['player-hit', *['flying'] * 5]*10, # Normal rally (now the ball is for receiver)
     'bounce-ground-receiver', 'end'] # It goes to net and out
])
def test_impossible_noise(sequence, indexers, hmm, hidden_states):
    indexer_hidden, indexer_obs = indexers
    sequences = [[indexer_obs[obs] for obs in sequence]]
    decoded_seq = hmm.decode(sequences)
    decoded_seq = [hidden_states[idx] for idx in decoded_seq[0]]
    assert("Point-server" in decoded_seq)
```

This type of test allows you to know the limits of the model. There must be a limit, and if you don't manage to create a test that fails, that is also and indicator that something is wrong. Maybe you are not creative enough for the cases, or you have some bug that makes all the test pass (that has happened to me). So it is also a good idea to have a test that fails, just in case.

## Conclusion

With this post the Hidden Markov Model for Padel Modelling series comes to an end. We have learned everything to deploy a HMM. From the theory behind the model, till testing the model extensively. Those are the steps to put any machine learning model into production. Learning the basics, designing the model and testing the model. The only thing left is to create a pipeline and integrate it into the final product, but that is a topic for another day. I hope you liked the process as much as I did. See you on my next series.