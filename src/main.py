import flet as ft
import os


from pages.ui.home import home_ui
from pages.model.model import HomeModel
from pages.bll.HomeBll import HomeBll
from assets.joblib.calorie_prediction_features import FeatureEngineer


def main(page: ft.Page):
    # پاک‌سازی کامل صفحه در شروع
    page.views.clear()
    page.controls.clear()
    page.on_route_change = None
    page.on_view_pop = None


    page.window.alignment = ft.alignment.center  # پنجره کجای صفحه باز بشود
    page.window.center()

    # تنظیمات آیکون پنجره و تسک بار
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "icon.ico")
    page.window.icon = icon_path


    def route_change(route):
        # پاک کردن تمام Views قبلی
        page.views.clear()

        if page.route == "home_ui":
            page.views.append(home_ui(page,HomeModel,HomeBll))

        # به‌روزرسانی صفحه
        page.update()

    def view_pop(view):
        # حذف آخرین View (صفحه) از لیست Views
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # تنظیمات رویدادها
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # شروع از صفحه اصلی
    page.go('home_ui')

ft.app(target=main, assets_dir='assets')