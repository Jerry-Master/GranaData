---
layout: post
title:  "The two craziest bugs I have solved in my career so far."
author: jose
categories: [ AI, engineering ]
featured: false
hidden: false
comments: false
share: false
image: assets/images/crazy-bugs/banner.png
time_read: 10
---

This year has been a complete roller coaster with the arrival of AI. However, I still enjoy the craft of developing algorithms and software and find it quite interesting to understand the system we (or AI) builds. It is my belief that there is pure joy in solving a very difficult bug, so I want to explain the two craziest bugs that my team has managed to solve this year which are, by far, the two most amazing bugs I have encountered in my life. If you have a curious mind and enjoy understanding complex systems, this post will amaze you.

For context, our team has been building a new system for true 3D automated optical inspection. Since this is quite niche, let me introduce the field to you first. Let's start by refreshing the concept of a PCB (Printed Circuit Board). It is how modern electronics is built nowadays. They look as you can see in these four examples.

<div class="image-grid">
  <img src="{{ site.baseurl }}/assets/images/crazy-bugs/pcb-1.jpg" alt="PCB 1" />
  <img src="{{ site.baseurl }}/assets/images/crazy-bugs/pcb-2.jpg" alt="PCB 2" />
  <img src="{{ site.baseurl }}/assets/images/crazy-bugs/pcb-3.jpg" alt="PCB 3" />
  <img src="{{ site.baseurl }}/assets/images/crazy-bugs/pcb-4.jpg" alt="PCB 4" />
</div>

It is an electronic circuit with many different components, ranging from ICs (Integrated Circuits) to BGAs (Ball Grid Arrays) passing through resistors, crystals, capacitors, connectors and many more. Their purpose can also be almost anything: refrigerators, cars, laptops, phones, smartwatches, planes, and even lamps have them these days. Apart from the electronic components, they need to be wired to be connected. The board looks something like this when you only have wires.

<p class="text-center"><img class="" src="{{site.baseurl}}/assets/images/crazy-bugs/only-wires.jpg" alt="only wires" /></p>

Now, the manufacturing process is a bit more involved. You could solder the wires manually and then place the components manually, but this is obviously not how it is done. The whole process is automated from beginning to end. And when you have automation, you need inspection to check if anything goes wrong. Below is the whole pipeline.

<p class="text-center"><img class="" src="{{site.baseurl}}/assets/images/crazy-bugs/assembly-line.jpg" alt="assembly line" /></p>

My team works mainly in the pre-flow AOI inspection step. We develop machines that can automatically detect if the components are correctly placed, and can do it very fast and with a lot of precision. When you work at such levels of speed and precision you start to notice system failures that you wouldn't encounter in any other field. For confidentiality reasons I cannot describe the system and the failures in full detail, but I will try to simplify and abstract everything so that you get a sense of how absurd the bugs were.

## Bug #1

For the first bug, some more context is needed. I work in the algorithm part of the machine. My company builds everything, GUI software, firmware, hardware, optics and algorithms. My role is focused solely on the latter. There are many algorithms, but the one I have been working on for the past two and a half years is quite complex and sometimes we find a minor failure gets increased to something that crashes the machine. So, my algorithm is made of several modules that I will refer to them just as M1, M2, ..., and so on. The first bug was noticed because sometimes, randomly, the machine will take minutes instead of seconds. That's it, that's the bug: random execution times. This is not a crash per se, but such hang can halt the manufacturing process so it can be considered a crash and obviously needs to be solved. Now, how on earth do you debug random execution times when everything works smoothly and no error is logged anywhere? Well, you basically just call me ;)

Okay, jokes aside, how do you actually solve this? The first thing is to detect what module is at fault and dump the state before and after it to analyze it. Luckily for me, even if the halt is random, it happened with enough frequency. As we will see, in the second bug we weren't so lucky, the second bug took several months to fix because each iteration required three whole days. But for this first bug, we just needed a few minutes to reproduce.

The first analysis showed that module M7 was the one that randomly halted execution. The dump of the input showed this.

<p class="text-center"><img class="" src="{{site.baseurl}}/assets/images/crazy-bugs/white-lines.png" alt="white lines" /></p>

The white lines should not be there. That module depends on the image being aligned with another image that comes from M6 because it involves an operation that may not converge if that does not happen. So, we now know why the pipeline halts. Some module from M1 to M5 distorts the image and misaligns it with the output of M6, and M7 does not converge. The next question is, which module is causing such weird noise patterns? Some further analysis localized the error to M4. 

<div class="image-grid">
  <figure>
    <img src="{{ site.baseurl }}/assets/images/crazy-bugs/m4-input.png" alt="M4 input" />
    <figcaption>M4 input</figcaption>
  </figure>

  <figure>
    <img src="{{ site.baseurl }}/assets/images/crazy-bugs/m4-output.png" alt="M4 output" />
    <figcaption>M4 output</figcaption>
  </figure>
</div>

