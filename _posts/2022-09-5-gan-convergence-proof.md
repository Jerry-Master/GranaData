---
layout: post
title:  "GAN convergence proof"
author: jose
categories: [ GAN, Theory, unsupervised learning ]
featured: false
hidden: false
comments: false
share: false
use_math: true
image: assets/images/GAN/gan-cat2.png
time_read: 16
---

In my [previous post]({{site.baseurl}}/gan_optimality_proof){:target="_blank"} about GANs I explained the mathematical proof of why GANs work. The theorem stated that the real data distribution was mimicked by the generator at the optimum of the cost function, although it didn't say how to find such optimum. In this post I will specify how to find such optimum and prove that the algorithm provided works. Keep in mind that this algorithm is the original proposed by Ian Goodfellow, several improvements have been made since then. At the end I will describe some of the faults of this algorithm and various changes that have been tried since it was published.

The algorithm can be described in pseudocode as follows:

<pre id="gan" class="pseudocode" style="display:hidden;">
    % This quicksort algorithm is extracted from Chapter 7, Introduction to Algorithms (3rd edition)
    \begin{algorithm}
    \caption{GAN convergence algorithm}
    \begin{algorithmic}
    \FOR{number of training iterations}
        \FOR{\$k\$ steps}
            \STATE Sample minibatch of \$m\$ noise samples \( \{ \)\$z\$\( ^{(1)},\dots,\)\$z\$\(^{(m)}\} \) from noise prior \$p\_z(z)\$.
            \STATE Sample minibatch of \$m\$ examples \( \{ \)\$x\$\( ^{(1)},\dots,\)\$x\$\(^{(m)}\} \) from data generating distribution \$p\_\{data\}(z)\$.
            \STATE Update the discriminator by ascending its stochastic gradient:
            $\nabla_{\theta_d}\frac{1}{m} \sum_{i=1}^{m}[log(D (x^{(i)})) + log(1-D(G(z^{(i)})))$
            \normalsize
        \ENDFOR
        \STATE Sample minibatch of \$m\$ noise samples \( \{ \)\$z\$\( ^{(1)},\dots,\)\$z\$\(^{(m)}\} \) from noise prior \$p\_z(z)\$.
        \STATE Update the generator by descending its stochastic gradient: $\nabla_{\theta_g}\frac{1}{m} \sum_{i=1}^{m}log(1-D(G(z^{(i)})))$
    \ENDFOR
    \end{algorithmic}
    \end{algorithm}
</pre>

Let's disect the algorithm piece by piece. Recall which function we were trying to optimize: 

<div>$$V(G,D) = \mathbb{E}_{\textbf{x} \sim p_{data}}[\log(D(\textbf{x}))] + \mathbb{E}_{\textbf{z} \sim p_{\textbf{z}}}[\log(1-D(G(\textbf{z})))]$$</div>

We wanted the maximum with respect to the discriminator and then the minimum with respect to the generator: 

<div>$$\min_G \max_D V(G,D)$$</div>

If you look at the pseudocode we are doing just that. We first apply gradient ascent on the discriminator and then gradient descent on the generator. You may have noticed that the formulas in the pseudocode are different from what I showed you in the previous post. That is because we are approximating the expectation using a Monte Carlo method. To compute the expected value of a variable you need to compute an integral which in this case, and many others, is intractable. For that reason the expectation is approximated by the mean:

<div>$$\mathbb{E}_{\textbf{x} \sim p}[f(\textbf{x})] \approx \frac{1}{m}\sum_{i=1}^{m} f(\textbf{x}^{(i)})$$</div>

where the $\textbf{x}^{(i)}$ are sampled from the distribution $p$. If you go to the pseudocode you will see that we sample the $\textbf{z}$ from the prior noise and the $\textbf{x}$ from the real data. You may have also noticed that there is one term missing when applying gradient descent for the generator. The reason for that is the first summand in the formula does not depend on the generator, therefore the gradient of that term is zero.

As you can see the algorithm itself is quite intuitive. For maximization apply gradient ascent and for minimization you apply gradient descent. That's it. But being simple and intuitive is not enough for an algorithm to be correct, there needs to be a proof of their correctness. In this case there needs to be a proof of convergence and optimality. And like every theorem, that proof is going to come with some hypothesis. 

The first hypothesis is that $D$ and $G$ have enough capacity. This means that whatever model you use for them can reach the optimum. That seems a pretty reasonable hypothesis, but in practice you never know how much complexity is enough complexity. 

The second hypothesis is that $D$ can reach the optimum at each step given $G$. This is basically saying that the parameter $k$ used is sufficiently large, and that the learning rate is sufficiently small so that other theorems of gradient descent convergence hold. That optimum is going to be called $D^*_G$. This hypothesis is less important than the next one, and in practice reaching the optimal discriminator at any step is a problem that I will describe later on in this post.

The last hypothesis is that at each step the criterion $C(G)=\min_D(V(G,D))$ improves. Which is basically saying that gradient descent is working on the generator. Formally, the theorem can be expressed like follows

<div class="theorem"> 
If $G$ and $D$ have enough capacity, and at each step of Algorithm 1, the discriminator is allowed to reach its optimum given $G$, and $p_g$ is updated so as to improve the criterion
<div>$$\mathbb{E}_{\textbf{x} \sim p_{data}}[\log(D^*_G(\textbf{x}))] + \mathbb{E}_{\textbf{x} \sim p_g}[\log(1-D^*_G(\textbf{x}))]$$</div>
then $p_g$ converges to $p_{data}$.
</div>

The proof consists of two main steps: proving the cost function is convex with respect to the generator and proving the gradient descent at the optimal $D$ given $G$ converges to the same as the gradient descent for the global optimal $D$. This way we don't need to know the real optimal discriminator, just the one that is optimum for each generator. The proof for convexity is more technical and I will explain it later. Let's go with showing we only need a suboptimal discriminator.

As everything in math, we start with definitions and notation that will made the rest of the proof easier to follow. The first change is for the value function, let's call $U(p_g,D)=V(G,D)$ to the value function, changing the dependency to the generated distribution instead of the model. This is to highlight that we are working with ideal models in the function space not in the parametric space. Let's call $U(p_g) = \sup_DU(p_g,D)$ the value function for the optimal discriminator. Since we are working in the function space the supremum is used instead of the maximum. Now the problem is to find $\inf_{p_g}U(p_g)$. 

Assuming $U(p_g,D)$ is convex for every $D$ there is [a theorem](https://math.stackexchange.com/questions/3363996/convexity-of-supremum-of-convex-functions){:target="_blank"} saying that $U(p_g)$ is also convex. Now, the key of the proof is showing that any [subgradient](https://en.wikipedia.org/wiki/Subgradient_method){:target="_blank"} of $U(p_g,D^\*_G)$ is also a subgradient of $U(p_g)$ when $D^\*_G=\text{argsup}_D U(p_g,D)$. This way gradient descent on $U(p_g,D^\*_G)$ converges to the same value as gradient descent on $U(p_g)$, since that function is convex and the global optimum exists, that optimum is found. Now, the details.

Mathematically, the argument of the subgradients can be expressed as follows:

<div>$$\partial U(p_g, \text{argsup}_D U(p_g,D)) \subseteq \partial \sup_D U(p_g,D)$$</div>

Being $\partial f$ the [set of subgradients](https://en.wikipedia.org/wiki/Subderivative#The_subgradient){:target="_blank"} of $f$. The proof of that is a matter of using correctly the definitions. We have $U(p_g,D^\*_G)=U(p_g)$. If $g\in \partial U(p_g,D^\*_G)$, then by definition we have $U(p_g',D^\*_G) \ge U(p_g,D^\*_G) + g^T (p_g'-p_g)$ for every other distribution $p_g'$, being the last term the scalar product of functions. By definition of supremum we have $U(p_g') \ge U(p_g',D^\*_G)$. Joining everything we obtain 
<div>$$U(p_g') \ge U(p_g',D^*_G) \ge U(p_g,D^*_G) + g^T (p_g'-p_g) = U(p_g) + g^T (p_g'-p_g)$$</div>
And therefore $U(p_g')\ge U(p_g) + g^T (p_g'-p_g)$ which shows that $g\in \partial U(p_g)$. In Algorithm 1 we don't use subgradients, and that is because if we assume the cost function is differentiable, then the only subgradient is the gradient. And we always use cost functions that are differentiable. For that reason, this part of the proof can also be expressed like this

<div>$$\nabla V(G,D^*_G) = \nabla C(G)$$</div>

which gives a way of optimizing $C(G)=\sup_D V(G,D)$ without needing to know the function itself. Quite a nice property of convex functions. Let's now prove that the function is in fact convex. What is the definition of convex in this context? It simply means that 
<div>$$U(tp_g'+(1-t)p_g,D) \ge tU(p_g',D)+(1-t)U(p_g,D)$$</div>

which, after removing at both sides the terms that doesn't depend on $p_g$, translates to 

<div>$$\mathbb{E}_{\textbf{x} \sim tp_g'+(1-t)p_g}[\log(1-D(\textbf{x}))] \ge t\mathbb{E}_{\textbf{x}\sim p_g'}[\log(1-D(\textbf{x}))] + (1-t)\mathbb{E}_{\textbf{x}\sim p_g}[\log(1-D(\textbf{x}))]$$</div>

To prove that, we are going to prove an even stronger statement, which is

<div>$$\mathbb{E}_{\textbf{x} \sim tp_g'+(1-t)p_g} \equiv t\mathbb{E}_{\textbf{x}\sim p_g'} + (1-t)\mathbb{E}_{\textbf{x}\sim p_g}$$</div>

And this is fairly easy to prove, we just need to recall the linearity of integrals

<div>$$\mathbb{E}_{\textbf{x} \sim tp_g'+(1-t)p_g} [f] =\int (tp_g'+(1-t)p_g)f = t\int p_g' f + (1-t) \int p_g f  = t\mathbb{E}_{\textbf{x}\sim p_g'}[f] + (1-t)\mathbb{E}_{\textbf{x}\sim p_g}[f]$$</div>

which finally proves the convexity of $U(p_g,D)$ with respect to $p_g$. Let's start now with the faults of this proof and why it doesn't hold on practice. The main reason it doesn't hold in practice is the convexity of the cost function. Whenever we change the set of all distributions $p_g$ by the set of parametrized generators $G$ the corresponding cost function becomes non-convex. This is so because we are reducing the space from an infinite convex space, to a finite space. Now $tG'+(1-t)G$ may not be any valid generator, and so the set of reproducible distributions could be non-convex. In addition, it is well-known that using deep neural networks creates non-convex costs functions. That limits the possibility of finding the global optimum by only using gradient descent.

There is another problem with this proof. It requires that we find a perfect discriminator at each step, and after it we apply gradient descent on the generator. The reason why that doesn't work is mainly numerical. A perfect discriminator is going to produce gradients close to zero. When propagating the gradient it results on the generator not training at all. In practice, many articles limit the ability of learning of the discriminator so that the gradient is non-zero. One technique for doing so is using a smaller learning rate for the discriminator. This way the discriminator is learning at a slower pace than the generator. 

However, there are no results either proving or disproving that a neural network is not well-suited for this task. Many researchers have achieved decent results when training GANs. I wouldn't even be writing this posts at all if GANs were a loss of time, which they aren't. In practice they can work very well, but bare in mind that they are difficult to train. There is no theorem guaranteeing that Algorithm 1 works always. And you may probably need to use a modification of Algorithm 1 to make it work. But all in all, you can consider real GANs as approximations of an ideal GAN that always converge. It's better than nothing.


<script>
    pseudocode.renderElement(document.getElementById("gan"));
</script>
<script>
    pseudocode.renderClass("pseudocode");
</script>