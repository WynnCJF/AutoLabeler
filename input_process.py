import os
from dotenv import load_dotenv
from aiconfig import AIConfigRuntime, InferenceOptions, CallbackManager
from aiconfig import Prompt
import pandas as pd
import asyncio
import openai
import google.generativeai as palm

load_dotenv()

openai.api_key = os.getenv("openai_api_key")
palm.configure(api_key=os.getenv("palm_api_key"))


class Labeler:
    def __init__(self, task, desc, file_path):
        """
        Constructor creates aiconfig
        Inputs:
        task: string - labelling task description
        desc: string - description of input data
        filepath: string - path to csv file containing training examples
        """
        train_df = pd.read_csv(file_path)
        classes = train_df["label"].unique()

        params = self.__getTrainParams(train_df, classes, task, desc)

        # create model and add training parameters
        self.aiconfig = AIConfigRuntime.create(
            "labeler_config",
            "data labeler config",
            metadata={"parameters": params}
        )
        
    def create_labeler(self, name, model_type="gpt-3.5-turbo", model_settings=None):
        """
        Create a lastmileAI model and prompt in aiconfig to be used for prediction
        Inputs:
        # name: string - name of labeler
        # model_type - string : model of LLM used
        # model_settings - python dictionary (contents depend on model used)
        """
        model_name = model_type

        if model_settings == None:
            model_settings = {"top_p": 1, "model": model_type, "temperature": 1,
                              "system_prompt": "You will only output a code block. No text explanation unless specified in the prompt."}

        self.aiconfig.add_model(model_name, model_settings)
        label_inputs = Prompt(
            name=name,
            input="""I want you to help with labeling data for the task of {{ task_name }}. The feature input of the task is {{ input_description }}. The output is a {{ class_num }}-class classification result. The output classes are: {{ output_classes }}. Here are several examples: {{ examples }}
            Please act as a data labeler, and label the following data: {{ real_inputs }}. There are {{ num_predictions }} inputs and {{ num_prediction}} outputs expected. Return only the predicted outputs in a python list, which should have {{ num_selected }} elements. """,
            metadata={"model": {"name": model_type,
                                "settings": {"model": model_type}}}
        )

        self.aiconfig.add_prompt(name, label_inputs)

    def saveAIConfig(self, fname, path="./"):
        """
        Saves AIConfig to a JSON file
        fname: string - name of file (must end with .json)
        path: directory to save file to
        """
        self.aiconfig.save(path+fname, include_outputs=False)


    async def predict(self, path, labeler, mode=True):
        """
        Generate predictions to text inputs
        path: string - file path to csv file with text inputs (one column, with header)
        labeler: string or list[string] - names of labelers to be used for prediction
        mode: bool - If true and labeler contains 3 elements or more, mode is added to output dataframe

        Returns pandas dataframe with original input and predictions
        """
        df = pd.read_csv(path)
        print("labeling " + str(df.shape[0]) + " entries\n")

        params = self.__getPredictParams(df)

        if not isinstance(labeler, list):
            labeler = [labeler]

        success = []
        for model in labeler:
            try:
                completion = await self.aiconfig.run(model, params=params)
                pred_str = self.aiconfig.get_output_text(model)
                pred_str = pred_str[1:-1]
                pred_str = pred_str.replace('\'', '')
                pred_str = pred_str.replace('\"', '')
                predictions_lst = [x.strip() for x in pred_str.split(',')]
                df[model] = predictions_lst
                success.append(model)
            except:
                print("error in " + model + " output\n")

        if (len(success) > 2) and mode:
            df['Mode'] = df[success].mode(axis=1).iloc[:, 0]

        return df

    def __getTrainParams(self, df, classes, task_name, input_desc):
        """
        Returns global parameter database
        """
        assert (df.shape[0] <= 100)

        class_text = ', '.join(classes)
        classes_num = len(classes)

        params = {"task_name": task_name, "input_description": input_desc,
                  "output_classes": class_text, "class_num": str(classes_num)}

        examples_text = ""
        for index, row in df.iterrows():
            examples_text = examples_text + \
                "Input: {{ input" + \
                str(index) + " }} ,Output: {{ output" + str(index) + " }}\n"
            params["input"+str(index)] = row[1]
            params["output"+str(index)] = row[0]

        params["examples"] = examples_text
        return params

    def __getPredictParams(self, df):
        """
        Returns parameter to be used in predicting labels of testing dataset
        """
        input_text = ""
        for i in range(df.shape[0]):
            input_text = input_text + str(i) + ". " + df.iloc[i, 0] + "\n"

        return {"real_inputs": input_text, "num_predictions": str(df.shape[0])}
