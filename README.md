# LLM Bias Benchmark
Repository for the Open-BBQ Benchmark for Large Language Models in
Open-ended Settings.

Authors: Zhao Liu∗, Tian Xie∗, Xueru Zhang

## The paper
Our paper "Evaluating and Mitigating Social Bias for Large Language Models in
Open-ended Settings"(https://arxiv.org/abs/2412.06134).

## Open-BBQ Benchmark (paper abstract)
Current social bias benchmarks for Large Language Models (LLMs) primarily rely on pre-defined question formats like multiple-choice, limiting their ability to reflect the complexity and open-ended nature of real-world interactions.
To address this gap, we extend an existing BBQ dataset introduced by Parrish incorporating fill-in-the-blank and short-answer question types, designed to evaluate biases in an open-ended setting.
Since evaluating free text in real-world use cases is always a huge challenge, we developed the process of evaluation to detect bias and stereotypes in an open-ended setting automatically.
Our finding reveals that LLMs tend to produce responses that are more biased against certain protected attributes, like age and socio-economic status.
On the other hand, these biased outputs produced by LLMs can serve as valuable contexts and chains of thought for debiasing.
Our debiasing approach combined zero-shot, few-shot, and chain-of-thought could significantly reduce the level of bias to almost 0.
We open-source our evaluation and debiasing code hoping to encourage further measurements and mitigation of bias and stereotype in LLMs.