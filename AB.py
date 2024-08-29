from telethon.sync import TelegramClient, events
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.errors.rpcerrorlist import MessageNotModifiedError, FloodWaitError
from telethon.tl.types import ChannelParticipantCreator, ChannelParticipantAdmin
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.functions.messages import DeleteMessagesRequest
import datetime
import pytz
import asyncio
import os
import pickle
import re
import io
import aiohttp
import random

# طلب إدخال api_id و api_hash و رقم الهاتف من المستخدم
api_id = input("أدخل API ID: ")
api_hash = input("أدخل API Hash: ")
phone_number = input("أدخل رقم الهاتف: ")

session_name = 'aa_update_session'
response_file = 'responses.pkl'
published_messages_file = 'published_messages.pkl'
muted_users_file = 'muted_users.pkl'
time_update_status_file = 'time_update_status.pkl'
channel_link_file = 'channel_link.pkl'
active_publishing_tasks = {}

client = TelegramClient(session_name, api_id, api_hash)
client.start(phone_number)

# قراءة الردود من الملف إذا كان موجودًا، وإلا استخدام قاموس فارغ
if os.path.exists(response_file):
    with open(response_file, 'rb') as f:
        responses = pickle.load(f)
else:
    responses = {}

# Load or initialize the channel link
if os.path.exists(channel_link_file):
    with open(channel_link_file, 'rb') as f:
        channel_link = pickle.load(f)
else:
    channel_link = None

# Load or initialize the time update status
if os.path.exists(time_update_status_file):
    with open(time_update_status_file, 'rb') as f:
        time_update_status = pickle.load(f)
else:
    time_update_status = {'enabled': False}

# Load or initialize the muted_users dictionary
if os.path.exists(muted_users_file):
    with open(muted_users_file, 'rb') as f:
        muted_users = pickle.load(f)
else:
    muted_users = {}

# Load responses and published messages from file or create new files if not exists

if os.path.exists(response_file):
    with open(response_file, 'rb') as f:
        responses = pickle.load(f)
else:
    responses = {}

if os.path.exists(published_messages_file):
    with open(published_messages_file, 'rb') as f:
        published_messages = pickle.load(f)
else:
    published_messages = []

# Define the active timers and countdown messages dictionaries
active_timers = {}
countdown_messages = {}

# اسم الصورة المحلية
image_path = 'local_image.jpg'

# Global variable to store the account name
account_name = None

async def respond_to_greeting(event):
    if event.is_private and not (await event.get_sender()).bot:  # تحقق ما إذا كانت الرسالة خاصة وليست من بوت
        message_text = event.raw_text.lower()
        if "هلا" in message_text:
            response = """
آهہليہنہ🎒

آلمآلكہ ما موجود 🎒

دز رسالتكہ وانتضر الرد🎒

رد تلقائي من سورس ᯤ̸𝐀𝐁𝐁𝐀𝐒𝐌𝐎𝐎𝟓𝟓ᯤ̸ 🎒

💠 سورس **❲** **AB** **❳** | @z1_xa 💠"""
            try:
                await client.send_file(event.chat_id, file=image_path, caption=response)
            except Exception as e:
                await event.reply(f"")
        else:
            for keyword, response in responses.items():
                if keyword in message_text:
                    try:
                        await client.send_file(event.chat_id, file=image_path, caption=response)
                    except Exception as e:
                        await event.reply(f"")
                    break

client.add_event_handler(respond_to_greeting, events.NewMessage(incoming=True))

def insert_emojis(message, emojis):
    random.shuffle(emojis)
    message_list = list(message)
    emoji_positions = []
    
    for emoji in emojis:
        pos = random.choice(range(len(message_list)))
        while pos in emoji_positions:
            pos = random.choice(range(len(message_list)))
        
        emoji_positions.append(pos)
        message_list[pos] = emoji
    
    return ''.join(message_list)

@client.on(events.NewMessage(from_users='me', pattern='.متت'))
async def update_message(event):
    await event.delete()
    message_text = ' ' * 6
    emojis = ['🤣', '😂', '😹', '🤣', '😂', '😹']
    
    message = await event.respond('🤣😂😹🤣😂😹')
    
    last_message = ""
    start_time = asyncio.get_event_loop().time()
    duration = 5  # مدة التحديث (10 ثوانٍ)
    
    while True:
        try:
            current_time = asyncio.get_event_loop().time()
            if current_time - start_time > duration:
                break
            
            emoji_string = insert_emojis(message_text, emojis)
            while emoji_string == last_message:
                emoji_string = insert_emojis(message_text, emojis)
            
            last_message = emoji_string
            await message.edit(emoji_string)
            
            await asyncio.sleep(0)

        except Exception as e:
            print(f"Error updating message: {e}")
            break

