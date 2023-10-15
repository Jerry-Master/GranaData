---
layout: post
title:  "How to make a full audiobook with AI tools."
author: jose
categories: [ stories, tutorial, AI ]
tags: [ AI ]
featured: false
hidden: false
comments: false
share: false
use_math: false
image: assets/images/audiobook/Cover.png
time_read: 7
---

A few days ago I got access to DALLE·3 and thought, "what if I made a book for children with it?" It may seem a bold idea, but as you will see, it played out decently and that's the reason for this tutorial. Since there is not yet a full consensus on the copyright of this material, I won't be posting the full audiobook just in case. But if you follow this tutorial you may end up with a similar copy in your hands. The process is quite simple:

1. Ask GPT-4 to structure a book around a given topic, which in my case was "animals in Africa".
2. Create the figures using DALLE·3.
3. Give texture to letters using Adobe text effects.
4. Compose letters and images in powerpoint.
5. Generate the audio using Tortoise.
6. Edit video and audio using Davinci Resolve. 

The objective is to reduce the human in the process as much as possible, although some careful editing and reviewing will always be neccesary. Let's dive into the details.

# GPT-4

One would think that a lot of prompt engineering is needed to make a full book, even if it is for children, right? Well, no. The prompt I used was simply this:

> hey, i want to create a child book for my nephew, he loves animal from africa, like giraffes and lions and pumas. Would you like to help me build a narrative together with the proper animations?

Yeah, that's it! Even with caligraphic errors GPT-4 understood the task and gave me this in response:

> ### Narrative:
>
> **Title**: "The Great African Adventure"
>
> **1. Introduction**:
> In a land far away, where the golden savannah stretches as far as the eye can see, three unlikely friends embark on an unforgettable journey. Meet Gigi the Giraffe, Leo the Lion, and Pippa the Puma.
>
> **2. The Lost Waterhole**:
> One day, Gigi notices that their favorite waterhole is starting to dry up. The three friends decide to search for a new one, ensuring they have water during the hot summer days.
>
> **3. The Mysterious Map**:
> While resting under an acacia tree, Pippa finds a tattered map blowing in the wind. It hints at a hidden waterhole, surrounded by lush greenery and cool shade. They decide to follow it.
>
> **4. Challenges Along the Way**:
> As they journey, they face various challenges. They cross rapid rivers, climb steep hills, and navigate through dense forests. Each friend uses their unique abilities to help the group. Gigi uses her long neck to scout ahead, Leo roars to scare away potential threats, and Pippa's agility helps them find shortcuts.
>
> **5. The Hidden Oasis**:
> After days of searching, they stumble upon a hidden oasis, just as the map had shown. It's more beautiful than they could have imagined, with fresh, clear water and plenty of food.
>
> **6. Conclusion**:
> The trio realizes that their journey was about more than just finding water. It was about friendship, teamwork, and the adventures they shared. They decide to keep the map as a reminder of their great African adventure.

> Now, let's create some illustrations to go with our story. I'll start by creating images for the introduction and the first two events. Shall we?

Not bad, but not a book either, this is more like a summary. So, given that summary, I then asked GPT-4 to create the full book, chapter by chapter. This was my prompt for the introduction:

> Okay, let's be more sistematic. We have 6 chapters. Let's start with the introduction. Write me a simple story that would fit in 5 pages with one sentence in each page. Also, for each page an illustration is needed. The characters must be the same as before: Gigi the Giraffe, Leo the Lion and Pippa the Puma.

And the response:

> ### Introduction: Meeting the Trio
>
> **Page 1**:
> **Sentence**: "In the heart of the African savannah, three friends stood tall and proud."
> **Illustration**: A vast savannah landscape with Gigi the Giraffe, Leo the Lion, and Pippa the Puma standing together, the sun setting in the background.
>
> **Page 2**:
> **Sentence**: "Gigi, with her long neck, loved to watch the clouds and dream."
> **Illustration**: Gigi gazing upwards at the sky, a dreamy expression on her face, as whimsical cloud shapes float above.
>
> **Page 3**:
> **Sentence**: "Leo, with his majestic mane, loved to roar and ensure everyone was safe."
> **Illustration**: Leo standing on a small mound, letting out a powerful roar, with birds taking flight in the background.
>
> **Page 4**:
> **Sentence**: "Pippa, always curious, loved to explore hidden paths and trails."
> **Illustration**: Pippa sneaking through some tall grass, her tail flicking with excitement, as she discovers a hidden trail.
>
> **Page 5**:
> **Sentence**: "Together, they were ready for any adventure the savannah had in store."
> **Illustration**: The three of them walking side by side, with the vast savannah ahead, signaling the beginning of their journey.

> Let's start by creating the illustrations for these pages. Shall we?

And this is the process, you tell GPT-4 how many pages you want per chapter and it expands the summary to fit into that number of pages. Even better, it suggests some illustrations, let's see how to make them a reality.

# DALLE·3

A few months ago, to achieve the illustrations one would have to take the prompt suggested by GPT-4 and take it to Midjourney, or Stable Diffusion to generate a valid image. The process required a lot of trial and error and a bit of prompt engineering. Now, however, DALLE·3 is embedded inside GPT-4, so you just have to say "yes" and it will generate the illustrations, like this:

<div class="image-grid">
    <div class="image-container">
        <img src="{{site.baseurl}}/assets/images/audiobook/dalle1-1.png" alt="dalle1_1" />
    </div>
    <div class="image-container">
        <img src="{{site.baseurl}}/assets/images/audiobook/dalle1-2.png" alt="dalle1_2" />
    </div>
    <div class="image-container">
        <img src="{{site.baseurl}}/assets/images/audiobook/dalle1-3.png" alt="dalle1_3" />
    </div>
    <div class="image-container">
        <img src="{{site.baseurl}}/assets/images/audiobook/dalle1-4.png" alt="dalle1_4" />
    </div>
</div>

Since it is limited to generating four at a time you need to generate them in batches, which is a minor problem since you can just say "continue" and it will do the rest. As you can notice, even though I did not specify any specific style or artist, these images do not seem to be copyright-free. Some of them resemble too much to Disney style or to other cartoons. Technically, OpenAI gives you ownership of this images to do whatever you want, commercial or not. But it is not clear to me that you are really allowed to _do whatever you want_. The problem is, even if I wanted to credit the authors of this material, or ask for permission to cite, or even request a commercial license, I don't know _who_ is the author I should be asking permission for. Anyway, the process is as simple as I described here and it is more or less automatic. In many cases the algorithm does not generate what I ask it for, but by repeating the question several times you can arrive to a satisfying image almost always.

Next step, generating covers for every chapter. This is a bit more challenging since generating letters in images is a quite difficult task, and it fails horribly most of the time. For instance, generating the words "The Hidden Oasis" seems an impossible task, here are some examples of the failure cases:


<div class="image-grid">
    <div class="image-container">
        <img src="{{site.baseurl}}/assets/images/audiobook/fail1.png" alt="fail1" />
    </div>
    <div class="image-container">
        <img src="{{site.baseurl}}/assets/images/audiobook/fail2.png" alt="fail2" />
    </div>
    <div class="image-container">
        <img src="{{site.baseurl}}/assets/images/audiobook/fail3.png" alt="fail3" />
    </div>
    <div class="image-container">
        <img src="{{site.baseurl}}/assets/images/audiobook/fail4.png" alt="fail4" />
    </div>
    <div class="image-container">
        <img src="{{site.baseurl}}/assets/images/audiobook/fail5.png" alt="fail4" />
    </div>
    <div class="image-container">
        <img src="{{site.baseurl}}/assets/images/audiobook/fail6.png" alt="fail4" />
    </div>
</div>

With a lot of trial and error I could manage to get cover for all of the chapters, but re-generating the illustrations to include extra text on them seemed and impossible task. For that reason I decided to edit the text in Adobe Firefly.


# Adobe text effects

I could have just used plain colors for the text, but it seemed too boring, so I decided to try this AI tool. By using a prompt like "moon" you could add texture to your letters based on it, although the result is not quite there yet in my opinion:

<p class="text-center"><img class="" src="{{site.baseurl}}/assets/images/audiobook/text1-1.png" alt="text" /></p>

For every prompt, no matter what I told to the tool it always gave me dark images. I surrendered and decided to apply a gain to the result if the background was also dark. Nonetheless, I used this tool for all the images because I found it funny, look, there is another example:

<p class="text-center"><img class="" src="{{site.baseurl}}/assets/images/audiobook/text2-3.png" alt="text" /></p>

This one is a bit more special, because I didn't use any original prompt, I just used the whole sentece provided by GPT-4 "The oasis was a paradise, with crystal-clear water and an abundance of food.". This way everything is automatic, you use the sentence as prompt to give texture to itself. The biggest limitation is that the tool only allows a few characters at a time, which made the process quite long and exhausting. The most consuming part was realizing that the text was not even useful because the color didn't match the scene. This is probably the worst part of the book and the part that has the most room for improvement in terms of AI tools.

# Tortoise

Given the catastrophic failure that the letters were, we need to fix it somehow. A possible solution for an unreadable text is to create an audiobook. Can't you read the text? No problem, here is somebody reading it for you. Well, more like *something*. Because we are going to use another AI tool to generate the voices automatically. This tool is not deployed on any pages like the previous tools. If you want to use it you will need to install it in your machine or in colab. In their [github repository](https://github.com/neonbjb/tortoise-tts){:target="_blank"} you have instructions on how to do it. You will need an NVIDIA GPU with CUDA capabilities or a mac with Apple Silicon or a lot of time, you choose. In my case I have a Mac M1 Max and the generation of all the 33 audios took one and a half hour. As an example, the following command generated the audio that is below:

```bash
PYTORCH_ENABLE_MPS_FALLBACK=1 python tortoise/do_tts.py --text "\[I am really excited,\] Let's follow the birds; they'll lead us to water." --voice train_dreams --preset fast --output_path book/chapter2/audio4/ --candidates 1 --seed 210501;
```

<audio controls>
    <source src="{{site.baseurl}}/assets/audio/audiobook/chapter2_audio4_2.mp3" type="audio/mpeg">
    Your browser does not support the audio element.
</audio>

The quality is decent. Its main limitation is the generation of emotions. As you can see in the example above, it is possible to trick the algorithm into expressing emotions, but there is much room for improvement and you need to specify which emotion you want. You could probably use GPT-4 to automatically identify which emotions to give, but for this side project I didn't want to overcomplicate things.


# Davinci Resolve

Finally, let's put everything together and generate the audiobook. We have images, text and audio. So, we can create a video. In my case I decided to compose images and text in powerpoint and then use a predefined animation to pass between pages. Then, I put the presentation in automatic mode giving each slide 8 seconds and recorded the screen. After that, I had to manually synchronize audio and video by cutting and moving segments. Here is the timeline before editing:

<p class="text-center"><img class="" src="{{site.baseurl}}/assets/images/audiobook/before.png" alt="before" /></p>

And here is after editing:

<p class="text-center"><img class="" src="{{site.baseurl}}/assets/images/audiobook/after.png" alt="after" /></p>

Hit render and you are done.

# Final thoughts

The whole process took me 3 days, but I was experimenting the most part. If this was fully automated it could be done in 1 day. Imagine, a editorial could put a hole office of, let's say, 20 employees and create 400 books in a month. Even more, if the process gets even more automatic, a child could read a different book each day of its whole life, or at least until this kind of books bore them. Nobody can deny this technology is going to have a huge impact in ours lives. Either positive or negative is still to be seen. For me, this can have a good impact since it will democratize knowledge even more. Not only that, people will be able to create masterpieces, books, films and many more. You will no longer need a huge budget to do this kind of things. Indie creators could compete with huge studios or editorials. It will all depend on what the legislation will say. If future (or present) politicians decide against this technology, that democratization will never arrive. Big fishes will remain big, and monopolies will win. As much as I believe this technology is capable of wonderful creations, I also believe that politicians are capable of awful laws. Time will say.