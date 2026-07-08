
Say What? Examining Text and Voice Input Modalities for
Prompt-Based Programming in Computing Education

# Kaitlin Riegel

# Yan Cathy Hua

# Paul Denny

# University of Auckland

# Auckland, New Zealand

# kaitlin.riegel@auckland.ac.nz

# yhua219@aucklanduni.ac.nz

# paul@cs.auckland.ac.nz

# Victor-Alexandru Pădurean

# Juho Leinonen

# James Prather

# MPI-SWS

# Saarbrücken, Germany

# vpadurea@mpi-sws.org

# Aalto University

# Espoo, Finland

# juho.2.leinonen@aalto.fi

# Abilene Christian University

# Abilene, TX, USA

# james.prather@acu.edu

# Adish Singla

# MPI-SWS

# Saarbrücken, Germany

# adishs@mpi-sws.org

arXiv:2607.05808v1 [cs.CY] 7 Jul 2026

# Abstract

Large language models (LLMs) are increasingly integrated into computing education, yet nearly all prior research has focused on text-based interactions. As voice-enabled interfaces become more capable and more common, there is growing interest in understanding how voice input might shape students’ use of LLM-powered tools. In this exploratory study, we investigated how introductory programming students interact with Prompt Problems, which are programming tasks that require crafting natural-language prompts to generate correct code. Students (N = 919) solved a series of Prompt Problems with the freedom to select or switch between text and voice input modalities. We collected their prompt submissions as well as post-activity survey responses, then analysed differences in prompt accuracy, persistence, and perspectives by modality. For two of the three problems, we found that students who typed their prompts using text were more likely to have those prompts succeed on the first attempt than students who submitted unedited voice prompts. There was no difference in success rate if students edited their transcribed voice prompts before submission. Across the problems, we found evidence that students who tried voice prompting varied in their usage of modality – perhaps indicating a complementary, or non-preferential approach. However, most students only tried and reported preferring text. Our qualitative analysis revealed how students’ perceived the roles of voice and text input in shaping their problem-solving process, as well as the reported drawbacks and advantages of each modality. We discuss implications for future multimodal tools and instructional design in computing education.

# CCS Concepts

• Social and professional topics → Computing education.

# Keywords

Natural language programming; Code-generating AI; Prompt problems; Voice-enabled prompting; Student perceptions

# ACM Reference Format:

Kaitlin Riegel, Yan Cathy Hua, Paul Denny, Victor-Alexandru Pădurean, Juho Leinonen, James Prather, and Adish Singla. 2026. Say What? Examining Text and Voice Input Modalities for Prompt-Based Programming in Computing Education. In Proceedings of the 31st ACM Conference on Innovation and Technology in Computer Science Education V. 1 (ITiCSE 2026), July 10–15, 2026, Madrid, Spain. ACM, New York, NY, USA, 7 pages. https://doi.org/10.1145/3803400.3809397

# 1 Introduction

Voice-based assistants have become increasingly capable, evolving from simple command tools to conversational systems that can understand context and support a wide range of tasks [11]. Modern LLM-powered voice interfaces provide flexible, natural interactions [7, 21], and research in education shows that voice-based tools can increase motivation and emotional engagement compared to text-based systems [23]. There is also emerging evidence that voice input may reduce cognitive load in certain programming contexts [2]. These developments suggest that voice interaction may offer benefits across a range of activities in computing education.

LLM-powered digital teaching assistants have now been widely explored as a way to provide students with timely help and guidance. These tools are used to clarify concepts, debug code, and work through problem-solving steps, and students appreciate their on-demand support and configurable guardrails [6, 36]. Other LLM-based programming assistants further support comprehension, error diagnosis, and task completion [13, 17, 20, 28, 29]. Despite this progress, nearly all existing work in computing education has focused on text-based interactions. Research on programming assistants and question–answering tools has overwhelmingly examined.

ITiCSE 2026, Madrid, Spain
© 2026 Copyright held by the owner/author(s).
This is the author’s version of the work. It is posted here for your personal use. Not for redistribution. The definitive Version of Record was published in Proceedings of the 31st ACM Conference on Innovation and Technology in Computer Science Education V. 1 (ITiCSE 2026), July 10–15, 2026, Madrid, Spain, https://doi.org/10.1145/3803400.3809397.


