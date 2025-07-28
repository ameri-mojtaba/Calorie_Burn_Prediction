from pages.model.model import HomeModel # اصلی
from dataclasses import dataclass
import pandas as pd
import joblib
import numpy as np

@dataclass
class HomeBll:


    def smart_find_model(model_name: str, model_sub_dir: str = "assets/joblib") -> str:
        import os
        import sys
        """
        Finds a reliable path to the model file, whether in development or built mode.

        Args:
            model_name (str): The name of the model file (for example: 'my_model.joblib').
            model_sub_dir (str): The relative path of the models folder from the project root.

        Returns:
            str: The absolute and correct path to the model file.

        """
        if getattr(sys, 'frozen', False):

            base_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        possible_relative_paths = [
            os.path.join(base_path, model_sub_dir, model_name),  # حالت build شده
            os.path.join(base_path, '..', model_sub_dir, model_name),  # اگر اسکریپت داخل پوشه src باشد
            os.path.join(base_path, '../..', model_sub_dir, model_name),  # اگر اسکریپت دو سطح تو در تو باشد
        ]

        print("🔎 در حال جستجو برای مدل...")
        for path in possible_relative_paths:
            # os.path.normpath مسیر را تمیز و استاندارد می‌کند (مثلاً 'a/b/../c' را به 'a/c' تبدیل می‌کند)
            clean_path = os.path.normpath(path)

            if os.path.exists(clean_path):
                print(f"✅ Model found: {clean_path}")
                return clean_path

        raise FileNotFoundError(
            f"فایل مدل '{model_name}' در هیچ‌یک از مسیرهای مورد انتظار یافت نشد. مسیر پایه جستجو: {base_path}")




    def Calories_send_to_joblib(self ,calories_data :HomeModel.CaloriesVariable  ):
        input_data = {
            'Sex': [calories_data.Sex],
            'Age': [calories_data.Age],
            'Height': [calories_data.Height],
            'Weight': [calories_data.Weight],
            'Duration': [calories_data.Duration],
            'Heart_Rate': [calories_data.Heart_Rate],
            'Body_Temp': [calories_data.Body_Temp]
        }

        input_data_df = pd.DataFrame(input_data)

        model_path = HomeBll.smart_find_model("calorie_prediction_pipeline.joblib")
        loaded_pipeline = joblib.load(model_path)
        joblib_output = loaded_pipeline.predict(input_data_df)

        return joblib_output

