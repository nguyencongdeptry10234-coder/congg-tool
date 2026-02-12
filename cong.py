import multiprocessing
import requests
import os
import re
import time
import random
import json
import pyfiglet

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_main_banner():
    banner = pyfiglet.figlet_format('' + f"Thời gian: {time.strftime('%I:%M %p, %d/%m/%Y')}")
    return banner

def create_instructions():
    instructions = """
"""
    return instructions

def AnkLaDontCry(cookie_str):
    cookies = {}
    cookie_items = cookie_str.split(';')
    for item in cookie_items:
        parts = item.strip().split('=', 1)
        if len(parts) == 2:
            cookies[parts[0].strip()] = parts[1].strip()
    return cookies

def get_du_lieu(ck):
    try:
        response = requests.get("https://m.facebook.com/", cookies=AnkLaDontCry(ck))
        fb_dtsg = response.text.split('<input type="hidden" name="fb_dtsg" value="')[1].split('"')[0]
        return fb_dtsg
    except Exception as e:
        print(f"Có lỗi không xác định: {e}")
        return None

def check_live(cookie):
    try:
        if 'c_user=' not in cookie:
            return {"status": "failed", "msg": "Cookie không chứa user_id"}
        
        user_id = cookie.split('c_user=')[1].split(';')[0]
        url = f"https://graph2.facebook.com/v3.3/{user_id}/picture?redirect=0"
        response = requests.get(url, timeout=30)
        check_data = response.json()

        if not check_data.get('data', {}).get('height') or not check_data.get('data', {}).get('width'):
            return {"status": "failed", "msg": "Cookie không hợp lệ"}

        headers = {
            'authority': 'm.facebook.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'vi-VN,vi;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': cookie,
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"0.1.0"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        }

        profile_response = requests.get(f'https://m.facebook.com/profile.php?id={user_id}', headers=headers, timeout=30)
        name = profile_response.text.split('<title>')[1].split('<')[0].strip()

        return {
            "status": "success",
            "name": name,
            "user_id": user_id,
            "msg": "successful"
        }
    except Exception as e:
        return {"status": "failed", "msg": f"Lỗi xảy ra: {str(e)}"}

def load_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if not content.strip():
            raise Exception(f"File {file_path} trống!")
        return content
    except Exception as e:
        raise Exception(f"Lỗi đọc file {file_path}: {str(e)}")

def parse_selection(input_str, max_index):
    try:
        numbers = [int(i.strip()) for i in input_str.split(',')]
        return [n for n in numbers if 1 <= n <= max_index]
    except:
        print("Định dạng không hợp lệ!")
        return []