---

ITiCSE 2026, July 10–15, 2026, Madrid, Spain
Kaitlin Riegel et al.

typed prompts [13, 17, 19, 20, 29, 36]. Only recently has the field begun to explore voice-based interaction. Jacobs and Kiesler [10] studied a real-time voice-enabled GenAI tutor and found that, while voice input can offer hands-free, accessible interaction, it also introduces challenges – in particular, poor verbalisation of code. These results suggest voice-based interaction may be well suited to conversational or conceptual tasks, but activities requiring precise expression of code elements are more problematic.

A natural next step, then, is to examine voice-based interaction in programming activities that focus on natural language rather than code syntax. In a Prompt Problem [5], students create a natural-language prompt designed to make an LLM generate correct code for a small computational task. Because students express their problem-solving approach directly through language, these tasks offer a clear way to compare how input modalities might influence prompt effectiveness. To date, all existing work on Prompt Problems has used only typed input [5, 14, 26, 30, 32].

As voice interfaces become more commonly used, it is important to understand how they may shape students’ engagement with programming tasks. Voice may change the process of problem solving and students may have different reasons for preferring when and how to use voice or text input. We therefore take an exploratory approach, examining how students use voice and text, how these choices relate to prompting outcomes, and how students experience each input mode. We investigated a series of Prompt Problems, where students were free to choose their preferred input mode. We collected information on the accuracy and usage of prompting by modality and surveyed the students about their choices and perspectives. Our study is guided by three research questions:

# RQ1:

To what extent does the accuracy of initial prompts submitted using each modality differ?

# RQ2:

To what extent do students persist in the use of voice prompting, where attempted?

# RQ3:

How do students’ perceptions of each prompting modality differ?

# 3 Methods

# Platform.

Our study employed the publicly available Prompt Programming web platform [32] (see Figure 1). The problems we used were selected from the library of problems available on the platform, and we collected interaction logs, which were anonymised prior to analysis. When working on the problems, students could submit prompts either by typing or by recording speech via an in-browser microphone control. Voice recordings were transcribed via the penAI API using whisper-1, powered by the open-source Whisper V2 model [24, 25]; prior work reports English benchmark word error rates below 5% [33]. The transcription request did not include a domain-specific prompt indicating that computing-related terminology should be expected. The resulting transcript was shown in the message box before submission, and students could either send it as-is (unedited voice) or edit it before sending (edited voice). The GPT-4o-mini model was used to support the chat assistant, with a system prompt directing it to return only task-relevant code in the requested language and format, without extraneous boilerplate. Interaction logs contained the sent messages, the transcribed voice recordings, the model responses, and code execution results.

# Course context and tasks.