@client.on(events.NewMessage(from_users='me', pattern='.انتحار'))
async def suicide_message(event):
    await event.delete()
    
    # إرسال رسالة "جاري الانتحار"
    message = await event.respond("**جاري الانتحار .....**")
    
    # الانتظار لمدة 6 ثوانٍ
    await asyncio.sleep(3)
    
    # تحديث الرسالة إلى النص المطلوب
    final_message = (
        "تم الانتحار بنجاح😂...\n"
        "　　　　　|\n"
        "　　　　　|\n"
        "　　　　　|\n"
        "　　　　　|\n"
        "　　　　　|\n"
        "　　　　　|\n"
        "　　　　　|\n"
        "　　　　　|\n"
        "　／￣￣＼| \n"
        "＜ ´･ 　　 |＼ \n"
        "　|　３　 | 丶＼ \n"
        "＜ 、･　　|　　＼ \n"
        "　＼＿＿／∪ _ ∪) \n"
        "　　　　　 Ｕ Ｕ"
    )
    
    await message.edit(final_message)

def insert_emojis(message, emojis):
    random.shuffle(emojis)
    message_list = list(message)
    emoji_positions = []
    
    for emoji in emojis:
        pos = random.choice(range(len(message_list)))
        while pos in emoji_positions:
            pos = random.choice(range(len(message_list)))
        
        emoji_positions.append(pos)
        message_list[pos] = emoji
    
    return ''.join(message_list)

@client.on(events.NewMessage(from_users='me', pattern='.شرير'))
async def update_message(event):
    await event.delete()
    message_text = ' ' * 6
    emojis = ['😈', '💀', '👿', '🔪', '☠️', '👹']
    
    message = await event.respond('👿💀👹👿🔪☠️')
    
    last_message = ""
    start_time = asyncio.get_event_loop().time()
    duration = 5  # مدة التحديث (10 ثوانٍ)
    
    while True:
        try:
            current_time = asyncio.get_event_loop().time()
            if current_time - start_time > duration:
                break
            
            emoji_string = insert_emojis(message_text, emojis)
            while emoji_string == last_message:
                emoji_string = insert_emojis(message_text, emojis)
            
            last_message = emoji_string
            await message.edit(emoji_string)
            
            await asyncio.sleep(0)

        except Exception as e:
            print(f"Error updating message: {e}")
            break

@client.on(events.NewMessage(from_users='me', pattern='.add'))
async def add_response(event):
    try:
        if event.reply_to_msg_id:
            # الحصول على الرسالة التي تم الرد عليها
            replied_message = await client.get_messages(event.chat_id, ids=event.reply_to_msg_id)
            
            # تحقق مما إذا كانت الرسالة تحتوي على صورة
            if replied_message.photo:
                photo = replied_message.photo
            else:
                photo = None
            
            # استخراج الكلمة المفتاحية والرد من الرسالة
            if ' ' in event.raw_text:
                _, args = event.raw_text.split(' ', 1)
                if '(' in args and ')' in args:
                    keyword, response = args.split('(', 1)[1].split(')', 1)
                    keyword = keyword.strip().lower()
                    response = response.strip()
                    
                    # حفظ الصورة والرد في القاموس
                    responses[keyword] = {
                        'response': response,
                        'photo': photo
                    }
                    
                    # حفظ الردود في الملف
                    with open(response_file, 'wb') as f:
                        pickle.dump(responses, f)
                    
                    if photo:
                        await event.reply("✅ تم إضافة الرد مع الصورة.")
                    else:
                        await event.reply("✅ تم إضافة الرد بدون صورة.")
                else:
                    await event.reply("⚠️ يجب استخدام الصيغة الصحيحة: .image (الكلمة المفتاحية) الرد")
            else:
                await event.reply("⚠️ يجب استخدام الصيغة الصحيحة: .image (الكلمة المفتاحية) الرد")
                
        else:
            await event.reply("⚠️ يجب الرد على رسالة تحتوي على صورة أو يمكنك إرسال الرد بدون صورة مباشرة.")
    except Exception as e:
        await event.reply(f"حدث خطأ: {str(e)}")

