6 2 0 2 l u J 7 ] Y C . s c [ 1 v 8 0 8 5 0 . 7 0 6 2 : v i X r a

# Say What? Examining Text and Voice Input Modalities for Prompt-Based Programming in Computing Education

Kaitlin Riegel

University of Auckland Auckland, New Zealand kaitlin.riegel@auckland.ac.nz

Victor-Alexandru Pădurean MPI-SWS Saarbrücken, Germany vpadurea@mpi-sws.org

Yan Cathy Hua

University of Auckland Auckland, New Zealand yhua219@aucklanduni.ac.nz

Juho Leinonen Aalto University Espoo, Finland juho.2.leinonen@aalto.fi

Paul Denny

University of Auckland Auckland, New Zealand paul@cs.auckland.ac.nz

James Prather Abilene Christian University Abilene, TX, USA james.prather@acu.edu

Adish Singla MPI-SWS Saarbrücken, Germany adishs@mpi-sws.org

# Abstract

# CCS Concepts

Large language models (LLMs) are increasingly integrated into computing education, yet nearly all prior research has focused on text-based interactions. As voice-enabled interfaces become more capable and more common, there is growing interest in understand- ing how voice input might shape students’ use of LLM-powered tools. In this exploratory study, we investigated how introductory programming students interact with Prompt Problems, which are programming tasks that require crafting natural-language prompts to generate correct code. Students (N = 919) solved a series of Prompt Problems with the freedom to select or switch between text and voice input modalities. We collected their prompt submissions as well as post-activity survey responses, then analysed differences in prompt accuracy, persistence, and perspectives by modality. For two of the three problems, we found that students who typed their prompts using text were more likely to have those prompts suc- ceed on the first attempt than students who submitted unedited voice prompts. There was no difference in success rate if students edited their transcribed voice prompts before submission. Across the problems, we found evidence that students who tried voice prompting varied in their usage of modality – perhaps indicating a complementary, or non-preferential approach. However, most students only tried and reported preferring text. Our qualitative analysis revealed how students’ perceived the roles of voice and text input in shaping their problem-solving process, as well as the reported drawbacks and advantages of each modality. We discuss implications for future multimodal tools and instructional design in computing education.

ITiCSE 2026, Madrid, Spain

© 2026 Copyright held by the owner/author(s).

This is the author’s version of the work. It is posted here for your personal use. Not for redistribution. The definitive Version of Record was published in Proceedings of the 31st ACM Conference on Innovation and Technology in Computer Science Education V. 1 (ITiCSE 2026), July 10–15, 2026, Madrid, Spain, https://doi.org/10.1145/3803400.3809397.

• Social and professional topics → Computing education.

# Keywords

Natural language programming; Code-generating AI; Prompt prob- lems; Voice-enabled prompting; Student perceptions

# ACM Reference Format:

Kaitlin Riegel, Yan Cathy Hua, Paul Denny, Victor-Alexandru Pădurean, Juho Leinonen, James Prather, and Adish Singla. 2026. Say What? Exam- ining Text and Voice Input Modalities for Prompt-Based Programming in Computing Education. In Proceedings of the 31st ACM Conference on Inno- vation and Technology in Computer Science Education V. 1 (ITiCSE 2026), July 10–15, 2026, Madrid, Spain. ACM, New York, NY, USA, 7 pages. https: //doi.org/10.1145/3803400.3809397

# 1 Introduction

Voice-based assistants have become increasingly capable, evolving from simple command tools to conversational systems that can understand context and support a wide range of tasks [11]. Modern LLM-powered voice interfaces provide flexible, natural interactions [7, 21], and research in education shows that voice-based tools can increase motivation and emotional engagement compared to text-based systems [23]. There is also emerging evidence that voice input may reduce cognitive load in certain programming contexts [2]. These developments suggest that voice interaction may offer benefits across a range of activities in computing education.

LLM-powered digital teaching assistants have now been widely explored as a way to provide students with timely help and guid- ance. These tools are used to clarify concepts, debug code, and work through problem-solving steps, and students appreciate their on-demand support and configurable guardrails [6, 36]. Other LLM- based programming assistants further support comprehension, er- ror diagnosis, and task completion [13, 17, 20, 28, 29]. Despite this progress, nearly all existing work in computing education has fo- cused on text-based interactions. Research on programming assis- tants and question–answering tools has overwhelmingly examined

ITiCSE 2026, July 10–15, 2026, Madrid, Spain

typed prompts [13, 17, 19, 20, 29, 36]. Only recently has the field begun to explore voice-based interaction. Jacobs and Kiesler [10] studied a real-time voice-enabled GenAI tutor and found that, while voice input can offer hands-free, accessible interaction, it also intro- duces challenges – in particular, poor verbalisation of code. These results suggest voice-based interaction may be well suited to con- versational or conceptual tasks, but activities requiring precise expression of code elements are more problematic.

A natural next step, then, is to examine voice-based interac- tion in programming activities that focus on natural language rather than code syntax. In a Prompt Problem [5], students cre- ate a natural-language prompt designed to make an LLM generate correct code for a small computational task. Because students ex- press their problem-solving approach directly through language, these tasks offer a clear way to compare how input modalities might influence prompt effectiveness. To date, all existing work on Prompt Problems has used only typed input [5, 14, 26, 30, 32]

As voice interfaces become more commonly used, it is important to understand how they may shape students’ engagement with programming tasks. Voice may change the process of problem solvingandstudentsmayhavedifferentreasonsforpreferringwhen and how to use voice or text input. We therefore take an exploratory approach, examining how students use voice and text, how these choices relate to prompting outcomes, and how students experience each input mode. We investigated a series of Prompt Problems, where students were free to choose their preferred input mode. We collected information on the accuracy and usage of prompting by modality and surveyed the students about their choices and perspectives. Our study is guided by three research questions:

- RQ1: To what extent does the accuracy of initial prompts submit- ted using each modality differ?

- RQ2: To what extent do students persist in the use of voice prompt- ing, where attempted?

- RQ3: How do students’ perceptions of each prompting modality differ?

# 2 Related Work

Prompt Problems are a natural language programming task where the learner is presented with a visual problem description and their task is to write a prompt for an AI model to generate the code to solve the problem [5]. The generated code can be run against instructor-defined unit tests to evaluate correctness. Several plat- forms now support Prompt Problems for classroom use, e.g., [4, 32]. Evaluations of Prompt Problems have found that students enjoy solving them [5], that performance demonstrates a weak correla- tion with code writing (suggesting these possibly target distinct skills) [14], and that Prompt Problems can support multilingual teaching, as they can be solved in students’ native languages [30].

All prior work on Prompt Problems has used text as the input modality. However, speech can be up to three times faster than typing as an input modality for text entry on mobile devices [34], suggesting improved usability. Rzepka et al. [35] argue that speech is more natural and intuitive as an input modality compared to text. They found participants using speech input for an information search task reported higher perceived efficiency, lower cognitive

Kaitlin Riegel et al.

effort, higher enjoyment, and higher service satisfaction, but re- sults were dependent on the task’s goal-directness. In the context of educational robots, Mele et al. [23] found that voice modality enhanced emotional and cognitive engagement for students, and improved concentration and emotional connection, while the text modality was preferred for supporting review of content. Thus, they argue that the modalities can be complementary and have dif- ferent benefits depending on the task. Korkmaz et al. [15] evaluated both voice and text modality as input and output using a 2x2 study design, where each participant experienced all four combinations of input-output modality pairs. They found that participants preferred usability over efficiency. For example, their results suggested that voice input and text output can be very efficient but less preferred, due to lower perceived user experience. Based on their results, the greatest preference was for the text input and output combination, due to giving users a high degree of control and freedom.

In a programming context, Chandu et al. [2] found a voice- controlled programming assistant reduced reported typing fatigue and helped debugging. Jacobs and Kiesler [10] had ninth grade stu- dents use a voice-controlled AI. They similarly found that students mostly used the AI for debugging and perceived it as competent, even though incorrect feedback was given ∼30% of the time. They also found a major problem was poor verbalisation of programming constructs in the voice modality, sometimes leading to incorrect or nonsensical outputs. To the best of our knowledge, Jacobs and Kiesler present the only study in programming education that exam- ines voice as an input modality for generative AI–based assistance. Our work complements this prior study by examining voice as an input modality for Prompt Problems and analysing how students’ modality choices relate to outcomes and perceptions.

# 3 Methods

Platform. Our study employed the publicly available Prompt Pro- gramming web platform [32] (see Figure 1). The problems we used were selected from the library of problems available on the platform, and we collected interaction logs, which were anonymised prior to analysis. When working on the problems, students could submit prompts either by typing or by recording speech via an in-browser microphone control. Voice recordings were transcribed via the Ope- nAI API using whisper-1, powered by the open-source Whisper V2 model [24, 25]; prior work reports English benchmark word error rates below 5% [33]. The transcription request did not include a domain-specific prompt indicating that computing-related termi- nology should be expected. The resulting transcript was shown in the message box before submission, and students could either send it as-is (unedited voice) or edit it before sending (edited voice). The GPT-4o-mini model was used to support the chat assistant, with a system prompt directing it to return only task-relevant code in the requested language and format, without extraneous boilerplate. Interaction logs contained the sent messages, the transcribed voice recordings, the model responses, and code execution results.

Course context and tasks. The study was run in an introductory C programming course at the University of Auckland in Semester Two of 2025 and data analysis was approved by the University’s Human Participants Ethics Committee (#25279). On one of the weeklylabs,weconfiguredfourproblemsontheplatform:summing

Say What? Examining Text and Voice Input Modalities

ITiCSE 2026, July 10–15, 2026, Madrid, Spain

Prompt P3 Programming 2 © Reset In this exercise, you will design a function o Write a function foo that returns the index of the last 0 int foo(int array[], int size) Basic Functions Warmup After carefully looking at the provided specifications, write your prompts to interact with 7 Edit P1 the Al model and guide it to generate a correct program. int foo(int arr(], int size) { QP2 for (int i = size 11 = 1-) { if (arr[i] == 0) { O [15 31 0 return 1; T return -1; T [15 31 & 77 o 1 [1 7] anonymous 2 b [e 28 Dashboard @ Log out 00

Figure 1: The Prompt Programming platform: the Prompt Problem (left), including the required function signature and visual input-output examples, and the chat pane and highlighted code snippets (right), with controls to edit and run code against tests.

two given arguments (warm-up); counting negative values in a given array (P1); summing even values in a given array (P2); and returning the index of the last zero in a given array (P3). Following thetasks,studentsrespondedtotworeflections:“Whatcombination of‘voice’inputand‘text’inputdidyoufindwasmosteffectivewhen working on the problems?” (options: Voice input only, Mostly voice input, with a little text input, An equal mix of voice and text input, Mostly text input, with a little voice input, and Text input only); and “Pleasecommentonyourexperienceusingthedifferentinputmodes (‘voice’ input and ‘text’ input) to solve these ‘prompt programming’ tasks”. 1038 students were enrolled in the course. 52 did not engage with the lab or the reflections and 55 engaged after the deadline, so were excluded from the analysis. 13 students did not engage in any prompting and were also excluded. Five students only attempted the warm-up.

Prompt analysis. Binary logistic regressions were conducted across P1-3 to examine the effect of initial prompt method (unedited voice, edited voice, or text) on immediate success (i.e., if the code gen- erated in the first model response succeeded), where 0 = failure and 1 = success. The model was estimated using maximum likelihood, and model significance was assessed with the likelihood-ratio om- nibus test. Individual predictor effects were evaluated using Wald 𝜒2 statistics. As this study is exploratory, uncorrected p values are reported. For students who attempted both prompting approaches, a generalised linear mixed model was employed to examine the influence of students’ previous input choice on their next choice (including the warm-up problem). A binomial distribution with a logit link function was specified. The model included fixed effects for previous choice and a random intercept for each participant.

Reflection question analysis. To analyse responses from students to the open-ended question, we adopted a multi-label classification

approach that assigns zero or more predefined category and senti- ment labels to each response text entry. We obtained the category labels using a combination of AI and manual processes. We used two pre-trained LLMs (Gemini 3.0 Pro1 and GPT-52) to summarise key topics from all response text entries as the initial category la- bels. We then iteratively repeated the following steps to refine the labels: 1) manually review and modify the labels to align with our research focus; 2) use the LLM to assign the labels to each entry; 3) review the label assignments and the distribution of entries across labels to evaluate category independence and fit for the data; and 4) manually update the labels to begin the next iteration.

To assign category and sentiment labels to each text entry, we leveraged the Aspect-based Sentiment Analysis (ABSA) method, which extracts all text segments relevant to the provided categories and assigns category and sentiment labels to each extracted seg- ment [8, 18]. For example, “I like using the text input most, because I can control it very easy" extracted aspect “text input" with opinion “can control it very easy," and was assigned category Input Accuracy andControl (Text) with apositive sentiment. Tospeedup theprocess, we performed the initial segment extraction and label assignment using a custom prompt with an ABSA-fine-tuned small LLM from Hua et al. [9]3, which showed better opinion extraction spans on a small pilot dataset compared to pre-trained LLMs. Two human annotators then independently re-annotated 250 randomly selected review entries from the LLM output file. Within the 250 human- annotated entries, the first 94 were used as a pilot to develop the annotation rules through the difference-resolution process, and the independent annotations of the remaining 156 entries were used

1https://deepmind.google/models/gemini/pro/, accessed via an institutional licence

2https://openai.com/index/introducing-gpt-5/, accessed via Microsoft Copilot with institutional licence

3We used the Phi4-mini version from https://huggingface.co/yhua219/EduRABSA_ SLM_v1_SLERP_phi4mini

ITiCSE 2026, July 10–15, 2026, Madrid, Spain

to calculate the inter-rater reliability. Inter-rater agreement was moderate (micro-averaged F1 = 0.65), reflecting the interpretive and multi-label nature of the task. Disagreements were subsequently resolved through discussion to produce a consensus-coded dataset for all 250 entries used for all further analyses. Together, the two researchers spent approximately 45 combined hours on the anal- ysis. For the purposes of this paper, we focus on the categories specifically reflecting on the input modalities.

# 4 Results

# 4.1 Initial Prompt Success by Initial Modality (RQ1)

Table 1 presents descriptive statistics by problem and input modal- ity (i.e., unedited voice, edited voice, and text). We employed binary logistic regression models across each of the three problems to ex- amine how the different approaches to constructing initial prompts influenced students’ immediate success. For both P1 and P2, the overall models were significant (𝜒2 𝑃1 = 7.405, p = .025; 𝜒2 𝑃2 = 7.158, p = .028). Compared to text prompting, students who initially used unedited voice prompting had lower odds of immediate success (OR𝑃1 = 0.50, 95% CI [0.27, 0.89], p = 0.02; OR𝑃2 = 0.43, 95% CI [0.23, 0.83], p = 0.01), while students who edited their voice prompts did not significantly differ (OR𝑃1 = 0.57, 95% CI [0.26, 1.27], p = 0.17; OR𝑃2 = 0.72, 95% CI [0.35, 1.49], p = 0.38). In P3, the model was not significant, 𝜒2 = 1.948, p = .378, indicating initial prompting method did not explain immediate success. Together, the results suggest the possibility that students who edit their voice prompts are as likely to succeed as students using text. However, unedited voice prompting may be unreliable.

# 4.2 Persistence of Voice Prompting (RQ2)

Including the warm-up problem, there were 813 students who only used text-based prompting (88.5%), 44 who only used voice (4.8%), and 62 who attempted both input methods (6.7%), demonstrating an overwhelming bias towards text prompting. However, we were interested in the influence of the novel voice input on students’ behaviours. Consequently, for the 62 students who attempted both prompt approaches, a binary, mixed-effects logistic regression was conducted to examine whether previous prompt modality influ- enced subsequent modality selection. The effect was not statisti- cally significant (OR = 1.28, 95% CI [0.71, 2.31], p = 0.41), indicating that, for this subset, students’ choices were independent of their previous choices. In addition to the 44 students who used voice and continued to only use voice for their initial prompts, the absence of a significant effect of voice prompting on subsequent modality use suggests that students are not deterred by voice-based interactions. A possible interpretation is that students flexibly combine voice and text prompting according to their needs.

We sought to examine the persistence of using voice prompts withinproblems,however,asmanystudentsimmediatelysucceeded on the problems, we did not attain sufficient sample sizes. For the small subsets who initially engaged with voice prompting and did not experience immediate success, we found there were some who continued using voice prompting within the problem. No strong conclusions can be drawn, but the results could hint that some students engage with voice prompting in a dialogue-based capacity.

Kaitlin Riegel et al.

Text input only 719 Mostly text input, with a little voice input 101 An equal mix of voice and text input 29 Mostly voice input, with a little text input 48 Voice input only 16 0 100 200 300 400 500 600 700 800 Number of Students

Figure 2: Student input modality preferences.

# 4.3 Students’ Perceptions of Prompting Modalities (RQ3)

Figure 2 summarises responses to the reflection question on mode preference and reveals students overwhelmingly preferred only text. However, the log data showed few opted to attempt using voice input. For this reason, we found it appropriate to examine the relationship between the proportional usage of the other modalities (edited voice and unedited voice) with reported preference (measured on a five-point scale). A Spearman rank-order correlation was con- ducted between preference (“Text input only” = 1 and “Voice input only” = 5) and proportion of both edited and unedited voice prompts. In both cases, there was a moderate, positive correlation between a greater proportion of voice prompts and a greater preference for using voice (𝜌𝑒𝑑𝑖𝑡𝑒𝑑 = .509, p < .001 and 𝜌𝑢𝑛𝑒𝑑𝑖𝑡𝑒𝑑 = .597, p <.001). Consequently, we received insight that students who do engage in voice prompting are more likely to enjoy it – suggesting, again, they are not being deterred by the modality.

Table 2 presents the results of the qualitative analysis, including the category-sentiment labels, definitions, and counts. The initial LLM-proposed categories largely mapped to the final Text/Voice- specific categories with rewording (e.g., “Code-Specific Suitabil- ity” to “Technical Expressions & Syntax”). From examining the pilot comments, we further added two higher-level categories, “AI/Activity” and “Problem Solving,” each with subcategories, and two input-modality categories, “Familiarity & User Confidence” and “Personal Factor”, to capture the themes. We discuss and provide student excerpts representing the dominant categories.

4.3.1 Input Accuracy and Control. The dominant category that emerged was the ability to input prompts with control and ac- curacy, heavily in favour of text-based prompting. One student explained, “I find using text input to be my preferred method as I know that whatever I write is exactly what will be passed onto the computer, as with voice it is possible for it to misunderstand what I am saying.” Many students cited transcription errors as an issue, includ- ing non-native English speakers (NNES). We conducted a post-hoc analysis on all 890 comment pieces to identify those with explicit mention of NNES status. Using a combination of keyword search, LLM categorisation (pre-trained Qwen3.5-4B in non-thinking mode [38]), and human consolidation, we identified 17 entries that explic- itly mentioned NNES status as a reason for preferring text input.

Say What? Examining Text and Voice Input Modalities

ITiCSE 2026, July 10–15, 2026, Madrid, Spain

Table 1: Descriptive statistics by problem and modality.

M (SD) Input modality N (attempt) N (success) Proportion Immediate Success Messages until Success First Message Characters Unedited Voice 51 48 0.35 (0.48) 1.69 (1.60) 221.41 (107.07) P1 Edited Voice 26 25 0.38 (0.50) 1.56 (0.96) 205.00 (113.90) Text 830 824 0.52 (0.50) 1.71 (1.89) 183.17 (96.47) Total N = 907 Unedited Voice 40 39 0.38 (0.49) 1.67 (1.16) 206.15 (100.23) P2 Edited Voice 30 30 0.50 (0.51) 1.23 (0.43) 197.07 (76.33) Text 831 829 0.58 (0.49) 1.53 (1.35) 193.41 (100.28) Total N = 901 Unedited Voice 35 34 0.31 (0.47) 2.15 (2.16) 272.80 (107.31) P3 Edited Voice 35 33 0.26 (0.44) 2.76 (2.96) 271.52 (186.95) Text 830 816 0.36 (0.48) 2.47 (2.78) 226.62 (118.82) Total N = 900

Table 2: Category labels and definitions with respect to prompt input modality. Counts for Positive, Neutral, and Negative sentiments within each category represented in the bars as green, grey, and red, respectively.

Category Label Definition Text Input Voice Input Affective Response Sentiment of the input mode with no further details 33/3/0 Ease of Use How easy or hard it is to use the input mode 26/0/1 Efficiency & Speed Speed of input mode execution or the overall process involving 13/0/5 the input mode Planning & Thinking Process How the input mode facilitates or hinders the user’s ability to 44/0/1 think, plan, structure thoughts, or manage cognitive load Editability & Refinement The ability to review or edit the prompt after drafting but before 47/0/2 execution Technical Expressions & Syn- Relating to using the input mode for programming / technical 5/0/1 tax tasks Input Accuracy & Control Relating to the accuracy of transcription errors, input precision, 53/0/2 or the user’s ability to input prompts precisely and with control Familiarity & User Confidence User familiarity and/or confidence in using a particular input mode 6/1/0 Environment External factors affecting the choice or experience, (e.g., noise 2/0/0 levels or social etiquette) Hardware Requirements Hardware or software limitations (e.g., broken microphone) 2/0/0 Personal Factor Individual constraints or preferences (e.g., language barriers, ac- 10/2/0 cessibility issues, or specific personal situations) Voice - Superfluous General opinion that the voice input mode is unnecessary, since n/a n = 17 the tasks can be solved with text. Combining Input Modes Opinions about using both input modes for different aspects of 11/6/1 the task 11/1/12 7/0/2 16/2/6 6/3/17 0/0/12 0/0/3 6/3/51 2/1/0 0/0/20 0/0/18 1/0/7

15 of these comments expressed concerns about their accent be- ing accurately recognised. The other two mentioned uncertainty about voice recognition picking up their native language and time pressure in constructing voice commands in English.

4.3.2 Editability and Refinement. The ability to edit and review text prompts before submitting was a major reported advantage. Specifically, “When you talk you can make mistakes and you’d have to rerecord the entire audio message if you want to redo it. With typing you can simply backspace.” This was an important category because voice-based revision was perceived strictly negatively. Further, the students felt if text-based editing was necessary, they should simply use text for the whole prompting process.

4.3.3 Planning and Thinking Process. A noteworthy finding is the ways the different input methods shape the reported problem- solving process, affecting students’ usage decisions. Students fre- quently referenced the opportunity to structure cohesive thoughts or the ability to engage in non-linear problem-solving using text inputs, exemplified by comments such as, “Text input allowed me to better collect my thoughts” and ‘I prefer using the text input because I can fully formulate and think through my prompt before actually sub- mitting it”. One student summarises the conflict between the input methods’ influence on their ability to think and plan as follows:

I am not bottlenecked by my typing speed, but rather, my thought speed...when using voice, I have to think about what

ITiCSE 2026, July 10–15, 2026, Madrid, Spain

to say beforehand, otherwise I will give the AI a confusing and poorly structured prompt...typing things out, I can think on the fly, and edit previous parts of my sentence to refine the prompt. If I am using voice input, then I either have to spend time thinking about what to say, or spend time editing the prompt I gave the AI – time better spent typing out the prompt.

In contrast, some students thought voice input served a valuable role in their prompt construction – often to get initial ideas out: “Voice input was a lot easier to get down what I was thinking into words as when I was speaking to the program I tended to think more about what the code needed to do than when I wrote it myself.”

4.3.4 Other Categories. General Sentiment and Ease of Use were much more positive for text input. Further, the Voice - Superfluous category indicated many students default to text and may avoid novelty if traditional methods meet their needs. These results align with students’ usage and preferences. However, the analysis high- lighted many avoid voice input for practical reasons, specifically, being in an inappropriate environment (“Speaking to the AI through audio can be especially bad if there is background noise”, or simply lacking the hardware (“My laptop doesn’t have a microphone.”).

Interestingly, there was a fairly even distribution for students positively perceiving the efficiency and speed of each input method. One wrote “I only used text input, because realistically, it is easier and faster to type out whatever I want to say than dictate, then wait for the programme to transcribe it.” In contrast, another commented, “The voice input tended to be much faster than writing out all the text...I find that voice is much better than writing it, especially if you have a lot to write.” Finally, some students discussed the interwoven roles of each input modality and how a combination may be the best approach. For example, one stated, “I liked starting with voice for the rough idea and then switching to text to clean it up.” Another commented on the differing contexts in which the modalities are appropriate: “I used only text input which worked well for these more simpleandshortcodes.Iwouldbemoreinclinedtousevoiceprompting for more complicated coding tasks.”

# 5 Discussion

This study examined students’ success, persistence, and percep- tions when solving Prompt Problems using voice versus text inputs. Critically, voice engagement did not reduce student preference or use. For those who initially used voice prompts, input modality failing to predict subsequent choices may be due to strategically combining use of text and voice, consistent with prior work [23].

There was a heavy skew toward students’ engagement with and preference for text input, mirroring Zavaleta Bernuy et al. [39], who found students preferred text over voice as a medium for self- explanations. Our findings appear driven not only by practical barri- ers (e.g., hardware, environment), but also by low perceived control [27] (e.g., Voice - Superfluous, Text - Familiarity & User Confidence) and concerns the negative perception of Input Control and Accu- racy, aligning with Korkmaz et al. [15]. Future work should improve voice usability, to support student control over success, through bet- ter hardware, appropriate environments, native language options [14, 30], explicit instruction, and adaptive transcription.

Although students were more likely to experience immediate success using text prompts than unedited voice prompts, this may

Kaitlin Riegel et al.

not reflect better learning. Over-reliance on AI tools may cause cognitive functioning to deteriorate [16], as well as weaker articu- lation of solutions [12, 31], poorer outcomes [22], and diminished metacognition and self-regulation [31] in programming education. Thus, faster success may come at the cost of deeper understanding and this could potentially be counteracted using a voice prompting technique.

Moreover, it is critical to evaluate how modality shapes engage- ment. Students preferred text for its non-linear, iterative planning (Planning & Thinking Process), but this may reduce retention. In- formation is moved out of the working memory once it is written down [37]. Consequently, students can succeed on a task, while focusing only on a single aspect of the problem for a fleeting mo- ment (or with heuristic iterative adjustments) without it sinking into their long-term memory, failing to cause learning. In contrast, voice-based prompting represents all the benefits of speak-aloud self-explanation [1]. Notably, edited voice prompting achieved a similar success rate to text, suggesting voice and text may combine effectiveness with deeper cognitive processing and warrant further investigation.

# 6 Limitations and Future Work

A key limitation is students’ self-selection into modality, with few students choosing voice, limiting generalisability of the results and motivating a controlled study. Additionally, causality cannot be established (i.e., whether modality influences outcomes, or student characteristics drive modality choice). Some students, including non-native English speakers, reported transcription issues, suggest- ing evaluations may reflect technology performance rather than modality. Future studies should examine outcomes when students can voice prompt in their native language. Transcription delay was not measured and may have influenced student behaviour and per- ceptions. Possible future avenues for this research could include the use of validated surveys measuring technology acceptance [3] and monitoring how students interact with LLMs in non-programming tasks.Thetasksinthisstudywererelativelysimpleandshort,which may have not been suitable for comparing modalities. Longitudinal evaluation of retention or potential disadvantages should be ex- ploredinfutureworkwithmorecomplextasksandcorrespondingly longer voice and text prompts.

# 7 Conclusions

This exploratory study illuminated the complex trade-offs between using text and voice input modalities for prompt-based program- ming. While students showed a clear preference for text, voice input holds promise as a tool for deeper cognitive engagement and self-explanation, with the potential to support long-term learn- ing outcomes. Moreover, immediate success may not translate to meaningful understanding, as over-reliance on AI and superficial strategies can undermine metacognition and retention. Future re- search into this area should focus on better faciliting the use of voice input and examining its impact in controlled settings.

# Acknowledgments

This work was supported by Research Council of Finland grant #356114.