def idelay(time_sec):
    while time_sec:
        mins, secs = divmod(time_sec, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(f' Vui lòng chờ {timeformat}', end='\r')
        time.sleep(1)
        time_sec -= 1
    print(" Code By Ank La DontCry ")

def get_thread_list(cookie, user_id, fb_dtsg):
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    ]
    
    headers = {
        'Cookie': cookie,
        'User-Agent': random.choice(user_agents),
        'Accept': '*/*',
        'Accept-Language': 'vi-VN,vi;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.facebook.com',
        'Referer': 'https://www.facebook.com/',
        'Host': 'www.facebook.com',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'X-FB-Friendly-Name': 'MessengerThreadListQuery'
    }
    
    form_data = {
        "av": user_id,
        "__user": user_id,
        "__a": "1",
        "__req": "1b",
        "__hs": "19234.HYP:comet_pkg.2.1..2.1",
        "dpr": "1",
        "__ccg": "EXCELLENT",
        "__rev": "1015919737",
        "fb_dtsg": fb_dtsg,
        "jazoest": "null",
        "lsd": "null",
        "__spin_r": "",
        "__spin_b": "trunk",
        "__spin_t": str(int(time.time())),
        "queries": json.dumps({
            "o0": {
                "doc_id": "3336396659757871",
                "query_params": {
                    "limit": 100,
                    "before": None,
                    "tags": ["INBOX"],
                    "includeDeliveryReceipts": False,
                    "includeSeqID": True,
                }
            }
        })
    }
    
    try:
        response = requests.post(
            'https://www.facebook.com/api/graphqlbatch/',
            data=form_data,
            headers=headers,
            timeout=15
        )
        
        if response.status_code != 200:
            return {"error": f"HTTP Error: {response.status_code}"}
        
        response_text = response.text.split('{"successful_results"')[0]
        data = json.loads(response_text)
        
        if "o0" not in data:
            return {"error": "Không tìm thấy dữ liệu thread list"}
        
        if "errors" in data["o0"]:
            return {"error": f"Facebook API Error: {data['o0']['errors'][0]['summary']}"}
        
        threads = data["o0"]["data"]["viewer"]["message_threads"]["nodes"]
        thread_list = []
        
        for thread in threads:
            if not thread.get("thread_key") or not thread["thread_key"].get("thread_fbid"):
                continue
            thread_list.append({
                "thread_id": thread["thread_key"]["thread_fbid"],
                "thread_name": thread.get("name", "Không có tên")
            })
        
        return {
            "success": True,
            "thread_count": len(thread_list),
            "threads": thread_list
        }
        
    except json.JSONDecodeError as e:
        return {"error": f"Lỗi parse JSON: {str(e)}"}
    except Exception as e:
        return {"error": f"Lỗi không xác định: {str(e)}"}

def start_spam(cookie, account_name, user_id, thread_ids, thread_names, file_names, delay):
    try:
        fb_dtsg = get_du_lieu(cookie)
        if not fb_dtsg:
            raise Exception("Không thể lấy fb_dtsg")
        
        for namefile in file_names:
            with open(namefile, "r", encoding='utf-8') as file:
                message_text = file.read()
                for thread_id, thread_name in zip(thread_ids, thread_names):
                    while True:
                        ts = int(time.time() * 1000)
                        data = {
                            'thread_fbid': thread_id,
                            'action_type': 'ma-type:user-generated-message',
                            'body': message_text,
                            'client': 'mercury',
                            'author': f'fbid:{user_id}',
                            'timestamp': ts,
                            'source': 'source:chat:web',
                            'offline_threading_id': ts,
                            'message_id': ts,
                            'ephemeral_ttl_mode': '',
                            '__user': user_id,
                            '__a': '1',
                            '__req': '1b',
                            '__rev': '1015919737',
                            'fb_dtsg': fb_dtsg
                        }

                        headers = {
                            'Cookie': cookie,
                            'User-Agent': 'python-http/0.27.0',
                            'Accept': '*/*',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Connection': 'keep-alive',
                            'Content-Type': 'application/x-www-form-urlencoded',
                            'Origin': 'https://www.facebook.com',
                            'Host': 'www.facebook.com',
                            'Referer': f'https://www.facebook.com/messages/t/{thread_id}'
                        }

                        response = requests.post("https://www.facebook.com/messaging/send/", headers=headers, data=data)
                        if response.status_code == 200:
                            print(f'[Cookie: {account_name}] BOX: {thread_name} (ID: {thread_id}) | FILE NGÔN: {namefile} | SPAM THÀNH CÔNG!')
                        else:
                            print(f'[Cookie: {account_name}] STATUS: {response.status_code}')
                        
                        idelay(delay)
    except Exception as e:
        print(f"Lỗi tài khoản {account_name}: {str(e)}")