@client.on(events.NewMessage(incoming=True))
async def respond_to_greeting(event):
    if event.is_private and not (await event.get_sender()).bot:
        message_text = event.raw_text.lower()
        for keyword, data in responses.items():
            if keyword in message_text:
                try:
                    if data['photo']:
                        await client.send_file(event.chat_id, file=data['photo'], caption=data['response'])
                    else:
                        await event.reply(data['response'])
                except Exception as e:
                    await event.reply(f"حدث خطأ: {str(e)}")
                break

async def respond_to_mention(event):
    if event.is_private and not (await event.get_sender()).bot:  # تحقق ما إذا كانت الرسالة خاصة وليست من بوت
        sender = await event.get_sender()
        await event.reply(f"انتظر يجي المطور @{sender.username} ويرد على رسالتك لا تبقه تمنشنه هواي")

client.add_event_handler(respond_to_mention, events.NewMessage(incoming=True, pattern=f'(?i)@{client.get_me().username}'))

def superscript_time(time_str):
    superscript_digits = str.maketrans('0123456789', '𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵')
    return time_str.translate(superscript_digits)

async def update_username():
    global account_name
    iraq_tz = pytz.timezone('Asia/Baghdad')
    
    # Get the current account name if not set
    if account_name is None:
        me = await client.get_me()
        account_name = re.sub(r' - \d{2}:\d{2}', '', me.first_name)
    
    while True:
        now = datetime.datetime.now(iraq_tz)
        current_time = superscript_time(now.strftime("%I:%M"))
        
        if time_update_status.get('enabled', False):
            new_username = f"{account_name} - {current_time}"
        else:
            new_username = f"{account_name}"
        
        try:
            # Change the username
            await client(UpdateProfileRequest(first_name=new_username))
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"Error updating username: {e}")
        
        # Calculate the remaining time until the start of the next minute
        seconds_until_next_minute = 60 - now.second
        await asyncio.sleep(seconds_until_next_minute)

@client.on(events.NewMessage(from_users='me', pattern=r'.ارسال (\d+) (\d+)'))
async def send_message_repeatedly(event):
    try:
        if event.is_reply:
            minutes = int(event.pattern_match.group(1))
            repeat_count = int(event.pattern_match.group(2))
            message = await event.get_reply_message()
            
            async def task():
                for i in range(repeat_count):
                    await client.send_message(event.chat_id, message)
                    await asyncio.sleep(minutes * 60)
            
            task = asyncio.create_task(task())
            
            # حفظ المهمة باستخدام معرف المحادثة لتتمكن من إيقافها لاحقًا
            if event.chat_id not in active_publishing_tasks:
                active_publishing_tasks[event.chat_id] = []
            active_publishing_tasks[event.chat_id].append(task)
            
            await event.reply(f"سيتم إرسال الرسالة كل {minutes} دقيقة لـ {repeat_count} مرات.")
        else:
            await event.reply("⚠️ يجب الرد على رسالة لاستخدام هذا الأمر.")
    except Exception as e:
        await event.reply(f"⚠️ حدث خطأ: {e}")

@client.on(events.NewMessage(from_users='me', pattern=r'.نشر متعدد (\d+)'))
async def send_message_infinite(event):
    try:
        if event.is_reply:
            minutes = int(event.pattern_match.group(1))
            message = await event.get_reply_message()
            
            async def task():
                while True:
                    await client.send_message(event.chat_id, message)
                    await asyncio.sleep(minutes * 60)
            
            task = asyncio.create_task(task())
            
            # حفظ المهمة باستخدام معرف المحادثة لتتمكن من إيقافها لاحقًا
            if event.chat_id not in active_publishing_tasks:
                active_publishing_tasks[event.chat_id] = []
            active_publishing_tasks[event.chat_id].append(task)
            
            await event.reply(f"سيتم إرسال الرسالة كل {minutes} دقيقة إلى ما لا نهاية.")
        else:
            await event.reply("⚠️ يجب الرد على رسالة لاستخدام هذا الأمر.")
    except Exception as e:
        await event.reply(f"⚠️ حدث خطأ: {e}")

@client.on(events.NewMessage(from_users='me', pattern=r'.ايقاف الارسال'))
async def stop_sending_messages(event):
    if event.chat_id in active_publishing_tasks:
        # إلغاء جميع المهام النشطة لهذه المحادثة
        for task in active_publishing_tasks[event.chat_id]:
            task.cancel()
        del active_publishing_tasks[event.chat_id]
        await event.reply("✅ تم إيقاف جميع عمليات النشر الفعّالة.")
    else:
        await event.reply("❌ لا توجد عمليات نشر فعّالة لإيقافها.")

