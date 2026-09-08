from datetime import datetime

stories = [
    {
        "title": "The Knock at 3 AM",
        "script": """
ည ၃ နာရီတိတိမှာ...

တံခါးကို သုံးချက်ခေါက်သံ ကြားလိုက်ရတယ်။

တစ်ယောက်တည်းနေတဲ့ ကောင်လေးက
တံခါးကို ဖြည်းဖြည်းချင်း ဖွင့်ကြည့်လိုက်တယ်။

ဒါပေမယ့်...

အပြင်မှာ ဘယ်သူမှ မရှိဘူး။

သူ တံခါးပိတ်လိုက်တဲ့အချိန်မှာတော့...

သူ့အခန်းထဲကနေ
တံခါးခေါက်သံ သုံးချက် ထပ်ကြားလိုက်ရတယ်...
"""
    }
]

story = stories[0]

today = datetime.now().strftime("%Y-%m-%d")

content = f"""# 👻 {story['title']}

Date: {today}

{story['script']}
"""

with open("horror_story.txt", "w", encoding="utf-8") as f:
    f.write(content)

print("👻 Horror story generated successfully!")
print(content)