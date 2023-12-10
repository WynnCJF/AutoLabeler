import streamlit as st
from input_process import Labeler


st.header("Auto Data Labeling 🏷️")

# Task description
st.markdown("### Define your labeling task")
task_name = st.text_input(
    label="Task name",
    value="Financial phrase sentiment classification",
    key="tn1",
    placeholder="Financial phrase sentiment classification"
)

input_description = st.text_input(
    label="Input feature description",
    value="A financial phrase from a piece of report/news to be classified.",
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
        labeler = Labeler(task=task_name, desc=input_description, file_path=example_csv_file)
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