# إضافة المفتاح الخاص بك
YOUTUBE_API_KEY = 'AIzaSyBfb8a-Ug_YQFrpWKeTc88zuI6PmHVdzV0'
YOUTUBE_API_URL = 'https://www.googleapis.com/youtube/v3/search'

@client.on(events.NewMessage(from_users='me', pattern=r'.يوتيوب (.+)'))
async def youtube_search(event):
    query = event.pattern_match.group(1)
    
    async with aiohttp.ClientSession() as session:
        async with session.get(YOUTUBE_API_URL, params={
            'part': 'snippet',
            'q': query,
            'key': YOUTUBE_API_KEY,
            'type': 'video',
            'maxResults': 1
        }) as response:
            data = await response.json()
            if data['items']:
                video_id = data['items'][0]['id']['videoId']
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                await event.reply(f"📹 هنا رابط الفيديو الذي تم العثور عليه:\n{video_url}")
            else:
                await event.reply("❌ لم يتم العثور على فيديو يتطابق مع العنوان المطلوب.")

@client.on(events.NewMessage(from_users='me', pattern='.تفعيل الوقت'))
async def enable_time_update(event):
    global time_update_status
    time_update_status['enabled'] = True
    with open(time_update_status_file, 'wb') as f:
        pickle.dump(time_update_status, f)
    reply = await event.reply("✅ تم تفعيل تحديث الاسم مع الوقت.")
    await event.delete()  # حذف الرسالة الأصلية

    await asyncio.sleep(1)
    await reply.delete()  # حذف رسالة التأكيد بعد 3 ثواني

@client.on(events.NewMessage(from_users='me', pattern='.تعطيل الوقت'))
async def disable_time_update(event):
    global time_update_status
    time_update_status['enabled'] = False
    with open(time_update_status_file, 'wb') as f:
        pickle.dump(time_update_status, f)
    
    # إزالة الوقت من اسم الحساب
    if account_name:
        iraq_tz = pytz.timezone('Asia/Baghdad')
        now = datetime.datetime.now(iraq_tz)
        current_name = re.sub(r' - \d{2}:\d{2}', '', account_name)
        new_username = f"{current_name}"
        
        try:
            await client(UpdateProfileRequest(first_name=new_username))
            reply = await event.reply("✅ تم تعطيل تحديث الاسم وإزالة الوقت من الاسم.")
        except Exception as e:
            reply = await event.reply(f"⚠️ حدث خطأ أثناء إزالة الوقت من الاسم: {e}")
    else:
        reply = await event.reply("⚠️ لم يتم تعيين اسم الحساب.")
    
    await event.delete()  # حذف الرسالة الأصلية

    await asyncio.sleep(1)
    await reply.delete()  # حذف رسالة التأكيد بعد 3 ثواني

@client.on(events.NewMessage(from_users='me', pattern='.اضافة قناة (.+)'))
async def add_channel(event):
    global channel_link
    channel_link = event.pattern_match.group(1)
    with open(channel_link_file, 'wb') as f:
        pickle.dump(channel_link, f)
    await event.reply(f"✅ تم تعيين رابط القناة إلى: {channel_link}")
    await event.delete()  # حذف الرسالة الأصلية

@client.on(events.NewMessage(from_users='me', pattern= '.ازالة القناة' ))
async def remove_channel(event):
    global channel_link
    channel_link = ''
    with open(channel_link_file, 'wb') as f:
        pickle.dump(channel_link, f)
    reply = await event.reply("❌ تم مسح رابط القناة.")
    await event.delete()  # حذف الرسالة الأصلية
    await asyncio.sleep(3)
    await reply.delete()  # حذف رسالة التأكيد بعد ثانية

async def is_subscribed(user_id):
    if not channel_link:
        return True  # إذا لم يكن هناك قناة محددة، اعتبر أن المستخدم مشترك
    channel_username = re.sub(r'https://t.me/', '', channel_link)
    try:
        offset = 0
        limit = 100
        while True:
            participants = await client(GetParticipantsRequest(
                channel=channel_username,
                filter=ChannelParticipantsSearch(''),
                offset=offset,
                limit=limit,
                hash=0
            ))
            if not participants.users:
                break
            for user in participants.users:
                if user.id == user_id:
                    return True
            offset += len(participants.users)
        return False
    except FloodWaitError as e:
        await asyncio.sleep(e.seconds)
        return await is_subscribed(user_id)
    except Exception as e:
        print(f"Error checking subscription: {e}")
        return False

