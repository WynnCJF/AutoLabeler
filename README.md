# Auto Labeler

## Inspiration
Not all NLP tasks require an LLM. There still exist lots of simple but specific NLP tasks (e.g. search query classification for a search engine), which be carried out by smaller, faster, and more resource-efficient models -- as long as we have labelled data for supervised training. Traditionally, when faced with data labeling tasks, we have to engage outsourcing human labeler teams and divide them into multiple groups to ensure high labeling accuracy. Our project, Llabeler, aims to leverage the outstanding few-shot learning abilities of LLMs to conduct fast and automatic data labeling for simple text classification tasks.

## What it does
Llabeler is currently comes in the form a Streamlit application, where users can input their NLP task's description and dataset. Given a set of user-defined task & I/O descriptions, as well as an file with very few labeled examples, we use three LLMs (PaLM, GPT-3.5, GPT-4) to produce predicted labels for the dataset. Subsequently, we will determine the mode (most frequently occurring label) among these predictions. This approach not only eliminates the need for extensive manual annotation but also enhances efficiency in obtaining accurate labels for our NLP tasks. The final output of Llabeler is a fully-labeled, ready-to-use .csv dataset.

## How we built it
We take advantage of LastMile.ai to easily configure prompts and access multiple LLMs. We build the front-end application with Streamlit.

## Challenges we ran into
We encountered several challenges in the project. Firstly, obtaining predicted labels from large language models (LLMs), particularly the Google PLAM model, proved to be unstable. We suspect this may be due to an outdated version, and we anticipate more stable outputs with future updates. Secondly, our model options are currently restricted to GPT-4, GPT-3.5, PLAM, and a handful of text-to-text models on Hugging Face. Limited model choices pose a constraint, restricting our exploration to only a few models for our application. We aim to overcome these challenges to enhance the reliability and diversity of our model outputs in the future.

## Accomplishments that we're proud of
We were able to make use of the LastMile AI's AIConfig to develop the Llabler that uses multiple LLM models - GPT-3.5, GPT-4 and Palm. In our experiments we used the Huggingface financial phrasebank dataset, which contains some phrases of financial news and we wanted to label the sentiment as "positive", ", it achieved 95% success rate in returning a final label, and a 76% accuracy in the financial sentiment labelling task. Note that in the original dataset they used 3 researchers and 13 masters students as annotators, and they have different methods in getting consensus. If we change the consensus rule to become all-agreement, it reaches 96% accuracy given success labeling.

## What we learned
Precise and concise prompting is very important for regulating LLMs' output format.

## What's next for Llabeler
Looking forward, the Auto Labeler project has big potential beyond the hackathon. By prioritizing continuous model improvement, integrating domain-specific models, and fostering human-in-the-loop collaboration, the system can evolve dynamically to meet the evolving demands of NLP tasks.

#### Run Streamlit app
```bash
streamlit run app.py
```