The study was run in an introductory C programming course at the University of Auckland in Semester Two of 2025 and data analysis was approved by the University’s Human Participants Ethics Committee (#25279). On one of the weekly labs, we configured four problems on the platform: summing



---

Say What? Examining Text and Voice Input Modalities
# ITiCSE 2026, July 10–15, 2026, Madrid, Spain

# Prompt P3

# Programming C Basic Functions

Section: C In this exercise, you will design a function

int foo(int array[], int size) {
for (int i = size - 1; i >= 0; i--) {
if (array[i] == 0) {
return i;
}
}
return -1; // Return -1 if 0 is not found
}

array [15, 31, 8, 77, 34] —→ 4

array [15, 31, 8, 77, 8, 17, 6] size 7

array [1, 2, 3, 4, 5, 6, 7] —→ -1

Type your message or press the record button (O) to start recording.

Press Enter to send. Use shift Enter for a new line.

# Figure 1

The Prompt Programming platform: the Prompt Problem (left), including the required function signature and visual input-output examples, and the chat pane and highlighted code snippets (right), with controls to edit and run code against tests.

two given arguments (warm-up); counting negative values in a given array (P1); summing even values in a given array (P2); and returning the index of the last zero in a given array (P3). Following the tasks, students responded to two reflections: “What combination of ‘voice’ input and ‘text’ input did you find was most effective when working on the problems?” (options: Voice input only, Mostly voice input, with a little text input, An equal mix of voice and text input, Mostly text input, with a little voice input, and Text input only); and “Please comment on your experience using the different input modes (‘voice’ input and ‘text’ input) to solve these ‘prompt programming’ tasks”. 1038 students were enrolled in the course. 52 did not engage with the lab or the reflections and 55 engaged after the deadline, so were excluded from the analysis. 13 students did not engage in any prompting and were also excluded. Five students only attempted the warm-up.

# Prompt analysis

Binary logistic regressions were conducted across P1-3 to examine the effect of initial prompt method (unedited voice, edited voice, or text) on immediate success (i.e., if the code generated in the first model response succeeded), where 0 = failure and 1 = success. The model was estimated using maximum likelihood, and model significance was assessed with the likelihood-ratio omnibus test. Individual predictor effects were evaluated using Wald statistics. As this study is exploratory, uncorrected p values are reported. For students who attempted both prompting approaches, a generalised linear mixed model was employed to examine the influence of students’ previous input choice on their next choice (including the warm-up problem). A binomial distribution with a logit link function was specified. The model included fixed effects for previous choice and a random intercept for each participant.

# Reflection question analysis

To analyse responses from students to the open-ended question, we adopted a multi-label classification approach that assigns zero or more predefined category and sentiment labels to each response text entry. We obtained the category labels using a combination of AI and manual processes. We used two pre-trained LLMs (Gemini 3.0 Pro and GPT-5) to summarise key topics from all response text entries as the initial category labels. We then iteratively repeated the following steps to refine the labels: 1) manually review and modify the labels to align with our research focus; 2) use the LLM to assign the labels to each entry; 3) review the label assignments and the distribution of entries across labels to evaluate category independence and fit for the data; and 4) manually update the labels to begin the next iteration.

To assign category and sentiment labels to each text entry, we leveraged the Aspect-based Sentiment Analysis (ABSA) method, which extracts all text segments relevant to the provided categories and assigns category and sentiment labels to each extracted segment. For example, “I like using the text input most, because I can control it very easy" extracted aspect “text input" with opinion “can control it very easy," and was assigned category Input Accuracy and Control (Text) with a positive sentiment. To speed up the process, we performed the initial segment extraction and label assignment using a custom prompt with an ABSA-fine-tuned small LLM from Hua et al., which showed better opinion extraction spans on a small pilot dataset compared to pre-trained LLMs. Two human annotators then independently re-annotated 250 randomly selected review entries from the LLM output file. Within the 250 human-annotated entries, the first 94 were used as a pilot to develop the annotation rules through the difference-resolution process, and the independent annotations of the remaining 156 entries were used.

1 https://deepmind.google/models/gemini/pro/, accessed via an institutional licence
2 https://openai.com/index/introducing-gpt-5/, accessed via Microsoft Copilot with institutional licence
3 We used the Phi4-mini version from https://huggingface.co/yhua219/EduRABSA_SLM_v1_SLERP_phi4mini



---

ITiCSE 2026, July 10–15, 2026, Madrid, Spain

Kaitlin Riegel et al.

to calculate the inter-rater reliability. Inter-rater agreement was moderate (micro-averaged F1 = 0.65), reflecting the interpretive and multi-label nature of the task. Disagreements were subsequently resolved through discussion to produce a consensus-coded dataset for all 250 entries used for all further analyses. Together, the two researchers spent approximately 45 combined hours on the analysis. For the purposes of this paper, we focus on the categories specifically reflecting on the input modalities.

# 4 Results

# 4.1 Initial Prompt Success by Initial Modality (RQ1)

Table 1 presents descriptive statistics by problem and input modality (i.e., unedited voice, edited voice, and text). We employed binary logistic regression models across each of the three problems to examine how the different approaches to constructing initial prompts influenced students’ immediate success. For both P1 and P2, the overall models were significant (χ21 = 7.405, p = .025; χ22 = 7.158, p = .028). Compared to text prompting, students who initially used unedited voice prompting had lower odds of immediate success (OR1 = 0.50, 95% CI [0.27, 0.89], p = 0.02; OR2 = 0.43, 95% CI [0.23, 0.83], p = 0.01), while students who edited their voice prompts did not significantly differ (OR1 = 0.57, 95% CI [0.26, 1.27], p = 0.17; OR2 = 0.72, 95% CI [0.35, 1.49], p = 0.38). In P3, the model was not significant, χ2 = 1.948, p = .378, indicating initial method did not explain immediate success. Together, the results suggest the possibility that students who edit their voice prompts are as likely to succeed as students using text. However, unedited voice prompting may be unreliable.