@client.on(events.NewMessage(incoming=True))
async def respond_to_greeting(event):
    if event.is_private and not (await event.get_sender()).bot:  # تحقق ما إذا كانت الرسالة خاصة وليست من بوت
        sender = await event.get_sender()
        if sender.phone == '42777':
            # السماح بمراسلة الحساب بدون الاشتراك في القناة إذا كان الرقم من Telegram
            return
        if not await is_subscribed(event.sender_id):
            await event.reply(f"لا يمكنك مراسلتي الى بعد الاشتراك في قناتي: {channel_link}")
            await client.delete_messages(event.chat_id, [event.id])
        else:
            message_text = event.raw_text.lower()

@client.on(events.NewMessage(from_users='me', pattern='.del'))
async def delete_response(event):
    try:
        # Extract keyword from the message
        command, keyword = event.raw_text.split(' ', 1)
        keyword = keyword.lower()
        
        if keyword in responses:
            del responses[keyword]
            # Save responses to file
            with open(response_file, 'wb') as f:
                pickle.dump(responses, f)
            await event.reply("✅ تم حذف الرد")
        else:
            await event.reply("⚠️ لم يتم العثور على الكلمة المحددة")
    except ValueError:
        await event.reply("⚠️ استخدم الصيغة: del الكلمة المفتاحية")

@client.on(events.NewMessage(from_users='me', pattern='.الردود'))
async def show_responses(event):
    if responses:
        response_text = "📋 الردود المضافة:\n"
        for keyword, response in responses.items():
            response_text += f"🔹 الكلمة المفتاحية: {keyword}\n🔸 الرد: {response}\n"
        await event.reply(response_text)
    else:
        await event.reply("❌ لا توجد ردود مضافة حتى الآن.")

@client.on(events.NewMessage(from_users='me', pattern='.time'))
async def countdown_timer(event):
    try:
        # Extract the number of minutes from the message
        command, args = event.raw_text.split(' ', 1)
        minutes = int(args.strip().strip('()'))

        # Check if there's an active timer, cancel it
        if event.chat_id in active_timers:
            active_timers[event.chat_id].cancel()
            del active_timers[event.chat_id]
            # Remove the existing countdown message if it exists
            if event.chat_id in countdown_messages:
                await client.delete_messages(event.chat_id, countdown_messages[event.chat_id])
                del countdown_messages[event.chat_id]

        async def timer_task():
            nonlocal minutes
            total_seconds = minutes * 60
            # Send the initial message about the countdown starting
            countdown_message = await event.reply("**⏳ سيبدأ العد التنازلي بعد 3 ثوانٍ**")

            # Store the message ID for later deletion
            countdown_messages[event.chat_id] = countdown_message.id

            # Wait for 1 second and update the message
            await asyncio.sleep(1)
            await countdown_message.edit("⏳** سيبدأ العد التنازلي بعد 2 ثانيتين**")


            # Wait for the final second before starting the countdown
            await asyncio.sleep(1)
            
            # Update the message to start the countdown
            countdown_message = await countdown_message.edit(f"⏳** سيبدأ العد التنازلي بعد 1 ثانية**")
            
            # Countdown loop
            while total_seconds > 0:
                minutes, seconds = divmod(total_seconds, 60)
                new_text = f"⏳** {minutes:02}:{seconds:02} متبقية**"
                await asyncio.sleep(1)
                total_seconds -= 1

                try:
                    if new_text != countdown_message.text:
                        await countdown_message.edit(new_text)
                except MessageNotModifiedError:
                    pass
            
            await countdown_message.edit("⏳ **الوقت انتهى!**")
            # Optionally remove the countdown message after completion
            # await countdown_message.delete()

        # Start the timer task
        active_timers[event.chat_id] = asyncio.create_task(timer_task())
        
    except (ValueError, IndexError):
        await event.reply("⚠️ استخدم الصيغة الصحيحة: time (عدد الدقائق)")

