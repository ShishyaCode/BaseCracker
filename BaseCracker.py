import base64
import re
import zlib
import os
import io
import zipfile
import requests,shutil,pyfiglet,time




red = "\033[1m\033[31m"
green = "\033[1m\033[32m"
yellow = "\033[1m\033[33m"
blue = "\033[1m\033[34m"
ORANGE = '\x1b[38;5;208m'  
WHITE = '\x1b[1;37m'
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
RESET = '\033[0m'

import pyfiglet
os.system('cls' if os.name=='nt' else 'clear')
def cracker():
    font_name = "small" 
    ascii_art = pyfiglet.figlet_format("BaseCracker", font=font_name)
    border_top = "_" * (len(max(ascii_art.split('\n'), key=len)) + 6)
    border_bottom = "-" * (len(max(ascii_art.split('\n'), key=len)) + 6)
    
    print(red + border_top)
    for line in ascii_art.split('\n'):
        print(f"# {line.center(len(border_top)-4)} #")  
    print(red + border_bottom)

cracker()
print(f"{YELLOW}Continuing in...", end='', flush=True)
for i in range(5, 0, -1):
    print(f"\r{YELLOW}Continuing in... {green}{i}  {RESET}", end='', flush=True)
    time.sleep(1)


os.system('cls' if os.name=='nt' else 'clear')
os.system('cls' if os.name=='nt' else 'clear')

print(f'''
{BLUE}┌─────────────────────────────────────────────────────────
{BLUE}│{RESET}                                                   
{BLUE}│{RESET}   👨‍💻 {CYAN}Developer       {WHITE}: {GREEN}Shishya                          
{BLUE}│{RESET}   📢 {CYAN}Telegram Channel {WHITE}: {YELLOW}@shishyacode                    
{BLUE}│{RESET}   💻 {CYAN}GitHub           {WHITE}: {MAGENTA}github.com/shishyacode       
{BLUE}│{RESET}   📸 {CYAN}Instagram        {WHITE}: {RED}instagram.com/shishyacode   
{BLUE}│{RESET}                                                      
{BLUE}└────────────────────────────────────────────────────────
''')

PATTERNS = [
    r"'(.*?)'",
    r"(.*?)",
    r'"(.*?)"',
    r'"""(.*?)"""',
    r"'''(.*?)'''",
    r"b'''(.*?)'''",
    r'b"""(.*?)"""',
    r"b'(.*?)'",
    r'b"(.*?)"',
    r'base64\.b64decode\(\s*[\'"]([^\'"]+)[\'"]\s*\)',
    r'base64\.b64decode\(\s*b[\'"]([^\'"]+)[\'"]\s*\)',
    r'base64\.b85decode\(\s*[\'"]([^\'"]+)[\'"]\s*\)',
    r'base64\.b85decode\(\s*b[\'"]([^\'"]+)[\'"]\s*\)',
    r'(exec|eval|compile)\(\s*base64\.b64decode\(\s*[\'"]([^\'"]+)[\'"]\s*\)\s*\)',
    r'(exec|eval|compile)\(\s*base64\.b85decode\(\s*[\'"]([^\'"]+)[\'"]\s*\)\s*\)',
    r'base64\.b64decode\(\s*base64\.b64decode\(\s*[\'"]([^\'"]+)[\'"]\s*\)\s*\)',
    r'base64\.b85decode\(\s*base64\.b85decode\(\s*[\'"]([^\'"]+)[\'"]\s*\)\s*\)',
    r'base64\.(b16decode|b32decode|b64decode|b85decode|urlsafe_b64decode)\(\s*[\'"]([^\'"]+)[\'"]\s*\)',
    r'base64\.(b16decode|b32decode|b64decode|b85decode|urlsafe_b64decode)\(\s*b[\'"]([^\'"]+)[\'"]\s*\)',
    r'base64\.(b16decode|b32decode|b64decode|b85decode|urlsafe_b64decode)\(\s*base64\.(b16decode|b32decode|b64decode|b85decode|urlsafe_b64decode)\(\s*[\'"]([^\'"]+)[\'"]\s*\)\s*\)',
    r'(exec|eval|compile)\(\s*base64\.(b16decode|b32decode|b64decode|b85decode|urlsafe_b64decode)\(\s*[\'"]([^\'"]+)[\'"]\s*\)\s*\)',
    r'(exec|eval|compile)\(\s*base64\.(b16decode|b32decode|b64decode|b85decode|urlsafe_b64decode)\(\s*b[\'"]([^\'"]+)[\'"]\s*\)\s*\)',
    r'base64\.(b64decode|b85decode)\(\s*base64\.(b64decode|b85decode)\(\s*base64\.(b64decode|b85decode)\(\s*[\'"]([^\'"]+)[\'"]\s*\)\s*\)\s*\)',
]