# 4.2 Persistence of Voice Prompting (RQ2)

Including the warm-up problem, there were 813 students who only used text-based prompting (88.5%), 44 who only used voice (4.8%), and 62 who attempted both input methods (6.7%), demonstrating an overwhelming bias towards text prompting. However, we were interested in the influence of the novel voice input on students’ behaviours. Consequently, for the 62 students who attempted both prompt approaches, a binary, mixed-effects logistic regression was conducted to examine whether previous prompt modality influenced subsequent modality selection. The effect was not statistically significant (OR = 1.28, 95% CI [0.71, 2.31], p = 0.41), indicating that, for this subset, students’ choices were independent of their previous choices. In addition to the 44 students who used voice and continued to only use voice for their initial prompts, the absence of a significant effect of voice prompting on subsequent modality use suggests that students are not deterred by voice-based interactions. A possible interpretation is that students flexibly combine voice and text prompting according to their needs.

We sought to examine the persistence of using voice prompts within problems, however, as many students immediately succeeded on the problems, we did not attain sufficient sample sizes. For the small subsets who initially engaged with voice prompting and did not experience immediate success, we found there were some who continued using voice prompting within the problem. No strong conclusions can be drawn, but the results could hint that some students engage with voice prompting in a dialogue-based capacity. We conducted a post-hoc analysis on all 890 comment pieces to identify those with explicit mention of NNES status. Using a combination of keyword search, LLM categorisation (pre-trained Qwen3.5-4B in non-thinking mode [38]), and human consolidation, we identified 17 entries that explicitly mentioned NNES status as a reason for preferring text input.

# 4.3 Students’ Perceptions of Prompting Modalities (RQ3)

