import os
import sys
import xgboost

# نام فایلی که به دنبال آن هستیم
filename_to_find = "xgboost.dll"

# مسیری که جستجو در آن انجام می‌شود (کل محیط پایتون فعلی)
search_path = sys.prefix

print(f"در حال جستجو برای '{filename_to_find}' در مسیر '{search_path}'...")
print("این فرآیند ممکن است چند لحظه طول بکشد...")

found_path = None
# os.walk تمام پوشه‌ها و فایل‌های زیرمجموعه را می‌گردد
for root, dirs, files in os.walk(search_path):
    if filename_to_find in files:
        # به محض پیدا شدن، مسیر کامل آن را ذخیره کن و از حلقه خارج شو
        found_path = os.path.join(root, filename_to_find)
        break

print("-" * 30)

if found_path:
    print("✅ فایل xgboost.dll با موفقیت پیدا شد!")
    print(f"\nمسیر کامل فایل:\n{found_path}")
    print("\n>>> این مسیر را در فایل .spec خود در بخش 'binaries' کپی کنید.")
else:
    print("❌ خطا: فایل پیدا نشد!")
    print(f"فایل '{filename_to_find}' در محیط پایتون شما پیدا نشد.")
    print("لطفاً از نصب صحیح کتابخانه xgboost مطمئن شوید.")



print("-" * 30)

# مسیر پوشه کتابخانه xgboost را پیدا می‌کند
xgb_path = os.path.dirname(xgboost.__file__)

# مسیر کامل فایل VERSION را می‌سازد
version_file_path = os.path.join(xgb_path, 'VERSION')

if os.path.exists(version_file_path):
    print("✅ فایل VERSION پیدا شد!")
    print(f"\nمسیر کامل فایل:\n{version_file_path}")
else:
    print("❌ خطا: فایل VERSION در مسیر مورد انتظار پیدا نشد!")