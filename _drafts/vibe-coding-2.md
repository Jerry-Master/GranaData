---
layout: post
title:  "Vibe-coding, an informed guide (Part II)."
author: jose
categories: [ AI ]
featured: false
hidden: false
comments: false
share: false
---

It was only a year ago when we were discussing [vibe coding]({{site.baseurl}}/vibe-coding){:target="_blank"} in its initial form. Productivity gains were estimated to be more than 14% and prices were less than 2000$ a year. It was very primitive given current standards but we had companies like replit providing some level of agentic coding. A year has passed and it is now time to look at the data again and see where we are now. Agentic coding is all over the place now. We have Claude Code, Codex, OpenCode, Pi and many more interfaces to interact with the models. The chat-based interface can be now considered obsolete. Models have also come a long way, so long that the US government is even denying access to some of them ([Fable](https://www.anthropic.com/news/fable-mythos-access){:target="_blank"}) to the rest of the world. The psicosis has only increased and that is the reason I am writing a new post to clarify the situation with the available evidence and data that we have today.

On today's post we will be answering the following questions: 
* How does an agent work? 
* How much does it cost? 
* Is it worth it? 
* What are its limitations?

Bear with me till the end because there are many remarkable facts and anecdotes that will catch your attention.

# The Agentic Loop

A year ago, coding with LLMs consisted mainly in copy-pasting snippets of code between the chat interface and your codebase back and forth. If you didn't look at the code it was considered vibe-coding, but you could review what you were doing to prevent hallucinations and it was the go-to tool for many developers for function implementation. The agentic loop is basically eliminating the human from the codebase-to-LLM step and just letting the model interact directly with the codebase. In its more primitive form, vibe-coders merged all the codebase into one file so that it could fit in one message. As you may be thinking now, that is inefficient and a huge bad practice in coding because you are destroying any modularization you had. To solve that issue models were trained to use tools.

LLMs are, as its name says, language models. They only understand language and they cannot run commands. But what they can do is to say "run the Read(path) tool". To implement this properly, the model needed to be more structured in its output. Many companies did this at the same time, but we can point to [this paper](https://arxiv.org/html/2505.04016v1){:target="_blank"} for an example of how this looks:

<p class="text-center"><img class="" src="{{site.baseurl}}/assets/images/vibe-coding-ii/toc_llmformatter.png" alt="structured output example" /></p>

How the models were trained to do that is out of the scope of this post but the idea is simple, just make the model output a json that a program can translate into an action. Once the model knows how to call a tool, the agentic loop consists of feeding the output of the command back to the model. This way the model can run autonomously and look inside a codebase without having to interact with a person. Anthropic has a nice diagram and explains in more detail how it works in [their blog](https://code.claude.com/docs/en/agent-sdk/agent-loop){:target="_blank"} and if you are interested in the low-level details of the loop there is [this vibe-coded page](https://ccunpacked.dev/){:target="_blank"} that was created after the [Claude Code leakage](https://github.com/tanbiralam/claude-code){:target="_blank"}:


<p class="text-center"><img class="" src="{{site.baseurl}}/assets/images/vibe-coding-ii/agent-loop-diagram.svg" alt="agentic loop" /></p>

This loop shows what happens when you ask the agent "How can I run this code locally?". Instead of having to manually copy and paste the `README.md` and all the main files, the agent can go and look directly into those files. Not only can the model read, but it can also write and modify your files. Of course, it can only do so if you let it. The interfaces don't give permissions to the models to anything by default and you can always control what you let the model do. However, alert fatigue can happen and in another [METR report](https://metr.org/es/blog/2026-05-19-frontier-risk-report/#coding-agents-did-real-projects-that-would-take-humans-hours-or-days){:target="_blank"} it was measured that between 20% and 40% of workers just allow the model to do everything unrestricted:

<p class="text-center"><img class="" src="{{site.baseurl}}/assets/images/vibe-coding-ii/metr-unrestricted-access.png" alt="metr figure" /></p>

Security concerns aside, the agentic loop can be improved with three elements:

* Planning
* Model Context Prototocols (MCPs)
* Skills

In the current state of affairs, models sometimes loop indefinitely trying something that goes nowhere. For that reason planning is usually a good approach. By dividing the task into a planning stage and a execution stage one can prevent such wasteful loops in the planning phase and also use a cheaper model in the execution phase. This is the logic behind [opusplan](https://code.claude.com/docs/es/model-config){:target="_blank"}, for instance. In my company, the savings are estimated to be around 28% when using opusplan versus just using opus and the tasks are completed perfectly fine. Normally, it is better to plan the task ahead before executing it, not only when using agents but as an advice in general.

The other problem that models have is that they are limited in how long the sessions can be. LLMs have a context window and once its limit is reached you have to either clear or compactify the session to continue. This implies that one cannot provide the model with an infinite amount of tools. Here is when MCPs come into play. The basic agent can read, write and execute commands but if you are interested in using a specific API you can provide commands to use that API specifically without having to insert the full API documentation into the context window. An example of that is the Atlassian MCP. One task that I do usually is to write reports about my job. Those reports need to be uploaded to Confluence and with the Atlassian MCP I can automate that part of my job. You can just tell the agent "look at commit messages and create a confluence page with aggregate metrics and an executive summary of what I have done in the past six months" and it will do it. It can also look into Jira tickets and explain the task to you when the description of the task is not descriptive enough. There are many MCPs that can be activated or deactivated when needed. There are MCPs for extending the memory, for using sharepoint, for decrypting files with DRM, for using a web browser and many more. You can extend the tools available to the agent with whatever is needed.

And the last element to extract the maximum value out of the agents are the skills. Skills are just markdown files that contain system prompts. They have this fancy name but in the end are just system prompts. Nevertheless, they can be very useful and there is a [marketplace](https://skillsmp.com/es){:target="_blank"} for the most popular and used ones. Here I will just mention my favorite: [caveman](https://github.com/JuliusBrussee/caveman/tree/main){:target="_blank"}. What is it about? Well, its slogan says it all: "🪨 why use many token when few do trick". Speaking like a caveman can not only reduce token consumption but also improve performance due to less context rot. Apart from the token savings I love this skill because it makes my job a hell of a lot funnier. The only risk associated with this skill is that you may become a caveman yourself. The other day I said "me hungry, lunch when" and my colleagues joked responding "caveman stop". Definitely recommend. 

# The Bill

Having shown how it works and assuming it is useful, one may ask the price. Last year we had 8$ per million output tokens with OpenAI smartest model at the time. How much are today's models worth? This question can be difficult to answer because token cost and real cost are two different things. A very cheap but fast and dumb model that loops around forever can cost you a lot for nothing. So let's first see the token price and then move on to the real price. Here is a wide view of the pricing for the main models available today:

| Provider       | Model                         | Input ($/1M) | Input cache ($/1M)  | Output ($/1M) |
|----------------|-------------------------------|--------------|---------------------|---------------|
| OpenAI         | gpt-5.5 (Flagship)            | 5.00         | 0.50                | 30.00         |
| OpenAI         | gpt-5.5-pro                   | 30.00        | —                   | 180.00        |
| OpenAI         | gpt-5.4                       | 2.50         | 0.25                | 15.00         |
| OpenAI         | gpt-5.4-mini                  | 0.75         | 0.075               | 4.50          |
| OpenAI         | gpt-5.4-nano                  | 0.20         | 0.02                | 1.25          |
| OpenAI         | gpt-4o                        | 2.50         | 1.25                | 10.00         |
| OpenAI         | gpt-4o-mini                   | 0.15         | 0.075               | 0.60          |
| OpenAI         | o3 (Global)                   | 2.00         | 0.50                | 8.00          |
| OpenAI         | o4-mini (Global)              | 1.10         | 0.28                | 4.40          |
| Anthropic      | Claude Fable 5                | 10.00        | 1.00                | 50.00         |
| Anthropic      | Claude Opus 4.8               | 5.00         | 0.50                | 25.00         |
| Anthropic      | Claude Sonnet 4.6             | 3.00         | 0.30                | 15.00         |
| Anthropic      | Claude Haiku 4.5              | 1.00         | 0.10                | 5.00          |
| Anthropic      | Claude 3.5 Haiku              | 0.80         | 0.08                | 4.00          |
| Google         | Gemini 3.5 Flash              | 1.50         | 0.15                | 9.00          |
| Google         | Gemini 3.1 Pro (≤200k)        | 2.00         | 0.20                | 12.00         |
| Google         | Gemini 3.1 Pro (>200k)        | 4.00         | 0.40                | 18.00         |
| Google         | Gemini 3.1 Flash-Lite         | 0.25         | 0.025               | 1.50          |
| Google         | Gemini 3 Flash                | 0.50         | 0.05                | 3.00          |
| Google         | Gemini 2.5 Pro (≤200k)        | 1.25         | 0.125               | 10.00         |
| Google         | Gemini 2.5 Flash              | 0.30         | 0.03                | 2.50          |
| Google         | Gemini 2.5 Flash-Lite         | 0.10         | 0.01                | 0.40          |
| GLM (Z.ai)     | GLM-5.2                       | 1.40         | 0.26                | 4.40          |
| GLM (Z.ai)     | GLM-5                         | 1.00         | 0.20                | 3.20          |
| GLM (Z.ai)     | GLM-4.7                       | 0.60         | 0.11                | 2.20          |
| GLM (Z.ai)     | GLM-4.5-Air                   | 0.20         | 0.03                | 1.10          |
| GLM (Z.ai)     | GLM-4.7-Flash                 | Free         | Free                | Free          |
| DeepSeek       | V4 Flash                      | 0.14         | 0.0028              | 0.28          |
| DeepSeek       | V4 Pro (Promo)                | 0.435        | 0.003625            | 0.87          |
| DeepSeek       | V4 Pro (Base)                 | 1.74         | 0.145               | 3.48          |
| DeepSeek       | R1 (Heredado)                 | 0.55         | 0.14                | 2.19          |
| Qwen           | Qwen3.7-Max (Promo)           | 1.25         | 0.125               | 3.75          |
| Qwen           | Qwen3.7-Plus (≤32k)           | 0.32         | 0.032               | 1.28          |
| Qwen           | Qwen3.6-Plus                  | 0.50         | 0.05                | 3.00          |
| Qwen           | Qwen3.6-Flash                 | 0.19         | 0.019               | 1.13          |
| Qwen           | Qwen3 Coder Plus (≤32k)       | 1.00         | 0.10                | 5.00          |
| Kimi (Moonshot)| Kimi K2.6                     | 0.95         | 0.16                | 4.00          |
| Kimi (Moonshot)| Kimi K2.7 Code                | 0.95         | 0.19                | 4.00          |
| Kimi (Moonshot)| Kimi K2.5                     | 0.60         | 0.10                | 3.00          |
| Kimi (Moonshot)| Moonshot V1 (8k)              | 0.20         | —                   | 2.00          |
| Mistral        | Large 3 (2512)                | 0.50         | 0.05                | 1.50          |
| Mistral        | Medium 3.5                    | 1.50         | 0.15                | 7.50          |
| Mistral        | Small 4                       | 0.10         | 0.01                | 0.30          |
| Mistral        | Codestral                     | 0.30         | 0.03                | 0.90          |

These are some of the main models competing for the leaderboard as of today. Each company has some kind of very smart, very expensive model and also some cheap and simpler models. The most expensive one is gpt5.5 Pro which costs 180$ per million of output tokens. And the best value for money seems to be GLM 5.2 which costs 4.40$ per million of output tokens and is near Opus level intelligence, being Opus the second best model of Anthropic with Fable being the best model and also the banned model we mentioned at the beginning.

As I said, this is only the token cost but we are interested in the real cost. There is this website called [Artificial Analysis](https://artificialanalysis.ai/){:target="_blank"} that has these wonderful charts that show the difference between token cost and real cost:

<p class="text-center"><img class="" src="{{site.baseurl}}/assets/images/vibe-coding-ii/cost-per-task-2.png" alt="artificial analysis cost per task" /></p>

<p class="text-center"><img class="" src="{{site.baseurl}}/assets/images/vibe-coding-ii/cost-per-task.png" alt="artificial analysis cost per task" /></p>

The most capable model can also be the less efficient. The opposite can also happen. Sonnet 4.6 is more expensive per task than Opus 4.7 even though Opus 4.7 is more expensive per token. But Opus 4.8 is more expensive than Sonnet 4.6 both per task and token. Deepseek V4 Pro (Max) and Qwen 3.7 Plus offer way more value for money than other propietary models but have its own limitations. Deepseek is known for having a [94% hallucination rate](https://artificialanalysis.ai/articles/deepseek-is-back-among-the-leading-open-weights-models-with-v4-pro-and-v4-flash){:target="_blank"} and Qwen has very limited reasoning capabilities. 

Knowing that, what is the real cost in real jobs? Let's start with me. I have been using Claude Code for the past 3 months. This is the bill for the whole duration:

- Input tokens (including cache): 1.224.081.064
- Input cache tokens: 1.128.602.083
- Output tokens: 11.159.812
- Cost: 914.69$ 
    - Sonnet 4.6: 658.88$
    - Opus 4.6: 153.18$
    - Opus 4.7: 74.38$

The first month involved a bit of experimentation so a more reliable bill is my consumption in the past month:

- Input tokens (including cache): 510.493.210
- Input cache tokens: 473.904.226
- Output tokens: 3.704.715
- Cost: 297.78$
    - Sonnet 4.6: 266.86$
    - Opus 4.7: 11.63$

Therefore, the real cost is around 300$ for a normal-to-heavy user that codes every day. I use caveman in ultra mode to reduce tokens and only use Opus when the task requires very heavy reasoning which happens very rarely. My job consists in designing computer vision algorithms for automated optical inspection of electronic components. I work with very complex systems, big codebases and a high level of performance. My code maxxes out the GPU usage from the beginning and is supposed to run 24/7 for a long time. Any memory leak can lead to a crash no matter how small it is. This is a real developer job that ends up in production in high stakes scenarios and not just a toy example prepared for a demo. Thus it is safe to assume that 300$ per month per user is a reasonable cost to expect. However, we are seeing that it is not the case for many companies. This is what [one user in twitter](https://x.com/marty_kausas/status/2066913707192410559?s=20){:target="_blank"} said it costed its company:

<p class="text-center"><img class="" src="{{site.baseurl}}/assets/images/vibe-coding-ii/token-cost-other.png" alt="artificial analysis cost per task" /></p>

How on earth are their software engineers spending 10 times more than me? Even though it is impressive, I have more data that proves that many engineers are really spending 3000$ per month. A friend of mine confirmed that figure for Databricks and internal documents of my company also show similar quantities for some departments. So, is it going to cost you 300$ or 3000$? The answer is it depends. Some deeper analysis have shown that the people that consume so much do the following:

* Use Opus (or the smartest model) always.
* Be vague in their descriptions.
* Use the model with 1M context windows instead of the one with 200K.
* Monitor and poll for the output of commands instead of waiting.
* Don't clear session between tasks.

And that's it. A few tricks can cost you thousands of dollars per month. That is how stupid the situation is right now. And that is the reason why Uber has put a [limit of 1500$](https://simonwillison.net/2026/Jun/3/uber-caps-usage/){:target="_blank"} per user after [burning its budget](https://fortune.com/2026/05/26/uber-coo-ai-spending-tokens-claude-code/){:target="_blank"} faster than expected.

That's it for the cost but, is it worth it? Ignoring the spending, let's divert our attention now towards the productivity gains. Nobody can say now that there are no gains, even for experienced developers. Last year there was a [METR RCT study](https://arxiv.org/pdf/2507.09089){:target="_blank"} that showed experienced open source developers got less productive instead of more productive. However, this year the same organization tried to replicate its own result and could not. They wrote an [article](https://metr.org/blog/2026-02-24-uplift-update/#wider-adoption-of-ai-has-made-it-more-difficult-to-measure-task-level-productivity){:target="_blank"} about it and decided not to continue with their productivity trials for one reason: nobody wants to work without AI. That doesn't mean there are no ways of measuring productivity, but the RCT experiment the METR organization wants to perform is no longer possible. RCTs are the most reliable piece of evidence science can produce, but that does not mean there aren't other ways of obtaining evidence even if less reliable. There is [this study](https://www.nber.org/papers/w35275){:target="_blank"} that estimated the real productivity gain to be 30%. That same study shows that code is shipped 180% faster but in the end it only translates into a speedup of 30% for real releases. That study basically shows what every experienced developer already knows: code is no longer a bottleneck. We can produce code now at virtually infinite speed, but the reviewing and testing process keeps being the biggest bottleneck. That is the result of an independent organization but even Anthropic that is biased has reached a similar value. They estimated the value gain of tasks to be 25% in a [recently published study](https://www.anthropic.com/research/claude-code-expertise){:target="_blank"}. So we can safely assume that real gains will be between 25% and 30%. Is that worth it? It depends on how much the worker is paid and how much they cost. For US developers even the 3000$ bill is worth it because their salaries have 6 digits. But for european or asian workers you better reduce the cost or it does not make economic sense.

What about Anthropic and OpenAI valuations? Are those also justified? For the purposes of this analysis let's make a few assumptions that you may disagree with but that are reasonable for me:

* There are [1 billion knowledge workers](https://www.forbes.com/councils/forbestechcouncil/2020/12/10/the-year-of-the-knowledge-worker/){:target="_blank"}.
* There are [47 million developers](https://www.slashdata.co/post/javascript-has-28-million-users-what-this-reveals-about-the-future-of-global-tech-teams){:target="_blank"}.
* Total knowledge workers' [compensation is 50T$](https://github.com/danielmiessler/Substrate/blob/main/Data/Knowledge-Worker-Global-Salaries/knowledge-worker-compensation-data.md){:target="_blank"}.
* Total developers' compensation is 3.2T$. I am assuming an average salary of [70K$ / year](https://www.birjob.com/blog/developer-salaries-global){:target="_blank"}.
* The bill for knowledge workers is an average of 380$ / month. This is based on the previous image.
* The bill for developers is capped at 1500$ / month. This based on Uber monthly cap.
* Developers productivity is increased by 30% and for the rest of knowledge workers is increased by 6%.
* A well established company that is no longer growing astronomically and is considered a value stock has a [PE ratio](https://www.investopedia.com/terms/p/price-earningsratio.asp){:target="_blank"} between 10 and 20.
* All AI company's valuations add up to 7 trillion dollars, that is, seven one trillion dollar companies.
* Everybody uses AI.

With all those hypothesis acknowledged we can estimate how much revenue can the agent industry generate and how much money are companies willing to pay. First, the willingness. Given average compensation and average productivity gains we can expect a total of 3.7T$ of value generated by the increase in productivity. Considering the pricing above and the number of workers there are, an upper bound on revenue would be 432B$. In principle, that revenue is justified by the value created, at least on average. Now, the PE ratio with that revenue would be ~16. This means that if current price and spending continues to hold and the market is saturated by the current companies, on average they could be fairly valued. However, there are caveats to take into account. First, this is just revenue. AI companies have massive capital expenditure that outpaces its revenue growth. Second, on a free market it is very difficult for seven companies to compete without prices going down, specially considering the open source competition and chinese models' pricing. If only OpenAI and Anthropic existed they could create an oligopoly and increase prices. But we have Google, xAI, Z.AI, DeepSeek, Mistral and others competing for a slice of market share. And third, productivity gains are still moderate mainly because of human bottlenecks not because of agent capabilities. Assuming that better models will translate to bigger productivity gains without changes in societal and work organization is a bit optimistic. My conclusion is that the AI companies could be fairly valued under some circumstances, but my bet is that some of the big companies will fail miserably. There are many unknowns yet to be discovered but it is fun to speculate about the future.

# The limitations

To finalize this post let's analyze the main limitations of the current agents, show some use cases that work quite well and make some predictions for the future ahead.

The biggest limitation of current agents is visual understanding. [New benchmarks](https://arxiv.org/html/2602.02185v1#S5){:target="_blank"} have been introduced this year because previous ones were found to allow the model to solve the problems via text-shortcuts. It's surprising that these models have an [IQ higher than the average human](https://www.trackingai.org/home){:target="_blank"} but cannot understand simple images. And I can illustrate this with a very simple task that they fail miserably: cropping a powerpoint. In my job we have to do a weekly report in powerpoint and then create a word out of it. It is a very automatic thing you just have to take a screenshot of the images and copy the text separately. You basically have to go from this:

<p class="text-center"><img class="" src="{{site.baseurl}}/assets/images/vibe-coding-ii/slides.png" alt="slides" /></p>

To this:

<p class="text-center"><img class="" src="{{site.baseurl}}/assets/images/vibe-coding-ii/word.png" alt="word" /></p>

Pretty simple, right? When I tried with both Opus and Sonnet they consumed almost 20$ to achieve nothing. They cannot recognize which part of the slide is an image and which part is text and therefore the crops they did were completely incorrect. That task normally involves including the subtitle inside the image which is something they also failed to recognize. This task is so simple a five year old kid can do it. Yet our best models cannot wrap their heads around it. With a very specific MCP that has an object detection model trained specifically to recognize figures the task could be solved, however, what is the point of that? That would be terrible overengineering and I hope that models will become better at visual understanding in the future.

The next big limitation of this technology is the human factor. The maximum number of agents that I can manage is two. And I am not the only one saying so, all of my colleagues agree with me in that regard. If you try to manage three or more agents at the same time, you will end up working sequentially rather than in parallel and some agents will be idle while you work with others. The reason for this is quite simple. There are two phases: planning and execution. Planning normally takes 15 minutes and execution another 15 minutes so you can only plan one task before another has finished, thus two is the maximum number of agents you can manage in parallel. This is what METR has called the time horizon of the agent. In [their report](https://metr.org/time-horizons/){:target="_blank"} they have shown that the time horizon is increasing exponentially so I expect that this human bottleneck will be reduced once the time horizons increase. I would expect models to perform 1 hour tasks by next year, so that would mean that I can have four agents working at the same time. However, for that to work I would need to have four copies of my repository so that agents can compile in four separate branches without fighting each other. Many changes will be needed in the way we work to adapt to this new reality.

Another limitation of these models is their memory. In the current formulation memory is just the context window enhanced by some MCP or skill that looks for memories in a database. If implemented correctly that could go very far but in its current state it is very primitive. Whatever is not included in the system prompt is rarely remembered. This handicaps the model and makes it more expensive. Many times have I found myself asking a question to the model only for it to start creating loads of subagents to explore the codebase for the umpteenth time. In expert fields there are terms that are specific to the project at hand. If the model needs to look for them every single time it is very costly. For me this looks like a simple problem, just create some glossary and when prompted with something the model does not understand look at the glossary instead of exploring everything. Current models look very static to me. For them to be considered real AGI they need to learn automatically. And having a dynamic memory that updates along the way and has efficient retrieval is the main obstacle right now to achieve AGI.

Nevertheless, there are a few coding tasks that agents can done fully autonomous with little to no supervision. They can be used to reduce technical debt in three ways:

* Increasing code coverage.
* Reducing cyclomatic complexity.
* Improving code quality with static tools.

Those three things can be measured and verified without human intervention. For instance, in C++ there is this thing called [cppcheck](https://cppcheck.sourceforge.io/){:target="_blank"} that allows to prevent common mistakes. By connecting the agent to the tool it can loop until it passes the test. Same goes for tests and complexity. Those are measurable and verifiable metrics that the agent can loop until achieving a target level of performance. Human intervention is still required to check the tests make sense but in my experience it works fine for simple unit tests and it is very rare to find the agent trying to perform a shortcut. For legacy codebases this can help reduce technical debt although it won't fix a bad architecture.

The previous examples can also end up in the absurd if taken to the limit. Using a bot to check for styling guidelines is overkill. Agents should not substitute linters. The same way they should not substitute compilers. We need to be thoughtful where we apply this technology.

# Conclusion

What a ride, right? In a year we have gone from laughing at Dario Amodei for their claims that nobody would be coding manually in six months, to actually not coding manually anymore. Our linear minds cannot comprehend exponential development but luckily for us we have data at our disposal to have our feet in the ground. Given current pace of development I predict that all the limitations I mentioned here will be solved before the end of 2027. On the other side, I also predict that AI adoption outside of software will remain as limited as it is today, maybe only slightly more. The roadmap seems to be improving vision capabilities, then improving memory, then world model reasoning and then increase agentic capabilities in the real world. It is difficult to see how long would the world model reasoning and real world capabilities take so I will just keep my prediction to the next year and we will see if I was pessimistic or optimistic. On the economic side I won't expect any productivity gains above 40%. We have gone from 14% to 25% in one year, so a linear monkey prediction would put the bar at 36% next year. I will also refrain myself from predicting any outcome about the valuations since that is outside of my expertise and a risky bet. My analysis was some fun experiment but as I mentioned before, many unknowns are there to be discovered yet.

Finally, given the pace of development one could wonder how to stay updated. My advice is to be patient and wait. I didn't try Claude Code when it was released, I didn't read about MCPs until the standard was stablished, I only read the reports and articles months later and I am normally not constantly following the news. Trying to be at the very edge of knowledge and technology requires a dedication that is simply not worth it. But waiting a few months for the technology to be stablished and battle-tested is not that much of a delay. This is the 80/20 rule as usual. Dedicating a little of your attention from time to time to the topic is more than enough to keep up. Maybe reading my articles every year is enough for you. Just don't become obsessed with the topic. AI psychosis is becoming a real thing and I think we need to balance touching grass with being informed and well-educated. I hope you liked my post about the topic and I will see you next year with more down-to-earth analysis.