def extract_encoded_strings(file_content):
    matches = []
    for pattern in PATTERNS:
        for match in re.findall(pattern, file_content, re.DOTALL):
            if isinstance(match, tuple):
                matches.append(match[-1])
            else:
                matches.append(match)
    return matches

def is_mostly_printable(s, threshold=0.9):
    text = s.strip()
    if not text:
        return False
    printable_count = sum(c.isprintable() for c in text)
    return (printable_count / len(text)) >= threshold

def try_all_decodes(encoded_str, output_prefix="decoded_output"):
    candidates = []
    decoding_methods = [
        ('base64', base64.b64decode),
        ('base85', base64.b85decode),
        ('base32', base64.b32decode),
        ('base16', lambda s: base64.b16decode(s, casefold=True)),
    ]

    likely_zip = "UEsDb" in encoded_str  

    for method_name, decoder in decoding_methods:
        for direction in ['normal', 'reversed']:
            try:
                data = encoded_str[::-1] if direction == 'reversed' else encoded_str
                decoded_bytes = decoder(data.encode())

                # Check if it's a ZIP archive
                if decoded_bytes[:4] == b'PK\x03\x04' or likely_zip:
                    zip_output_dir = f"{output_prefix}_zip_{method_name}_{direction}"
                    os.makedirs(zip_output_dir, exist_ok=True)

                    try:
                        with zipfile.ZipFile(io.BytesIO(decoded_bytes), 'r') as zf:
                            zf.extractall(zip_output_dir)

                        return {
                            'text': f'# ZIP archive extracted to {zip_output_dir}',
                            'method': method_name,
                            'direction': direction,
                            'source': 'zip',
                            'zip_output_dir': zip_output_dir
                        }
                    except zipfile.BadZipFile:
                        continue  # Wasn't actually a zip file

                # Try to decompress via zlib
                try:
                    decompressed = zlib.decompress(decoded_bytes)
                    decoded_str = decompressed.decode('utf-8', errors='ignore')
                    source = 'zlib-compressed'
                except Exception:
                    decoded_str = decoded_bytes.decode('utf-8', errors='ignore')
                    source = 'plain'

                if is_mostly_printable(decoded_str):
                    candidates.append({
                        'text': decoded_str,
                        'method': method_name,
                        'direction': direction,
                        'source': source
                    })
            except Exception:
                continue

    if candidates:
        return sorted(candidates, key=lambda c: (c['source'] == 'plain', len(c['text'])), reverse=True)[0]
    return None

def checker(token, chat_id):
    msg = "😊 Heyy Thanks for using BaseCracker\n\n ~ a special type decoder to decode all Base Encryption\nPlease support: @ShishyaCode || @ShishyaPy"

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "☠️ Coder ", "url": "https://t.me/shishyapy"},  
                {"text": "⛔️ Channel", "url": "https://t.me/shishyacode"}     
            ]
        ]
    }

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": msg,
        "reply_markup": keyboard 
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status() 
        
    except requests.exceptions.RequestException as e:
        raise ValueError("❌ Failed to send message. Start the bot first or check your credentials.") from e




