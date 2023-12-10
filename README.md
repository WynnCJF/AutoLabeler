# Auto Labeler

### Project Goal
Our project, named Auto Labeler, aims to address the challenges associated with manual annotation in NLP tasks. Traditionally, when faced with annotation tasks, we had to engage outsourcing teams and divide them into multiple groups to ensure high labeling accuracy. The approach involved comparing labels assigned by different teams; if there was a consensus, the label was considered highly accurate.

To streamline and automate this process, we propose leveraging various large language models' zero-shot or few-shot learning ability. Instead of relying on manual efforts, three models will provide their predicted labels for the NLP task. Subsequently, we will determine the mode (most frequently occurring label) among these predictions. This approach not only eliminates the need for extensive manual annotation but also enhances efficiency in obtaining accurate labels for our NLP tasks.

#### Run Streamlit app
```bash
streamlit run app.py
```