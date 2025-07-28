import flet as ft
import flet_lottie as fl
import base64, os, json
import sys
import numpy as np
from typing import Union, List, Dict

def home_ui(page: ft.Page,HomeModel,HomeBll):
    page.title = "Predict Calorie"
    page.scroll = "auto"
    page.window.width = 600
    page.window.min_height=500
    page.window.min_width=300

# --------------------------------------------------------------------------
# Animations
# --------------------------------------------------------------------------


    # تابع برای دریافت مسیر فایل JSON
    def get_json_paths(filenames: Union[str, List[str]]) -> List[str]:
        """دریافت مسیر کامل فایل‌های JSON"""
        # تبدیل به لیست اگر تک فایل باشد
        if isinstance(filenames, str):
            filenames = [filenames]

        # تعیین مسیر پایه
        if getattr(sys, 'frozen', False):
            base_path = os.path.join(sys._MEIPASS, "assets")
        else:
            base_path = os.path.join(os.path.abspath("."), "assets")

        # ساخت مسیرهای کامل
        return [os.path.join(base_path, filename) for filename in filenames]

    def load_json_files(filenames: Union[str, List[str]]) -> Dict[str, str]:
        """
        لود کردن یک یا چند فایل JSON و تبدیل به base64

        Args:
            filenames: نام فایل یا لیست نام فایل‌ها

        Returns:
            دیکشنری با کلید نام فایل و مقدار base64 محتوا
        """
        # اطمینان از اینکه ورودی لیست باشد
        if isinstance(filenames, str):
            filenames = [filenames]

        # دریافت مسیرهای کامل
        paths = get_json_paths(filenames)

        results = {}

        for filepath, filename in zip(paths, filenames):
            try:
                with open(filepath, "rb") as f:
                    json_content = f.read()
                    base64_content = base64.b64encode(json_content).decode("utf-8")
                    results[filename] = base64_content

            except FileNotFoundError:
                print(f"خطا: فایل '{filename}' پیدا نشد")
                results[filename] = ""
            except Exception as e:
                print(f"خطا در لود فایل '{filename}': {e}")
                results[filename] = ""

        return results


    animations = load_json_files(["Grey_Wave.json", "header_anime.json"])

    # انیمیشن پس‌زمینه با تنظیمات بهتر
    background_animation = fl.Lottie(
        src_base64=animations["Grey_Wave.json"],
        reverse=False,
        animate=True,
        fit=ft.ImageFit.COVER,  # یا می‌توانید CONTAIN را امتحان کنید
        filter_quality=ft.FilterQuality.HIGH,
        expand=True,  # این مهم است
    )

    header_animation = fl.Lottie(
        src_base64=animations["header_anime.json"],
        reverse=False,
        animate=True,
        fit=ft.ImageFit.COVER,  # یا می‌توانید CONTAIN را امتحان کنید
        filter_quality=ft.FilterQuality.HIGH,
        expand=True,  # این مهم است
    )

    # Container برای انیمیشن که کل صفحه را پر کند
    background_container = ft.Container(
        alignment=ft.alignment.center,
        content=background_animation,
        expand=True,
        padding=0,
        margin=0,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,  # برای جلوگیری از overflow
    )

