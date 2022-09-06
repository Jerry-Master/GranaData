---
layout: post
title:  "Modelling a padel match with Hidden Markov Models"
author: jose
categories: [ Hidden Markov Model ]
featured: false
hidden: false
comments: false
share: false
use_math: true
image: assets/images/HMM/padel_court.png
#time_read: 16
---

Imagine you are at a padel match. You watch the ball go from one side to the other, hit the wall, hit the ground, the net, and after some time someone wins the point. In your head you are following the state of the match until the end to know the winner. Imagine now that you were distracted by a fly and lost concentration on the players. You don't know what has happened when you were distracted but you managed to watch the last part of the point and so you still know who is the winner. How can we replicate this situation with a model? Which is the correct model to manage situations where you can lose track in the middle but by looking the last part you know the result? The property of only needing to know the last part to know the result is called the Markov property. So a suitable model for this task is a Hidden Markov Model.

In this series I will describe how to properly design a Hidden Markov Model (HMM from now on) to keep track of the state of a padel match. I will also provide functional python code that you could play with. And as extra material I will talk about unit testing and how to use unit tests to incrementally build a model like this one. Let's begin.

