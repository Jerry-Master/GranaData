---
layout: post
title:  "GAN optimality proof"
author: jose
categories: [ GAN, Theory, unsupervised learning, Deep Learning ]
featured: false
hidden: false
comments: false
share: false
use_math: true
image: assets/images/GAN/gan-cat.png
time_read: 15
---

The so-called Generative Adversarial Networks have been with us since 2014, producing amazing results lately. Today I am bringing the proof of why they work. That is, a proof that states GANs are optimal in the limit when no parametric model is taken into account. But first, what is a GAN and what "amazing results" am I talking about?

<p class="text-center"><img class="" src="{{site.baseurl}}/assets/images/GAN/pix2pix.png" alt="simple" /></p>

The above example is about pix2pix which is a conditional adversarial network which gives style to your draft. You draw some sketch, tell some style and the network does the rest of the work. But there are other types of GANs, like style GAN which is very good at generating images of some given type, like the ones below, which are all artificial.

<p class="text-center"><img class="" src="{{site.baseurl}}/assets/images/GAN/stylegan.png" alt="simple" /></p>

GANs are also related to DALLE-2, the famous text-to-image model. Both are a special case of energy-based models, which is a more general framework. If you want to know more about it you can look at the [Yann Lecunn lectures about it](https://www.youtube.com/watch?v=tVwV14YkbYs). 

Let's dive into the details of the original GAN formulation. Typically, GANs are presented with the following diagram.

<p class="text-center"><img class="" src="{{site.baseurl}}/assets/images/GAN/gan-diagram.png" alt="simple" /></p>

But I prefer to understand models in the mathematical realm. There a GAN is a min-max problem. Concretely it is _this_ min-max problem:

<div>$$\min_G \max_D V(G,D)$$</div>

Where $D$ is the discriminator, it receives an image an outputs the probability of it being fake. $G$ is the generator, it receives some input vector $\textbf{z}$ and outputs a fake image, denoted by $\textbf{x}$. $V$ is a value function, which is defined as follows (each term will be explained in detail later):

<div>$$\mathbb{E}_{\textbf{x} \sim p_{data}}[\log(D(\textbf{x}))] + \mathbb{E}_{\textbf{z} \sim p_{\textbf{z}}}[\log(1-D(G(\textbf{z})))]$$</div>

How can we interpret those two terms? The first one is large when the discriminator is correctly identifying real images as real. The second one is large when the discriminator is correctly identifying the generator images as fake. Maximising this quantity yields a perfect discriminator. However, we want more than that, we want to fool the discriminator. That means creating a good generator. Fooling the discriminator means minimising the value function. Thus, we have the min-max problem as stated above. Intuitively the equilibrium of this problem will be reached when we have a perfect generator and the discriminator always outputs $\frac{1}{2}$ because the generated images are the same as the real ones. This is exactly what the optimality theorem from the original Ian Goodfellow's paper proves.

To understand the theorem, it is needed to give some formalism to the intuitive idea of perfect generator. What is a perfect generator? For us humans, it means that the images seem real. But mathematically, what does "real" means? It means that the probability distribution of the generated images and the probability distribution of the data are the same. Mathematically the images are random variables, whose observations are represented by a vector. If the real and fake vectors come from the same distribution, then, they can be considered to be the same. As an example, consider the probability distribution function (pdf) of images of Granada. From that pdf it is more probable to draw an image of the Alhambra than an image of the Eiffel tower. Also, random noise has zero probability on that pdf. So now, a good generator pdf should mimick that behaviour, giving high probability to images of Granada and low probability to everything else. 

In mathematical terms, the data pdf is denoted by $p_{data}(\textbf{x})$ and the generator pdf is $p_{g}(\textbf{x})$. So producing "real" images means that $p_{data}(\textbf{x}) = p_{g}(\textbf{x})$, $\forall \textbf{x}$. Now we can state the optimality theorem:

<div class="theorem"> The global minimum of $C(G) = \max_{D}V(G,D)$ is reached if and only if $p_{data}\equiv p_g$. Also, that minimum value is $-\log(4)$.</div>

Before proving it, let's analyse the consequences of it and what it is telling us. The main takeaway is that the solution to the min-max problem gives a perfect generator, which means that we can learn to reproduce any probability distribution. For simpler distributions this doesn't seem much, one can simply compute the histogram of a variable and use it as the estimated distribution. However, for images that is not possible. How can you compute the histogram of a set of images? There are no repeated values, we just have a bunch of different images with some similarities. So one can think of a GAN as a way of estimating the histogram of a set of images. But it is more than that, it also provides a way of drawing points (images) from that distribution. 

Another takeaway from the theorem is the optimal value of the value function. It may seem useless at first but it is a good indicator of whether or not the training is converging or not. Because in practice that optimal generator does not appears to us by divine revelation, an iterative method is typically used to find it. If you see that during training the model converges to a value different than $-\log(4) \approx -1.38$ then you can be certain that you have not solved the min-max problem.

So far so good but, the generator as presented above is just a deterministic function, where does the variability comes from? It is there on the formulas, you just need to give a closer look. When defining the value function the second term was computed from the distribution $p_{\textbf{z}}$, what is that? It is a prior distribution for the input of the generator, which means that the generator is a function transforming one distribution into another. Mathematically this means $\textbf{z} \sim p_{\textbf{z}} \Rightarrow G(\textbf{z}) \sim p_g$, a key fact that will be used in the proof. The inference process is now quite easy, just draw a point from $p_{\textbf{z}}$ and apply the generator to get a new image. In practice you can just put any value you want for $\textbf{z}$ since the prior is a noise prior, not anything in particular.

Finally, let's prove the theorem. The first step is to find the optimal discriminator given the generator. After that, that value is substituted into the formulas and everything is rearranged into something with an obvious lower bound. I will skip many computational details, you can just check them by hand or if they don't seem trivial to you, email me and I will write an appendix with more details. Let's go, first part:

<div class="prop"> If $G$ is fixed, the optimal $D$ is 
<div>$$ D^*(\textbf{x}) = \frac{p_{data}(\textbf{x})}{p_{data}(\textbf{x}) + p_{g}(\textbf{x})} $$</div>
</div>

<div class="proof"> We have $V(G,D)=\mathbb{E}_{\textbf{x} \sim p_{data}}[\log(D(\textbf{x}))] + \mathbb{E}_{\textbf{z} \sim p_{\textbf{z}}}[\log(1-D(G(\textbf{z})))]$, in order to combine both integrals we need them to depend on the same variable $\textbf{x}$. To do so we are going to exploit the fact that $\textbf{z} \sim p_{\textbf{z}} \Rightarrow G(\textbf{z}) \sim p_g$. This fact, in conjunction with the <a href="https://en.wikipedia.org/wiki/Radon%E2%80%93Nikodym_theorem">Radon-Nikodym Theorem</a> lets us conclude that $\mathbb{E}_{\textbf{z} \sim p_{\textbf{z}}}[\log(1-D(G(\textbf{z})))] = \mathbb{E}_{\textbf{x} \sim p_{g}}[\log(1-D(\textbf{x}))]$. Where $\textbf{x} = G(\textbf{z})$. Now, if we express the expectations in integral form we get the following
<div>$$ \int_{\textbf{x}} p_{data}(\textbf{x})\log(D(\textbf{x})) + p_g(\textbf{x})\log(1-D(\textbf{x})) d\textbf{x} $$</div>

The integrand is now bounded by a function that does not depend on $D$ and so that bound is the optimum. That bound is found by differentiating with respect to $D$ and equalling to zero. The integrand there is basically $a \log(D) + b\log(1-D)$, which has the maximum at $\frac{a}{a+b}$ if $a$, $b$ are constant with respect to $D$. I still have <a href="https://datascience.stackexchange.com/questions/113390/minor-error-in-ian-goodfellows-gan-optimality-proof">my doubts</a> with respect to that assumption, but assuming it we get that the maximum is reached when $D=\frac{p_{data}}{p_{data}+p_g}$ which ends the proof.
</div>

We now have found the optimal discrimator so we can now compute the value function for that optimal discriminator. If we call $C(G)=\max_{D}(V(D,G))$ the value of the value function for the optimal discriminator, we just want to find the minimum of $C(G)$ for any given generator. The "rearrangement" I mentioned above is the following

<div>$$ 
\begin{align*}
\max_D V(G,D) &=\mathbb{E}_{\textbf{x} \sim p_{data}}[\log(D^*(\textbf{x}))] + \mathbb{E}_{\textbf{x} \sim p_{g}}[1-\log(D^*(\textbf{x}))] \\
&= \mathbb{E}_{\textbf{x} \sim p_{data}}[\log(\frac{p_{data}(\textbf{x})}{p_{data}(\textbf{x}) + p_{g}(\textbf{x})})] + \mathbb{E}_{\textbf{x} \sim p_{g}}[\log(\frac{p_{g}(\textbf{x})}{p_{data}(\textbf{x}) + p_{g}(\textbf{x})}] \\
&= -\log(4) + KL(p_{data}||\frac{p_{data}+p_g}{2}) + KL(p_g||\frac{p_{data}+p_g}{2})\\
&= -\log(4) + 2 \cdot JSD(p_{data}||p_g)
\end{align*}
$$</div>

The acronyms means [Kullback-Leibler divergence](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence) and [Jensen-Shannon divergence](https://en.wikipedia.org/wiki/Jensen%E2%80%93Shannon_divergence). For a more in-depth explanation of this rearrangement you can look at this [great post](https://srome.github.io/An-Annotated-Proof-of-Generative-Adversarial-Networks-with-Implementation-Notes/).

We are almost finished, there is a property of the JSD that states it is a nonnegative value, being zero if and only if both distributions are equal. That property translates into $C(G) \ge -\log(4)$ with equality if and only if $p_{data} = p_g$ exactly as desired. Magic, isn't it?

Unfortunately, this theorem only states that the optimal generator exists but it doesn't give a way of finding it. In my [next post]({{site.baseurl}}/gan-convergence-proof){:target="_blank"} on the GANs series I will show the proof of convergence for the algorithm also proposed by Ian Goodfellow which proves that such generators can be found, at least in theory.