@client.on(events.NewMessage(from_users='me', pattern='.stop'))
async def stop_timers(event):
    if event.chat_id in active_timers:
        # Cancel the active timer
        active_timers[event.chat_id].cancel()
        del active_timers[event.chat_id]
        
        # Delete the countdown message if it exists
        if event.chat_id in countdown_messages:
            try:
                await client.delete_messages(event.chat_id, countdown_messages[event.chat_id])
                del countdown_messages[event.chat_id]
            except Exception as e:
                print(f"Error deleting countdown message: {e}")

        # Send the confirmation message
        stop_message = await event.reply("✅ تم إيقاف جميع العدادات التنازلية.")
        
        # Wait 3 seconds before deleting the message
        await asyncio.sleep(3)
        await stop_message.delete()
    else:
        # Send the no active timer message
        no_timer_message = await event.reply("❌ لا توجد عدادات تنازلية نشطة لإيقافها.")
        
        # Wait 3 seconds before deleting the message
        await asyncio.sleep(3)
        await no_timer_message.delete()

@client.on(events.NewMessage(from_users='me', pattern='.الاوامر'))
async def show_commands(event):
    commands_text = (
        """📜✨ **أوامر البوت** ✨📜

1️⃣ **add (الكلمة المفتاحية) الرد**  
➖ لإضافة رد مع صورة يجب الرد على الصورة وكتابة الامر مع الكلمة المفتاحية و لإضافة فقط رد بدون صورة قم بالرد على رسالة وارسل الامر مع الكلمة المفتاحية و الرد

2️⃣ **del الكلمة المفتاحية**  
➖ لحذف رد تلقائي مرتبط بالكلمة المفتاحية.  
🔹 **مثال:** del مرحبا  

3️⃣ **الردود**  
➖ عرض جميع الردود التي تم إضافتها باستخدام الأمر add.  

4️⃣ **time (عدد الدقائق)**  
➖ لبدء عداد تنازلي لعدد الدقائق المحددة.  
🔹 **مثال:** time (5) لبدء عداد تنازلي لمدة 5 دقائق.

5️⃣ **stop**  
➖ لإيقاف جميع العدادات التنازلية النشطة

6️⃣ **name (الاسم الجديد)**  
➖ لتغيير اسم الحساب إلى الاسم الجديد المحدد.  
🔹 **مثال:** name (اسم جديد) لتحديث اسم الحساب.

7️⃣ **مسح (عدد الرسائل)**  
➖ لحذف عدد محدد من الرسائل في المحادثة.  
🔹 **مثال:** مسح (10) لحذف آخر 10 رسائل في المحادثة.

8️⃣ **نشر (عدد المجموعات) الرسالة**  
➖ لنشر رسالة في عدد محدد من المجموعات.  
🔹 **مثال:** نشر (5) مرحبا جميعاً لنشر رسالة في 5 مجموعات.

9️⃣ **حذف**  
➖ لحذف جميع الرسائل التي تم نشرها باستخدام الأمر نشر.  

🔟 **الرسائل**  
➖ لعرض الرسائل وكم مجموعة تم نشر الرسالة فيها باستخدام الأمر نشر.  

🔄 **الاوامر**  
➖ لعرض قائمة بجميع أوامر البوت وكيفية استخدامها.  

🔗 **اضافة قناة (رابط القناة)**  
➖ لتعيين رابط قناة يمكن التحقق من اشتراك المستخدمين فيها قبل التفاعل معهم.  حيث لا يمكن للمستخدم الاخر التحدث معك الى بعد الاشتراك في القناة
🔹 **مثال:** اضافة قناة https://t.me/example_channel لتعيين قناة تحقق من اشتراك المستخدمين فيها.

⏱️ **تفعيل الوقت**  
➖ لتفعيل الاسم الوقتي

⏳ **تعطيل الوقت**  
➖ لتعطيل الاسم الوقتي

🔕 **كتم**  
➖ لكتم مستخدم  

🗣️ **سماح**  
➖ لإلغاء كتم مستخدم والسماح له بالتحدث معك

👥 **المكتومين**  
➖ لعرض قائمة بالمستخدمين المكتومين.

**ارسال (عدد الدقائق) (عدد المرات)**
➖ 🔄: يرسل الرسالة بشكل دوري على حسب عدد من الدقائق وعدد من المرات المحددة.

**نشر متعدد (عدد الدقائق)**
➖🔁: ينشر الرسالة بشكل دوري كل عدد من الدقائق إلى ما لا نهاية بدون تحديد عدد مرات النشر.

**ايقاف الارسال**
 ➖🚫: يوقف جميع عمليات النشر النشطة في المحادثة.

**يوتيوب (عنوان الفيديو)**
➖🎥: يبحث عن فيديو على YouTube بناءً على النص المدخل ويرسل رابط الفيديو.

**❲اوامر التسليه❳**

**متت

انتحار

شرير**

📋 **لنسخ الأوامر، اضغط على النص أدناه**

🗑 **ازالة القناة**
➖لحذف القناة التي تم تعينها للأشتراك الاجباري

**❲**`add (الكلمة المفتاحية) الرد` **❳**
**❲** `del الكلمة المفتاحية` **❳**
**❲** `time (عدد الدقائق)` **❳**
**❲** `stop` **❳**
**❲** `name (الاسم الجديد)` **❳**
**❲** `مسح (عدد الرسائل)` **❳**
**❲** `نشر (عدد المجموعات) الرسالة` **❳**
**❲** `حذف` **❳**
**❲** `الرسائل` **❳**
**❲** `الاوامر` **❳**
**❲** `اضافة قناة (رابط القناة)` **❳**
**❲** `تفعيل الوقت` **❳**
**❲** `تعطيل الوقت` **❳**
**❲** `كتم` **❳**
**❲** `سماح` **❳**
**❲** `المكتومين` **❳**
**❲** `الردود` **❳**
**❲** `ازالة القناة` **❳**
*❲** `ارسال (عدد الدقائق) (عدد المرات)` **❳***
❲** `نشر متعدد (عدد الدقائق)` **❳**
**❲** `ايقاف الارسال` **❳**
**❲** `يوتيوب (عنوان الفيديو)` **❳**
**❲** `متت` **❳**
**❲** `انتحار` **❳**
**❲** `شرير` **❳**
**ملاحظة**"
**قبل استخدام ايه امر اجعل قبله علامة ❲.❳**

**المطور : @z1_xa**
**القناة : @yqyqy66**
"""
    )
    await event.reply(commands_text)