Figure 2 summarises responses to the reflection question on mode preference and reveals students overwhelmingly preferred only text. However, the log data showed few opted to attempt using voice input. For this reason, we found it appropriate to examine the relationship between the proportional usage of the other modalities (edited voice and unedited voice) with reported preference (measured on a five-point scale). A Spearman rank-order correlation was conducted between preference (“Text input only” = 1 and “Voice input only” = 5) and proportion of both edited and unedited voice prompts. In both cases, there was a moderate, positive correlation between a greater proportion of voice prompts and a greater preference for using voice (ρ = .509, p &#x3C; .001 and ρ = .597, p &#x3C; .001).

# 4.3.1 Input Accuracy and Control

The dominant category that emerged was the ability to input prompts with control and accuracy, heavily in favour of text-based prompting. One student explained, “I find using text input to be my preferred method as I know that whatever I write is exactly what will be passed onto the computer, as with voice it is possible for it to misunderstand what I am saying.” Many students cited transcription errors as an issue, including non-native English speakers (NNES).

| Category-Sentiment Labels      | Definitions | Counts |
| ------------------------------ | ----------- | ------ |
| Technical Expressions & Syntax |             |        |
| AI/Activity                    |             |        |
| Problem Solving                |             |        |
| Familiarity & User Confidence  |             |        |
| Personal Factor                |             |        |



---

Say What? Examining Text and Voice Input Modalities
# ITiCSE 2026, July 10–15, 2026, Madrid, Spain

# Table 1: Descriptive statistics by problem and modality.

|                 | Input modality | N (attempt) | N (success) | Proportion  | Immediate Success | Messages until Success | First Message Characters |   |   |   |   |   |
| --------------- | -------------- | ----------- | ----------- | ----------- | ----------------- | ---------------------- | ------------------------ | - | - | - | - | - |
| Unedited Voice  | 51             | 48          | 0.35 (0.48) | 1.69 (1.60) | 221.41 (107.07)   |                        |                          |   |   |   |   |   |
| P1 Edited Voice | 26             | 25          | 0.38 (0.50) | 1.56 (0.96) | 205.00 (113.90)   |                        |                          |   |   |   |   |   |
| Text            | 830            | 824         | 0.52 (0.50) | 1.71 (1.89) | 183.17 (96.47)    |                        |                          |   |   |   |   |   |
| Total N = 907   |                |             |             |             |                   |                        |                          |   |   |   |   |   |
| Unedited Voice  | 40             | 39          | 0.38 (0.49) | 1.67 (1.16) | 206.15 (100.23)   |                        |                          |   |   |   |   |   |
| P2 Edited Voice | 30             | 30          | 0.50 (0.51) | 1.23 (0.43) | 197.07 (76.33)    |                        |                          |   |   |   |   |   |
| Text            | 831            | 829         | 0.58 (0.49) | 1.53 (1.35) | 193.41 (100.28)   |                        |                          |   |   |   |   |   |
| Total N = 901   |                |             |             |             |                   |                        |                          |   |   |   |   |   |
| Unedited Voice  | 35             | 34          | 0.31 (0.47) | 2.15 (2.16) | 272.80 (107.31)   |                        |                          |   |   |   |   |   |
| P3 Edited Voice | 35             | 33          | 0.26 (0.44) | 2.76 (2.96) | 271.52 (186.95)   |                        |                          |   |   |   |   |   |
| Text            | 830            | 816         | 0.36 (0.48) | 2.47 (2.78) | 226.62 (118.82)   |                        |                          |   |   |   |   |   |
| Total N = 900   |                |             |             |             |                   |                        |                          |   |   |   |   |   |

# Table 2: Category labels and definitions with respect to prompt input modality.

| Category Label                 | Definition                                                                                                                           | Text Input | Voice Input |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ | ---------- | ----------- |
| Affective Response             | Sentiment of the input mode with no further details                                                                                  | 33/3/0     | 11/1/12     |
| Ease of Use                    | How easy or hard it is to use the input mode                                                                                         | 26/0/1     | 7/0/2       |
| Efficiency & Speed             | Speed of input mode execution or the overall process involving                                                                       | 13/0/5     | 16/2/6      |
| Planning & Thinking Process    | How the input mode facilitates or hinders the user’s ability to think, plan, structure thoughts, or manage cognitive load            | 44/0/1     | 6/3/17      |
| Editability & Refinement       | The ability to review or edit the prompt after drafting but before execution                                                         | 47/0/2     | 0/0/12      |
| Technical Expressions & Syntax | Relating to using the input mode for programming / technical tasks                                                                   | 5/0/1      | 0/0/3       |
| Input Accuracy & Control       | Relating to the accuracy of transcription errors, input precision, or the user’s ability to input prompts precisely and with control | 53/0/2     | 6/3/51      |
| Familiarity & User Confidence  | User familiarity and/or confidence in using a particular input mode                                                                  | 6/1/0      | 2/1/0       |
| Environment                    | External factors affecting the choice or experience, (e.g., noise levels or social etiquette)                                        | 2/0/0      | 0/0/20      |
| Hardware Requirements          | Hardware or software limitations (e.g., broken microphone)                                                                           | 2/0/0      | 0/0/18      |
| Personal Factor                | Individual constraints or preferences (e.g., language barriers, accessibility issues, or specific personal situations)               | 10/2/0     | 1/0/7       |
| Voice - Superfluous            | General opinion that the voice input mode is unnecessary, since the tasks can be solved with text.                                   | n/a        | n = 17      |
| Combining Input Modes          | Opinions about using both input modes for different aspects of the task                                                              |            | 11/6/1      |

# 4.3.3 Planning and Thinking Process.

A noteworthy finding is the ways the different input methods shape the reported problem-solving process, affecting students’ usage decisions. Students frequently referenced the opportunity to structure cohesive thoughts.

# 4.3.2 Editability and Refinement.

The ability to edit and review text prompts before submitting was a major reported advantage. Specifically, “When you talk you can make mistakes and you’d have to rerecord the entire audio message if you want to redo it. With typing you can simply backspace.” This was an important category because voice-based revision was perceived strictly negatively. Further, the students felt if text-based editing was necessary, they should simply use text for the whole prompting process. I am not bottlenecked by my typing speed, but rather, my thought speed...when using voice, I have to think about what.



---

ITiCSE 2026, July 10–15, 2026, Madrid, Spain
Kaitlin Riegel et al.

to say beforehand, otherwise I will give the AI a confusing and not reflect better learning. Over-reliance on AI tools may cause cognitive functioning to deteriorate [16], as well as weaker articulation of solutions [12, 31], poorer outcomes [22], and diminished metacognition and self-regulation [31] in programming education. Thus, faster success may come at the cost of deeper understanding and this could potentially be counteracted using a voice prompting technique.

In contrast, some students thought voice input served a valuable role in their prompt construction – often to get initial ideas out: “Voice input was a lot easier to get down what I was thinking into words as when I was speaking to the program I tended to think more about what the code needed to do than when I wrote it myself.”

# 4.3.4 Other Categories

General Sentiment and Ease of Use were much more positive for text input. Further, the Voice - Superfluous category indicated many students default to text and may avoid novelty if traditional methods meet their needs. These results align with students’ usage and preferences. However, the analysis highlighted many avoid voice input for practical reasons, specifically, being in an inappropriate environment (“Speaking to the AI through audio can be especially bad if there is background noise”, or simply lacking the hardware (“My laptop doesn’t have a microphone.”).

Interestingly, there was a fairly even distribution for students positively perceiving the efficiency and speed of each input method. One wrote “I only used text input, because realistically, it is easier and faster to type out whatever I want to say than dictate, then wait for the programme to transcribe it.” In contrast, another commented, “The voice input tended to be much faster than writing out all the text...I find that voice is much better than writing it, especially if you have a lot to write.” Finally, some students discussed the interwoven roles of each input modality and how a combination may be the best approach. For example, one stated, “I liked starting with voice for the rough idea and then switching to text to clean it up.” Another commented on the differing contexts in which the modalities are appropriate: “I used only text input which worked well for these more simple and short codes. I would be more inclined to use voice prompting for more complicated coding tasks.”

# 6 Limitations and Future Work

A key limitation is students’ self-selection into modality, with few students choosing voice, limiting generalisability of the results and motivating a controlled study. Additionally, causality cannot be established (i.e., whether modality influences outcomes, or student characteristics drive modality choice). Some students, including non-native English speakers, reported transcription issues, suggesting evaluations may reflect technology performance rather than modality. Future studies should examine outcomes when students can voice prompt in their native language. Transcription delay was not measured and may have influenced student behaviour and perceptions. Possible future avenues for this research could include the use of validated surveys measuring technology acceptance [3] and monitoring how students interact with LLMs in non-programming tasks. The tasks in this study were relatively simple and short, which may have not been suitable for comparing modalities. Longitudinal evaluation of retention or potential disadvantages should be explored in future work with more complex tasks and correspondingly longer voice and text prompts.

# 5 Discussion

This study examined students’ success, persistence, and perceptions when solving Prompt Problems using voice versus text inputs. Critically, voice engagement did not reduce student preference or use. For those who initially used voice prompts, input modality failing to predict subsequent choices may be due to strategically combining use of text and voice, consistent with prior work [23].

There was a heavy skew toward students’ engagement with and preference for text input, mirroring Zavaleta Bernuy et al. [39], who found students preferred text over voice as a medium for self-explanations. Our findings appear driven not only by practical barriers (e.g., hardware, environment), but also by low perceived control [27] (e.g., Voice - Superfluous, Text - Familiarity &#x26; User Confidence) and concerns the negative perception of Input Control and Accuracy, aligning with Korkmaz et al. [15]. Future work should improve voice usability, to support student control over success, through better hardware, appropriate environments, native language options [14, 30], explicit instruction, and adaptive transcription.

Although students were more likely to experience immediate success using text prompts than unedited voice prompts, this may not translate to meaningful understanding, as over-reliance on AI and superficial strategies can undermine metacognition and retention. Future research into this area should focus on better facilitating the use of voice input and examining its impact in controlled settings.

# 7 Conclusions

This exploratory study illuminated the complex trade-offs between using text and voice input modalities for prompt-based programming. While students showed a clear preference for text, voice input holds promise as a tool for deeper cognitive engagement and self-explanation, with the potential to support long-term learning outcomes.

# Acknowledgments

This work was supported by Research Council of Finland grant #356114.