Good. We now know exactly where the problem is. However, when looking at the specific function that painted those lines no visible problem is found. The function does not have any memory related issues, and the CUDA kernel works perfectly in isolation. The logic is fine, the implementation is correct and it is only with that specific input that such problem occurs. This drove me crazy for a few days. In the end I decided to measure if there was any difference in the input between when the artifacts appeared and when they didn't. Maybe there is something in the input that is different even if it is not visible at first. 

<p class="text-center"><img class="" src="{{site.baseurl}}/assets/images/crazy-bugs/diff.png" alt="diff" /></p>

Can't you see it? Let me zoom a bit for you on the top part.

<p class="text-center"><img class="" src="{{site.baseurl}}/assets/images/crazy-bugs/zoom.png" alt="zoom" /></p>

There you have it. A line of outliers that appear out of nowhere. Moreover, those values are crazy high and have nothing to do with the expected range of values for the input. So we now have an explanation of why a perfectly valid function was creating artifacts: because the input was corrupted. The next step is to find when those outliers are introduced. We can feel we are close to reaching the real culprit of the bug because the error is now quite structured. In the first image the noise pattern was completely random but now we just have a line of high values at the top of the image. 

Any ideas? What do you think could be causing something like that? Well, the reason was that I forgot to implement proper boundary checks in a previous kernel. There was a kernel that should ignore values at the top of the image but was instead copying them. The fix ended up being just this:

<p class="text-center"><img class="" src="{{site.baseurl}}/assets/images/crazy-bugs/fix.png" alt="fix" /></p>

But I wasn't quite convinced by that solution. The output buffer shouldn't need to be filled with NAN values. The output buffer is void and is filled inside the kernel. If you don't fill the values, they should just be zero, right? Well, not if you did not initialize the variable. That was the biggest facepalm of my career. During my training at university we worked in Linux where uninitialized variables are initialized most of the time to zero. However, this is the real world and people use Windows. In Windows uninitialized variables are not initialized at zero. In fact, they are initialized at random values, very high values in some cases. That is why my mental model expected this to never happen and why I didn't bother to put the halo check in the first place. Fuck Windows; that is the conclusion. And also remember to always initialize your variables, even if they are output buffers, because there could be halo effects like this one.

## Bug #2

The second bug was even crazier than the first one. Bug #1 is sweet in comparison. Let me show you. As I said before, our machines operate in an industrial setting, so they need to be tested for long-run execution. At the beginning, long-run tests failed because of memory leaks. The first memory leak was MBs of memory so after a few hours the machine crashed. The second memory leak was a few bytes of memory so it needed a few days, but it also crashed. The reason why a memory leak crashes the machine is because the algorithms are run indefinitely over and over. Since each algorithm execution is done in a few seconds, the effect compounds over time. Also, no human is at the computer, so no memory cleaning can be done by restarting the program. Therefore, memory leaks consume memory until there is no more and the system crashes. Sometimes, this error shows in long execution times because the OS starts doing memory swapping. But for the most part it just crashes. These types of long-run failures are easy to detect, you just log the memory information, see it is increasing and you know it is a memory leak. But Bug #2 was on a whole new level.

Bug #2 was also a crash in the long-run test. But in contrast with what happens with memory leaks, the crash was random. In a memory leak you can predict the time it takes for the machine to crash depending on the size of the leak. However, in Bug #2 it sometimes took 4 hours and sometimes took 3 days. We were sure it was not a memory leak because we logged memory and cpu information and nothing unusual happened. The crazy part of this bug is that it only showed when the code used 2 threads, not when we used 1 thread. For context, our code is parallelized in the gpu so we don't need cpu threads for the most part. The only reason we have several threads is to hide latency between one iteration and the next. This makes the bug seem like something impossible to solve because it is not caused by parallelism itself, but by one thread interfering with the other, even though each thread waited for the other. So, how do we debug this? Calling me again ;) I'm joking, I did not solve this bug, it was Claude under the supervision of my coworker Luis.

Again, jokes aside. The way you debug something like this is to log information to a file so that when the system crashes you have something similar to the black box of airplanes that survives the crash and can be analyzed afterwards. This took some time because the logging system needed to be connected to the GUI software and so we could not do it ourselves and needed to involve the GUI SW team. After some back and forth, we finally got the logging system connected and had some file to analyze after each crash.

What do you think we found in the logs? You are right, absolutely nothing. Even though we had placed markers everywhere in the code and added try / catch blocks everywhere the logs showed no traceback and there was nothing apart from the code of the program after the crash. Knowing the program executed with code -1 is not a lot of information to deal with. But it is information, nonetheless, it tells you that this is a CUDA kernel crash due to some illegal memory access because that is kind of the only way this can happen. The problem is, you cannot get much more information than this. Or so we thought.

Apparently, you can dump the core of the GPU after a crash with `CUDA_ENABLE_COREDUMP_ON_EXCEPTION=1`. So you can get more information indeed. But, and there is always a but, that information is a bunch of bytes encoding kernel state and GPU instructions. It is highly cryptic. 