@client.on(events.NewMessage(from_users='me', pattern='.name'))
async def set_account_name(event):
    global account_name
    try:
        # Extract the new account name from the message
        command, new_name = event.raw_text.split(' ', 1)
        account_name = new_name.split('(', 1)[1].split(')')[0].strip()
        
        # Update the account name immediately
        iraq_tz = pytz.timezone('Asia/Baghdad')
        now = datetime.datetime.now(iraq_tz)
        current_time = superscript_time(now.strftime("%I:%M"))
        new_username = f"{account_name} - {current_time}"
        
        try:
            await client(UpdateProfileRequest(first_name=new_username))
            await event.reply(f"✅ تم تغيير اسم الحساب إلى {new_username}")
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)
            await client(UpdateProfileRequest(first_name=new_username))
            await event.reply(f"✅ تم تغيير اسم الحساب إلى {new_username}")
        except Exception as e:
            await event.reply(f"⚠️ حدث خطأ أثناء تغيير الاسم: {e}")
    except ValueError:
        await event.reply("⚠️ استخدم الصيغة: name (الاسم الجديد)")

@client.on(events.NewMessage(from_users='me', pattern='.مسح'))
async def delete_messages(event):
    try:
        # استخراج عدد الرسائل المراد حذفها من الرسالة
        command, num_str = event.raw_text.split(' ', 1)
        num_messages = int(num_str.strip('()'))
        
        if num_messages <= 0:
            await event.reply("⚠️ يجب أن يكون عدد الرسائل المراد حذفها أكبر من صفر.")
            return
        
        # الحصول على معرفات الرسائل التي سيتم حذفها
        messages = await client.get_messages(event.chat_id, limit=num_messages)
        message_ids = [msg.id for msg in messages]
        
        if message_ids:
            await client(DeleteMessagesRequest(id=message_ids))
            confirmation_message = await event.reply(f"✅ تم مسح {num_messages} رسالة.")
            
            # الانتظار لمدة 3 ثوانٍ ثم حذف رسالة التأكيد
            await asyncio.sleep(2)
            await client(DeleteMessagesRequest(id=[confirmation_message.id]))
        else:
            await event.reply("⚠️ لم يتم العثور على رسائل للحذف.")
    except (ValueError, IndexError):
        await event.reply("⚠️ استخدم الصيغة: مسح (عدد الرسائل)")
    except Exception as e:
        await event.reply(f"⚠️ حدث خطأ أثناء حذف الرسائل: {e}")