def start_multiple_accounts():
    clear()
    print(create_main_banner())
    print(create_instructions())
    
    try:
        num_accounts = int(input("Nhập số lượng tài khoản Facebook muốn chạy: "))
        if num_accounts < 1:
            print("Số lượng tài khoản phải lớn hơn 0. Thoát chương trình.")
            return
    except ValueError:
        print("Số lượng tài khoản phải là số nguyên. Thoát chương trình.")
        return

    processes = []
    for i in range(num_accounts):
        print(f"\nNhập thông tin cho tài khoản {i+1}\n")
        cookie = input("Nhập Cookie: \n").strip()
        if not cookie:
            print("Cookie không được để trống. Bỏ qua tài khoản này.")
            continue
        
        cl = check_live(cookie)
        if cl["status"] == "success":
            print(f"Tài khoản Facebook: {cl['name']} (ID: {cl['user_id']}) - Cookie Sống!")
        else:
            print(f"Lỗi: {cl['msg']}. Bỏ qua tài khoản này.")
            continue

        fb_dtsg = get_du_lieu(cookie)
        if not fb_dtsg:
            print("Không thể lấy fb_dtsg. Bỏ qua tài khoản này.")
            continue

        print(f"\nĐang lấy danh sách box cho tài khoản {cl['name']}...")
        result = get_thread_list(cookie, cl['user_id'], fb_dtsg)
        
        if "error" in result:
            print(f"Lỗi: {result['error']}. Bỏ qua tài khoản này.")
            continue
        
        threads_list = result['threads']
        if not threads_list:
            print("Không tìm thấy box nào. Bỏ qua tài khoản này.")
            continue
        
        print(f"\nTìm thấy {len(threads_list)} box:")
        print("=" * 60)
        for idx, thread in enumerate(threads_list, 1):
            thread_name = thread.get('thread_name', 'Không có tên') or 'Không có tên'
            display_name = f"{thread_name[:45]}{'...' if len(thread_name) > 45 else ''}"
            print(f"{idx}. {display_name}")
            print(f"   ID: {thread['thread_id']}")
            print("-" * 55)
        
        raw = input("Nhập số thứ tự box muốn chạy (VD: 1,3): ")
        selected = parse_selection(raw, len(threads_list))
        if not selected:
            print("Không chọn box nào! Bỏ qua tài khoản này.")
            continue
        
        selected_ids = [threads_list[i - 1]['thread_id'] for i in selected]
        selected_names = [threads_list[i - 1]['thread_name'] or 'Không có tên' for i in selected]
        
        file_names = []
        sst2 = 0
        print("\nNhập danh sách file chứa nội dung...")
        while True:
            sst2 += 1
            name_file = input(f"Nhập tên file .txt chứa ngôn lần thứ {sst2} (VD: nd.txt) hoặc nhập 'xong': ").strip()
            if name_file.lower() == 'xong':
                break
            if name_file:
                try:
                    message_text = load_file(name_file)
                    print(f"Đã tải nội dung từ {name_file}")
                    file_names.append(name_file)
                except Exception as e:
                    print(f"Lỗi: {str(e)}. Bỏ qua file này.")
                    continue
        
        if not file_names:
            print("Không nhập file nội dung nào. Bỏ qua tài khoản này.")
            continue

        try:
            delay = int(input("Nhập delay giữa các lần gửi (giây): "))
            if delay < 1:
                print("Delay phải là số nguyên dương. Bỏ qua tài khoản này.")
                continue
        except ValueError:
            print("Delay phải là số nguyên. Bỏ qua tài khoản này.")
            continue
        
        print(f"\nKhởi động treo ngôn cho tài khoản {cl['name']}...")
        p = multiprocessing.Process(
            target=start_spam,
            args=(cookie, cl['name'], cl['user_id'], selected_ids, selected_names, file_names, delay)
        )
        processes.append(p)
        p.start()
    
    if not processes:
        print("Không có tài khoản nào được khởi động. Thoát chương trình.")
        return
    
    print("\nAnk La Dontcry")
    print("Nhấn Ctrl+C để dừng.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nĐã dừng tool")
        for p in processes:
            p.terminate()
        os._exit(0)

if __name__ == "__main__":
    start_multiple_accounts()