def create_unique_output_dir(base_name="ShishyaDec"):
    dir_name = base_name
    count = 1
    while os.path.exists(dir_name):
        count += 1
        dir_name = f"{base_name}{count}"
    os.makedirs(dir_name)
    return dir_name
def decode_script_file():
    input_file = input(blue + "📂 Enter the encoded script filename (e.g., script.py): " + yellow).strip()

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            contents = f.read()

        encoded_strings = extract_encoded_strings(contents)
        if not encoded_strings:
            raise ValueError(red + "No encoded strings found in the file.")

        output_dir = create_unique_output_dir("ShishyaDec")
        x = 0

        print(f"\n{CYAN}What would you like to do with decoded files?")
        print(f"{GREEN}1.{RESET} Save files locally")
        print(f"{GREEN}2.{RESET} Send files to Telegram")

        choice = input(f"{YELLOW}Enter your choice (1 or 2): {RESET}").strip()
        if choice =='2':
            TELEGRAM_BOT_TOKEN = input(f"{RED}Enter telegram Token: {YELLOW}")
            TELEGRAM_USER_ID = input(f"{RED}Enter Chat ID: {YELLOW}")
            checker(token=TELEGRAM_BOT_TOKEN,chat_id=TELEGRAM_USER_ID)

        for i, encoded in enumerate(encoded_strings):
            result = try_all_decodes(encoded, output_prefix=os.path.join(output_dir, f'chunk{i+1}'))
            if result:
                if result['source'] == 'zip':
                    print(f"{green}\n✅ ZIP archive decoded from chunk #{i+1} ({result['method'].upper()}, {result['direction']})")
                    print(f"{green}📁 Extracted to folder: {result['zip_output_dir']}")
                    if choice == "2":
                        zip_path = shutil.make_archive(result['zip_output_dir'], 'zip', result['zip_output_dir'])
                        send_file_to_telegram(TELEGRAM_BOT_TOKEN=TELEGRAM_BOT_TOKEN,TELEGRAM_USER_ID=TELEGRAM_USER_ID,file_path=zip_path, caption=f"ZIP archive from chunk #{i+1}")
                        
                else:
                    out_name = os.path.join(output_dir, f'decoded_{i+1}.py')
                    with open(out_name, 'w', encoding='utf-8') as out_f:
                        out_f.write(result['text'])
                    print(f"\n✅ Decoded chunk #{i+1} ({result['method'].upper()}, {result['direction']}, {result['source']})")
                    print(f"💾 Output saved to: {out_name}")
                    if choice == "2":
                        send_file_to_telegram(TELEGRAM_BOT_TOKEN=TELEGRAM_BOT_TOKEN,TELEGRAM_USER_ID=TELEGRAM_USER_ID,file_path=out_name, caption=f"Decoded chunk #{i+1}")
                        os.remove(out_name)
                        
            else:
                x += 1

        print(f"{blue}\n🧮 Total decode failures: {x}")
        print(f"{yellow}📂 All decoded files are saved in: {output_dir}")

    except Exception as e:
        print(f"\n❌ Error: {e}")


def send_file_to_telegram(TELEGRAM_BOT_TOKEN,TELEGRAM_USER_ID,file_path, caption=None):


    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
        full_caption = (caption or "") + "\n\nPlease support @ShishyaCode || @ShishyaPy"
        with open(file_path, 'rb') as file_data:
            response = requests.post(url, data={
                'chat_id': TELEGRAM_USER_ID,
                'caption': full_caption.strip()
            }, files={'document': file_data})
        if response.status_code == 200:
            print(f"📤 Sent '{file_path}' to Telegram successfully.")
        else:
            print(f"❌ Failed to send '{file_path}' to Telegram: {response.text}")
    except Exception as e:
        print(f"❌ Error sending file to Telegram: {e}")



if __name__ == "__main__":
    decode_script_file()