@client.on(events.NewMessage(from_users='me', pattern='.نشر'))
async def publish_message(event):
    try:
        # Extract the number of groups and the message from the message
        command, args = event.raw_text.split(' ', 1)
        num_groups, message = args.split('(', 1)[1].split(')')[0], args.split(')', 1)[1].strip()
        num_groups = int(num_groups)
        
        # Fetch groups where the bot is a member
        dialogs = await client.get_dialogs()
        groups = [dialog for dialog in dialogs if dialog.is_group]
        
        if len(groups) < num_groups:
            await event.reply(f"⚠️ عدد المجموعات المتاحة أقل من {num_groups}.")
            return
        
        # Publish the message to the specified number of groups
        published_message_ids = []
        for group in groups[:num_groups]:
            msg = await client.send_message(group, message)
            published_message_ids.append((group.id, msg.id))
        
        # Save the published message details
        published_messages.append({
            'message': message,
            'group_ids': [group.id for group in groups[:num_groups]],
            'message_ids': published_message_ids
        })
        with open(published_messages_file, 'wb') as f:
            pickle.dump(published_messages, f)
        
        await event.reply(f"✅ تم نشر الرسالة في {num_groups} مجموعة.")
    except (ValueError, IndexError):
        await event.reply("⚠️ استخدم الصيغة: نشر (عدد المجموعات) الرسالة")
    except Exception as e:
        await event.reply(f"⚠️ حدث خطأ أثناء نشر الرسالة: {e}")

@client.on(events.NewMessage(from_users='me', pattern='.حذف'))
async def delete_published_messages(event):
    try:
        if not published_messages:
            await event.reply("❌ لا توجد رسائل منشورة لحذفها.")
            return
        
        # Delete all published messages
        for entry in published_messages:
            for group_id, msg_id in entry['message_ids']:
                try:
                    await client(DeleteMessagesRequest(id=[msg_id], revoke=True))
                except Exception as e:
                    print(f"Error deleting message {msg_id} in group {group_id}: {e}")
        
        # Clear the published messages list
        published_messages.clear()
        with open(published_messages_file, 'wb') as f:
            pickle.dump(published_messages, f)
        
        await event.reply("✅ تم حذف جميع الرسائل المنشورة.")
    except Exception as e:
        await event.reply(f"⚠️ حدث خطأ أثناء حذف الرسائل المنشورة: {e}")

# تحميل قائمة المستخدمين المكتومين من الملف أو إنشاء قائمة جديدة إذا لم تكن موجودة
if os.path.exists(muted_users_file):
    with open(muted_users_file, 'rb') as f:
        muted_users = pickle.load(f)
else:
    muted_users = set()

# أوامر الكتم والسماح وعرض المكتومين
@client.on(events.NewMessage(from_users='me', pattern='.كتم'))
async def mute_user(event):
    if event.is_private:
        muted_users.add(event.chat_id)
        with open(muted_users_file, 'wb') as f:
            pickle.dump(muted_users, f)
        await event.reply("✅ **تم كتم المستخدم**")
    else:
        await event.reply("⚠️ يمكن استخدام هذا الأمر في المحادثات الخاصة فقط.")

@client.on(events.NewMessage(from_users='me', pattern='.سماح'))
async def unmute_user(event):
    if event.is_private and event.chat_id in muted_users:
        muted_users.remove(event.chat_id)
        with open(muted_users_file, 'wb') as f:
            pickle.dump(muted_users, f)
        await event.reply("✅ تم فك الكتم عن هذا المستخدم.")
    else:
        await event.reply("⚠️ هذا المستخدم ليس في قائمة المكتومين")

@client.on(events.NewMessage(from_users='me', pattern='.المكتومين'))
async def show_muted_users(event):
    if muted_users:
        muted_users_list = "\n".join([str(user_id) for user_id in muted_users])
        await event.reply(f"📋 المستخدمون المكتومون:\n{muted_users_list}")
    else:
        await event.reply("❌ لا يوجد مستخدمون مكتومون حالياً.")

# حذف الرسائل من المستخدمين المكتومين
@client.on(events.NewMessage(incoming=True))
async def delete_muted_user_messages(event):
    if event.is_private and event.chat_id in muted_users:
        await client.delete_messages(event.chat_id, [event.id])

@client.on(events.NewMessage(from_users='me', pattern='.الرسائل'))
async def show_published_messages(event):
    if not published_messages:
        await event.reply("❌ لا توجد رسائل منشورة.")
        return
    
    response_text = "📋 الرسائل المنشورة:\n"
    for i, entry in enumerate(published_messages, 1):
        response_text += f"🔹 الرسالة {i}: {entry['message']}\n"
        response_text += f"🔸 عدد المجموعات: {len(entry['group_ids'])}\n\n"
    
    await event.reply(response_text)

async def main():
    await client.start()
    await update_username()

with client:
    client.loop.run_until_complete(main())