import asyncio
import httpx
from tkinter import Tk, Button, Label, StringVar, DoubleVar
from tkinter.ttk import Progressbar

async def download(url: str, filename: str, progress_var, label_var):

    try:
        with open(filename, 'wb') as f:
            async with httpx.AsyncClient(timeout=30.0) as client:
                async with client.stream('GET', url) as r:
                    r.raise_for_status()
                    total = int(r.headers.get('content-length', 0)) or None
                    downloaded = 0

                    async for chunk in r.aiter_bytes():
                        f.write(chunk)
                        downloaded += len(chunk)
                        progress = (downloaded / total) * 100 if total else 0
                        progress_var.set(progress)
                        label_var.set(f"{filename}: {progress:.2f}% completed")
                        await asyncio.sleep(0.01)  # Allow UI updates
    except Exception as e:
        label_var.set(f"Error downloading {filename}: {e}")
        raise

def start_download(urls):
    asyncio.create_task(do_downloads(urls))

async def do_downloads(urls):
    tasks = []
    for i, (url, filename) in enumerate(urls):
        progress_var = progress_vars[i]
        label_var = label_vars[i]
        tasks.append(download(url, filename, progress_var, label_var))
    await asyncio.gather(*tasks)

# Tkinter GUI Setup
root = Tk()
root.title("Download Manager")
root.geometry("400x300")
u = "https://download938.mediafire.com/yxh4m3yjv5egyomxam4ctv8CB6pBrKWvj6Gb-vaTGIJC2ze2fMFv5nOHQWgqFtDSaccW8MLyrrONe1UdB8XfvMxTWr_4RxY3oG-xl8gkAFiEP2mMcttKOI0i0cQ5kfdtz6OIQ8x4k90zNfqkYtC77UpYlMNweTgHUyt9nG_YWQwb/qob85dyzjpiqfdn/download.rar"
# Create progress bars and labels
urls = [
    (u, "file1.zip"),
    (u, "file2.zip"),
    (u, "file3.zip"),
]

progress_vars = []
label_vars = []

for _, filename in urls:
    label_var = StringVar(value=f"Waiting to download {filename}")
    label = Label(root, textvariable=label_var)
    progress_var = DoubleVar(value=0)
    progress = Progressbar(root, orient='horizontal', length=300, mode='determinate', variable=progress_var)

    label.pack(pady=5)
    progress.pack(pady=5)

    progress_vars.append(progress_var)
    label_vars.append(label_var)

# Start button
start_button = Button(root, text="Start Download", command=lambda: start_download(urls))
start_button.pack(pady=10)

# Run Tkinter event loop and integrate with asyncio
async def tkinter_loop():
    while True:
        root.update()
        await asyncio.sleep(0.01)

async def main():
    await asyncio.gather(tkinter_loop())

if __name__ == "__main__":
    asyncio.run(main())
