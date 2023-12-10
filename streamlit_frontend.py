import streamlit as st
from input_process import Labeler
import asyncio


st.header("Auto Data Labeling 🏷️")

# Task description
st.markdown("### Define your labeling task")
task_name = st.text_input(
    label="Task name",
    value="Financial phrase sentiment classification",
    key="tn1",
    placeholder="Financial phrase sentiment classification"
)

task_description = st.text_area(
    label="Task description",
    value="",
    key="task_desc1",
)

input_description = st.text_input(
    label="Input feature description",
    value="A financial phrase from a piece of news to be classified.",
    key="td1",
    placeholder="A financial phrase from a piece of report/news to be classified."
)

out_class_num = st.number_input(
    label="Number of output classes",
    min_value=2,
    max_value=10,
    key="ocn1",
)

with st.expander("Define output classes:"):
    out_classes_lst = []

    for i in range(out_class_num):
        out_classes_lst.append(
            st.text_input(
                label="Output class {}".format(i+1),
                value="",
                key="oc{}".format(i+1),
                placeholder=""
            )
        )

# Parse output classes
output_classes_lst = [x for x in out_classes_lst if x != ""]

allow_example = False
if len(output_classes_lst) > 0:
    if out_class_num != len(output_classes_lst):
        st.error("Number of output classes and output classes do not match!")
        allow_example = False
    else:
        allow_example = True

# Read in example file
allow_real_input = False
if allow_example:
    st.divider()
    st.markdown("### Upload an example dataset")
    example_csv_file = st.file_uploader(
        label="Upload a CSV file containing examples. Please make sure that there are at least 1 example for each class. Columns: [Input, Output]",
        type="csv",
        key="ud1"
    )

    if example_csv_file is not None:
        st.write("Example CSV file uploaded successfully!")
        # Create labeler
        labeler = Labeler(task=task_name, desc=input_description, task_desc=task_description,
                          file_path=example_csv_file)

        # Create LLM labelers
        # GPT-3.5
        labeler.create_labeler("chatgpt", "gpt-3.5-turbo")

        # PaLM
        palm_settings = {"topK": 40, "topP": 0.95, "maxOutputTokens": 1024, "model": "models/text-bison-001",
                         "system_prompt": "You will only output a code block. No text explanation unless specified in the prompt."}
        labeler.create_labeler("palm", "models/text-bison-001", palm_settings)

        # GPT-4
        gpt4_settings = {"top_p": 1, "model": "gpt-4", "temperature": 1, "remember_chat_context": False,
                         "system_prompt": "You will only output a code block. No text explanation unless specified in the prompt. Only return a list of outputs."}
        labeler.create_labeler("gpt4", "gpt-4", gpt4_settings)
        
        # Save configuration to JSOn
        labeler.saveAIConfig("newconfig.json")

        allow_real_input = True

    else:
        st.write("Example CSV file not uploaded.")

if allow_real_input:
    st.divider()
    st.markdown("### Upload the dataset to be labeled")
    data_csv_file = st.file_uploader(
        label="Upload a CSV file containing the dataset to be labeled. Columns: ['Input']",
        type="csv",
        key="ud2",
    )
    
    if data_csv_file is not None:
        st.write("Dataset CSV file uploaded successfully!")
        
        start_predict_button = st.button("Start Auto-Labeling!")
        
        if start_predict_button:
            async def predict_labels(data_csv_file):
                return await labeler.predict(data_csv_file, ["chatgpt","palm","gpt4"])
            
            with st.spinner('Wait for it...'):
                results = asyncio.run(predict_labels(data_csv_file))

            st.success('Labeling completed!', icon="✅")
            data_for_download = results.to_csv().encode('utf-8')
            
            st.download_button(
                label="Download data as CSV",
                data=data_for_download,
                file_name='labeling_result.csv',
                mime='text/csv',
            )