# --------------------------------------------------------------------------
# App_Bar
# --------------------------------------------------------------------------


    # آپ بار
    page.appbar = ft.AppBar(
        title=ft.Row(
            controls=[
                ft.Icon(ft.Icons.DIRECTIONS_RUN, color=ft.Colors.WHITE, size=24),
                ft.Container(width=8),
                ft.Text(
                    "Estimate calories burned",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
            ]
        ),
        center_title=True,
        bgcolor=ft.Colors.BLUE_ACCENT_200,
        elevation=4,
    )

# --------------------------------------------------------------------------
# Functions
# --------------------------------------------------------------------------

    def update_forecast_button_state():
        # چک می‌کنیم که همه تکست‌فیلدهای مورد نیاز مقدار داشته باشند.
        required_fields = [
            dropdown_gender.value,
            textField_Age.value,
            textField_Height.value,
            textField_Weight.value,
            textField_Duration.value,
            textField_Heart_Rate.value,
            textField_Body_Temp.value,
        ]
        # اگر همه فیلد‌های مورد نیاز مقدار داشته باشند, دکمه فعال می‌شود.
        if all(required_fields):
            forecast_button.disabled = False
            textField_Result.value = ''
        else:
            forecast_button.disabled = True
            textField_Result.value = "Please fill all the fields"
        page.update()

    def update_forecast_button_state_after(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            # به روز رسانی دکمه forrcast پس از اجرای تابع اعتبارسنجی
            update_forecast_button_state()
            return result
        return wrapper


    @update_forecast_button_state_after
    def validate_number(e):
        input_value = e.control.value
        previous_value = getattr(validate_number, "previous_value", "")
        # بررسی: اگر کاراکتر وارد شده عدد نباشد
        if input_value and not input_value.isdigit():
            e.control.value = previous_value
            page.open(ft.SnackBar(content=ft.Text("Please enter number only."),
                                  bgcolor=ft.Colors.RED_600,
                                  duration=3000))
        # اگر طول عدد وارده بیشتر از 3 رقم بود
        elif len(input_value) > 3:
            e.control.value = previous_value
            page.open(
                ft.SnackBar(content=ft.Text("The entered number is not within the normal range."),
                            bgcolor=ft.Colors.RED_600,
                            duration=3000))
        page.update()




    @update_forecast_button_state_after
    def validate_number_float(e , max_value=99.99, max_decimals=2):
        input_value = e.control.value
        previous_value = getattr(validate_number_float, "previous_value", "")

        if not input_value:
            validate_number_float.previous_value = ""
            page.update()
            return

        try:
            # بررسی معتبر بودن به عنوان float
            float_value = float(input_value)

            # بررسی منفی نبودن
            if float_value < 0:
                raise ValueError("Negative numbers not allowed")

            # بررسی حداکثر مقدار
            if float_value > max_value:
                raise ValueError(f"Value exceeds maximum ({max_value})")

            # بررسی تعداد اعشار
            if "." in input_value:
                decimal_part = input_value.split(".")[1]
                if len(decimal_part) > max_decimals:
                    raise ValueError(f"Maximum {max_decimals} decimal places allowed")

            # اگر همه چیز معتبر بود، مقدار را ذخیره کن
            validate_number_float.previous_value = input_value

        except ValueError as error:
            e.control.value = previous_value
            error_message = str(error)

            # پیام‌های خطای سفارشی
            if "could not convert" in error_message or "invalid literal" in error_message:
                message = "Please enter valid positive numbers (decimals allowed)."
            else:
                message = error_message

            page.open(
                ft.SnackBar(
                    content=ft.Text(message),
                    bgcolor=ft.Colors.RED_600,
                    duration=3000,
                )
            )

        page.update()





    @update_forecast_button_state_after
    def dropdown_gender_value(e):
        pass



    @update_forecast_button_state_after
    def clear_fields(e):
        dropdown_gender.value = None
        textField_Age.value= None
        textField_Height.value = None
        textField_Weight.value = None
        textField_Duration.value = None
        textField_Heart_Rate.value = None
        textField_Body_Temp.value = None
        page.update()

    def forecast_calories(e):
        data = HomeModel.CaloriesVariable(
            Sex = dropdown_gender.value,
            Age = float(textField_Age.value) if textField_Age.value else 0.0,
            Height = float(textField_Height.value) if textField_Height.value else 0.0,
            Weight = float(textField_Weight.value) if textField_Weight.value else 0.0,
            Duration = float(textField_Duration.value) if textField_Duration.value else 0.0,
            Heart_Rate = float(textField_Heart_Rate.value) if textField_Heart_Rate.value else 0.0,
            Body_Temp = float(textField_Body_Temp.value) if textField_Body_Temp.value else 0.0,
        )

        result_model = HomeBll().Calories_send_to_joblib(calories_data=data)
        textField_Result.value = int(np.round(result_model))
        page.update()


# --------------------------------------------------------------------------
# Objects
# --------------------------------------------------------------------------


    reponsive_rows_setting = {
        "xs": 12,  # موبایل: تمام عرض
        "sm": 6,  # تبلت کوچک: نصف عرض
        "md": 4,  # تبلت: یک سوم عرض
        "lg": 3,  # دسکتاپ: یک چهارم
        "xl": 3,  # دسکتاپ بزرگ: یک چهارم
    }
    dropdown_gender = ft.DropdownM2(expand=True, col=reponsive_rows_setting, label="Gender",
                                    bgcolor=ft.Colors.GREY_50,filled=True,
                                    options=[
                                        ft.dropdown.Option("male"),
                                        ft.dropdown.Option("female"),],
                                    on_change=lambda e:dropdown_gender_value(e),
                                    )

    textField_Age = ft.TextField(col=reponsive_rows_setting, label='Age(Year)', value="",
                                 text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                                 bgcolor=ft.Colors.GREY_50,filled=True,
                                on_change=lambda e:validate_number(e))

    textField_Height = ft.TextField(col=reponsive_rows_setting, label='Height(CM)', value="",
                                    bgcolor=ft.Colors.GREY_50, filled=True,
                                 text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                                    on_change=lambda e:validate_number(e))

    textField_Weight = ft.TextField(col=reponsive_rows_setting, label='Weight(KG)', value="",
                                    bgcolor=ft.Colors.GREY_50, filled=True,
                                 text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                                    on_change=lambda e:validate_number(e))

    textField_Duration = ft.TextField(col=reponsive_rows_setting, label='Duration(Minute)', value="",
                                      bgcolor=ft.Colors.GREY_50, filled=True,
                                 text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                                      on_change=lambda e:validate_number(e))

    textField_Heart_Rate = ft.TextField(col=reponsive_rows_setting, label='Heart Rate', value="",
                                        bgcolor=ft.Colors.GREY_50, filled=True,
                                 text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                                        on_change=lambda e:validate_number(e))

    textField_Body_Temp = ft.TextField(col=reponsive_rows_setting, label='Body Temp(Celsius)', value="",
                                       bgcolor=ft.Colors.GREY_50, filled=True,
                                 text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                                       on_change=lambda e:validate_number_float(e))

    clear_button = ft.ElevatedButton(
        text="Clear the fields",
        on_click=lambda e: clear_fields(e),
        col=reponsive_rows_setting,
        style=ft.ButtonStyle(
            shape={
                ft.ControlState.HOVERED: ft.StadiumBorder(),
                ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=10),
                ft.ControlState.DISABLED: ft.RoundedRectangleBorder(radius=10),
            },
            color={
                ft.ControlState.HOVERED: ft.Colors.WHITE,
                ft.ControlState.DEFAULT: ft.Colors.BLACK,
                ft.ControlState.DISABLED: ft.Colors.WHITE,
            },
            bgcolor={
                ft.ControlState.HOVERED: ft.Colors.BLUE_800,
                ft.ControlState.DEFAULT: ft.Colors.BLUE_300,
                ft.ControlState.DISABLED: ft.Colors.GREY,
            },
            side={
                ft.ControlState.DISABLED: ft.BorderSide(1, ft.Colors.BLACK),
            },
        ),
        width=200,
        height=50,
    )


    forecast_button = ft.ElevatedButton(
        text="Forecast",
        on_click=lambda e: forecast_calories(e),
        disabled=True,
        col=reponsive_rows_setting,
        style=ft.ButtonStyle(
            shape={
                ft.ControlState.HOVERED: ft.StadiumBorder(),
                ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=10),
                ft.ControlState.DISABLED: ft.RoundedRectangleBorder(radius=10),
            },
            color={
                ft.ControlState.HOVERED: ft.Colors.WHITE,
                ft.ControlState.DEFAULT: ft.Colors.BLACK,
                ft.ControlState.DISABLED: ft.Colors.WHITE,
            },
            bgcolor={
                ft.ControlState.HOVERED: ft.Colors.GREEN_800,
                ft.ControlState.DEFAULT: ft.Colors.GREEN_300,
                ft.ControlState.DISABLED: ft.Colors.GREY,
            },
            side={
                ft.ControlState.DISABLED: ft.BorderSide(1, ft.Colors.BLACK),
            },
        ),
        width=200,
        height=50,
    )

    textField_Result = ft.TextField(col=reponsive_rows_setting, label='Calories burned',
                                    bgcolor=ft.Colors.GREY_50, filled=True,
                                    value="Please fill all the fields",
                                 text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                                      read_only=True )


    container_1 = ft.Container(
        alignment=ft.alignment.center,
        height=100,
        expand=True,
        padding=0,
        margin=0,
        bgcolor=ft.Colors.TRANSPARENT,
        content=header_animation
    )

    container_2 = ft.Container(
        alignment=ft.alignment.center,
        expand=True,
        padding=0,
        margin=0,
        bgcolor=ft.Colors.TRANSPARENT,
        content=ft.ResponsiveRow(
            controls=[dropdown_gender,
                      textField_Age,textField_Height,
                      textField_Weight,textField_Duration,
                      textField_Heart_Rate,textField_Body_Temp,
                      clear_button]
        )
    )

    container_3 = ft.Container(
        alignment=ft.alignment.center,
        expand=True,
        padding=0,
        margin=0,
        bgcolor=ft.Colors.TRANSPARENT,
        content=ft.ResponsiveRow(
            controls=[forecast_button,
                      textField_Result]
        )
    )

# --------------------------------------------------------------------------
# Stack , View
# --------------------------------------------------------------------------


    # محتوای اصلی
    main_content = ft.Container(
        alignment=ft.alignment.top_center,  # کل محتوا از بالا چیده میشود
        expand=True,
        padding=25,
        margin=0,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            spacing=30,
            controls=[
                container_1,
                container_2,
                container_3
            ],
        ),
    )

    # Stack با تنظیمات بهتر
    stack = ft.Stack(
        expand=True,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        controls=[
            background_container,
            main_content,
        ],
    )

    #
    return ft.View(
        route="home_ui",
        appbar=page.appbar,
        padding=0,
        controls=[stack],

    )