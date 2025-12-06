import time
import pyperclip

LOG_FILE = "clipboard_log.txt"

def main():
    last_text = pyperclip.paste()

    print("Clipboard logger started. Press Ctrl+C to stop.")

    i = 1
    while True:
        try:
            text = pyperclip.paste()
            if text != last_text and text.strip() != "":
                print(f"[{text}], # {i}")
                last_text = text
                i += 1
            time.sleep(0.2)
        except KeyboardInterrupt:
            print("\nStopped.")
            break
        except Exception as e:
            print("Error:", e)
            time.sleep(1)

if __name__ == "__main__":
    main()