```
^?ELF^B^A^A^@^@^@^@^@^@^@^@^@^4^@>^@^A^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@
ø^C^@^@^@^@^@^@^@^@^@^@P^@8^@^G^@@^@^@^@^@^@^D^@^@^@^T^@^@^@CORE^@^@^@^@
^A^@^@^@^@^@^@^@NT_GPU_CUDA_EXCEPTION_CONTEXT^@^@^@^@^@^@^@^@^A^@^@^@
^@^@^@^@^X^@^@^@^A^@^@^@CUDA_SM_TYPE_BLACKWELL_120^@^@^@^@^@^@^@^@^@^@
P¿àG©\ÿ^?^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@
`¥§0^@^@^@^@`¥§0^@^@^@^@^X^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@@^@^@^@^@^@^@^@
^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@ì^?^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@
@ÿÿÿÿÿÿÿ^?^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@
\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x90\x00\x00\x00\x00\x00\x00\x00\x00
\x7f\x31\xab\xb9\xf6\xd0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00
\xfe\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00
^A^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@
.shstrtab^@.cuda_exception_info^@.cuda_warp_state^@.cuda_sm_0_register_file^@
.cuda_sm_0_shared_mem^@.cuda_global_mem_segment_0x7f31a0000000^@
^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@
Hæ^P^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@
^@^@^@^@^@^@^@^@\x80\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00
4á¿ª\x8f^A^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@
```

Luckily, there are tools for analyzing this like `cuda-dbg` that can convert that to something slightly more readable:

```
Opening GPU coredump: core.cuda.myhostname.12345
[New LWP 1799919]
[New Thread 0x7f31abb9f6d0 (LWP 1799919)]
CUDA Exception: Warp Illegal Address
The exception was triggered at PC 0x7f31abb9f6d0: my_broken_kernel(int*, int) at vector_add.cu:42

[Current focus set to CUDA kernel 0, grid 1, block (0,0,0), thread (0,0,0), device 0, sm 124, warp 0, lane 0]
```

So, Luis went and looked at the kernel that crashed and the values that caused the crash and found that the values were: 0x3d0d7793 (0.034538), 0x3d649f10 (0.055816), and 0x3d3779113d0d7793, which if split to 32bits results in 0x3d377911 (0.044793) and 0x3d0d7793 (0.034538)​. Here is when a human just pauses and wonders at how utterly fucked he is in trying to find why on earth those values crash the kernel and where do they come from. But, AI just automatically recognized them as the values from a gaussian kernel with sigma of 5 and pointed to the exact line of code that caused it. Magic.

To be more descriptive, what was happening was the following. Our code is highly parallelized, we have cpu code with gpu code in threads and streams. We also use a memory pool and a global allocator of memory. There was one function that was not using streams properly and was giving access to a memory address before it was available. 

<p class="text-center"><img class="" src="{{site.baseurl}}/assets/images/crazy-bugs/stream-bug.png" alt="stream-bug" /></p>

Can't you see the problem? The upload is not on any stream. The fix is just this.

<p class="text-center"><img class="" src="{{site.baseurl}}/assets/images/crazy-bugs/stream-fix.png" alt="stream-fix" /></p>

What was happening here is that the allocator was giving the memory address to the cpu thread before the gpu stream had access to it. If you upload on the stream, then nothing happens because the cpu values won't upload to the gpu until the memory is valid. However, if you don't specify the stream you will upload the values before the memory address is valid. Simple, right? Well, the thing is that for this operation to crash a kernel the uploaded values need to end up in a part of the memory that is currently being used by a different thread which explains why this crash did not happen when using just one thread. The fact that the values are randomly placed in memory also explains why the crash appeared randomly. Sometimes the upload operation places the values in a place in memory that is not used by the other thread, so even though it is illegal nothing happens. But on very rare occasions they ended up in two specific kernels, where those values caused the gpu threads to compute some indices that were outside of the bounds of the buffers and then the real illegal memory access occurred. 

Let's pause for a moment to admire Bug #2. A bug that disappeared when activating debug flags. A bug that crashed in a kernel that was not the one responsible for it. A bug that occurred due to the allocator providing illegal gpu access to a cpu thread. A bug that occurred once in days and left no useful logs whatsoever. A bug, that without the help of AI would have been impossible to solve. And finally, a bug that was caused by a human error that AI would never make: forgetting to write boilerplate code (the stream in the upload operation).

# Conclusion

I want to end this post by claiming that AI will make software far more secure and stable than what we have today. Latest cybersecurity incidents put the focus on the offensive usage of AI and how it is posing a significant threat. But what we have to think is that AI is able to exploit human bugs, not AI bugs. These two bugs were caused because software was developed during the period of two years. It is impossible for a human to not fail one day or to never forget anything. Code in my company is reviewed by several people before getting merged. It is tested locally, then on the CI / CD server and then on the machine. And even under those circumstances these two bugs took weeks or even months to detect, and far more to fix. And in both cases the bugs were the result of a human forgetting a tiny little detail. AI does not make these kinds of stupid mistakes. A human can forget the stream, but let me assure you that Opus 5.5 will never forget such detail. In the upcoming years we will see AI used to exploit human errors made in this century but once human errors are gone, AI errors won't exist. After we patch existing software and update existing systems, no exploit nor crash due to illegal memory access will ever be created again if we use AI properly. So don't be afraid of the future, in the long term we will all be safer.