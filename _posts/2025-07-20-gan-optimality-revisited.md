---
layout: post
title:  "GAN optimality proof revisited"
author: jose
categories: [ GAN, Theory, unsupervised learning, Deep Learning ]
featured: false
hidden: false
comments: false
share: false
use_math: true
image: assets/images/GAN/gan-cat3.png
time_read: 4
---

Three years have passed since I published two posts related to the original formulation of the Generative Adversarial Networks (GANs). Three very crazy years in which the state of the art (SOTA) of generative models has surpassed any kind of expectation. Specially in video models that have now passed Tik-Tok quality by of large, they are still below TV quality and, of course, below cinema quality, but it is a lot more than what I predicted back in the days. The new SOTA models are all based on a different formulation from GANs, they use diffusion models. I am not going to write about diffusion models since that topic is already well covered in this [post](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/){:target="_blank"} together with a continuation for [video diffusion models](https://lilianweng.github.io/posts/2024-04-12-diffusion-video/){:target="_blank"}. And for those of you who want to have deeper mathematical intuition there is [this wonderful paper](https://arxiv.org/abs/2208.11970){:target="_blank"} with hundreds of formulas and derivations that gets as deep as you can get into the foundations of diffusion models. However, this post is again about GANs, more concretely, about the optimality proof. 

Three years ago I was not convinced by Goodfellow's proof of this theorem:

<div class="theorem"> The global minimum of $C(G) = \max_{D}V(G,D)$ is reached if and only if $p_{data}\equiv p_g$. Also, that minimum value is $-\log(4)$.</div>

Just to recap, this theorem is saying that the solution of the min-max problem is reached when we have a perfect generator. And the step that bothered me was in an intermediate proposition:

<div class="prop"> If $G$ is fixed, the optimal $D$ is 
<div>$$ D^*(\textbf{x}) = \frac{p_{data}(\textbf{x})}{p_{data}(\textbf{x}) + p_{g}(\textbf{x})} $$</div>
</div>

This proposition computed the optimal discriminator given the generator. And in the limit it results in a stupid discriminator who always predicts 50-50 probability of being real and fake. I already showed [my doubts]({{ site.baseurl }}/gan_optimality_proof#my-doubts){:target="_blank"} with respect to one of the steps regarding the proof of this proposition. In fact, I wrote a [post](https://datascience.stackexchange.com/questions/113390/minor-error-in-ian-goodfellows-gan-optimality-proof){:target="_blank"} back in 2022 asking if anyone knew of a way to overcome what seemed to be a minor error. Surprisingly, after three years somebody has taken the time to provide a more convincing proof of that tiny step and also highlighted an omission in the Goodfellow paper. So, without further ado, let's see what I was missing and what Goodfellow was missing.

First, let's remember what was the proof. It involves two steps: a change of variable and a maximization problem. The change of variable is a bit technical and you can give a look to an sketch of the details and the theorems involved in [my previous post]({{ site.baseurl }}/gan_optimality_proof#prop){:target="_blank"}. It reduced the problem to finding the maximum of this integral

<div>$$ \int_{\textbf{x}} p_{data}(\textbf{x})\log(D(\textbf{x})) + p_g(\textbf{x})\log(1-D(\textbf{x})) d\textbf{x} $$</div>

The original argument to maximize this integral read, quote: "For any $(a,b) \in \mathbb{R} - \{(0,0)\}$, the function $y \rightarrow a \log (y) + b \log (1-y)$ achieves its maximum in $[0,1]$ at $\frac{a}{a+b}$." That argument for me was insufficiently explained, but it is correct (for the most part). The argument is basically constructing a function that at each point is the maximum; therefore, when integrating, the result is the maximum possible. I initially understood the argument as simply optimizing the integrand which seemed incorrect to me because $(a,b)$ here are not constant. But later on, Graham Pulford pointed out that this is calculus of variations. So here it goes what I think is a more rigorous rewrite of that step. We define the lagrangian to be

<div>$$ \mathcal{L}(\textbf{x}, D, D') = p_{data}(\textbf{x})\log(D(\textbf{x})) + p_g(\textbf{x})\log(1-D(\textbf{x})) $$</div>

Thus, the optimum (if it exists) must satisfy the Euler-Lagrange equations:

<div>$$ \frac{\partial \mathcal{L}}{\partial D} - \frac{d}{d\textbf{x}}\frac{\partial \mathcal{L}}{\partial D'} = 0 $$</div>

It looks like I am treating multivariable as single variable but I am just using this notation for simplicity: $\frac{d}{d\textbf{x}} = \sum_i \frac{\partial}{\partial x_i}$. The Euler-Lagrange equations is only one equation in fact because there is no derivative in the lagrangian. Therefore we just need to solve for $\frac{\partial \mathcal{L}}{\partial D} = 0$. With some patience that leads to the desired result:

<div>$$ 
\begin{align*}
&\frac{\partial \mathcal{L}}{\partial D} = \frac{p_{data}(\textbf{x})}{D} - \frac{p_g(\textbf{x})}{1-D} = 0\\
\Rightarrow& \frac{p_{data}(\textbf{x})}{p_g(\textbf{x})} = \frac{D}{1-D} = \frac{1}{1-D}-1\\
\Rightarrow& \frac{p_{data}(\textbf{x}) + p_g(\textbf{x})}{p_g(\textbf{x})} = \frac{1}{1-D}\\
\Rightarrow& D = \frac{p_{data}(\textbf{x})}{p_{data}(\textbf{x}) + p_g(\textbf{x})}
\end{align*}
$$</div>

But there is a catch. This argument only works for sufficiently smooth lagrangians which is why intuitive arguments should be made rigorous. Taking the optimum at each point and integrating only returns the functional optimum if the functions are not pathologic, which in this context means twice differentiable. To solve the Euler-Lagrange you only need the integrand to be once differentiable, but to prove it is a maximum you need to look into the second derivative and see it is negative, which is, in fact, the case:

<div>
$$ \frac{\partial^2 \mathcal{L}}{\partial D^2} = -\left(\frac{p_{data}(\textbf{x})}{D} + \frac{p_g(\textbf{x})}{1-D}\right) < 0 $$
</div>

And what happens if you do not have a sufficiently smooth integrand? In that case you no longer have such a simple way to find the optimal discriminator. But that surely only happens in the mind of the perturbed mathematicians, right? Wrong. That assumption can be broken very easily. [Graham Pulford](https://ieeexplore.ieee.org/document/9641798){:target="_blank"} showed that having $\dim(\textbf{z}) < \dim(\textbf{x})$ is enough to break the smoothness of the lagrangian. This comes from the first step of the proof: the change of variable. When reducing the dimensionality of a probability distribution function the behaviour can be pathological, breaking the smoothness. In that article I linked, he constructed several concrete examples showing such pathological behaviour. That same author [went a step further](https://ieeexplore.ieee.org/abstract/document/11030454){:target="_blank"} and constructed a discriminator that was optimal but was nowhere equal to the $1/2$ that Goodfellow promised. Curiously enough, that discriminator produces $1$ almost everywhere and $0$ in a set of measure zero, which means it is also a stupid discriminator that is overconfident in saying that everything is fake. As expected, answering one question creates new ones. In this case I am left with the doubt of whether or not the optimal discriminator is always independent with respect to the generator. Maybe in another three years that is also solved? 

Apart from the theoretical insights, all of these new results bring more light to the practical side of the GANs. Training a GAN was always an unstable process that required many tweaks to make it work. We now know the reason for that instability. The initial algorithm for training GANs was an iterative process that tuned discriminator and generator in alternate processes. The tuning method for the discriminator involved that formula that appeared in the proposition we mentioned before. That formula we now know has no guarantees of being always correct. Since the issue was with the smoothness, many tweaks for making the learning more stable did that in different ways. Either with regularization or controlling the rate of change. But, in the end, every method was just a patch to a fundamental flaw in the formulation. This may explain why everybody has moved to diffusion models. Their formulation is more robust and its training is better understood.