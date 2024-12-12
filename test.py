import asyncio
import httpx
from tqdm import tqdm

async def download(url: str, filename: str):
    try:
        with open(filename, 'wb') as f:
            async with httpx.AsyncClient(timeout=30.0) as client:
                async with client.stream('GET', url) as r:
                    r.raise_for_status()
                    total = int(r.headers.get('content-length', 0)) or None
                    tqdm_params = {
                        'desc': filename,
                        'total': total,
                        'miniters': 1,
                        'unit': 'B',
                        'unit_scale': True,
                        'unit_divisor': 1024,
                    }
                    with tqdm(**tqdm_params) as pb:
                        total_downloaded = 0
                        for chunk in r.aiter_bytes():
                            f.write(chunk)
                            total_downloaded += len(chunk)
                            pb.update(len(chunk))
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        raise  # Re-raise the exception after logging it


async def main():
    """
    Downloading multiple large files simultaneously.
    Each file has its own progress bar.
    """
    urls = [
        ('https://download938.mediafire.com/pgsuiwnvuk4g4rsA9x8NAAoMwmJDTg-aNrAXUJuI1wXdL14huApR6qNqu7sRH8ZqALHNgZ7jgSgCLdrVHIstbsDJbCxMRVyZMBYKfnRmdmjL7Dm0ueBIjVJe87e42Hp0IJNLlihoE55QyJjdpaZgYle2Bl2fqXPMdeAByB4ciFzs/qob85dyzjpiqfdn/download.rar', '10MB_1.zip'),
        ('https://download938.mediafire.com/pgsuiwnvuk4g4rsA9x8NAAoMwmJDTg-aNrAXUJuI1wXdL14huApR6qNqu7sRH8ZqALHNgZ7jgSgCLdrVHIstbsDJbCxMRVyZMBYKfnRmdmjL7Dm0ueBIjVJe87e42Hp0IJNLlihoE55QyJjdpaZgYle2Bl2fqXPMdeAByB4ciFzs/qob85dyzjpiqfdn/download.rar', '10MB_2.zip'),
        ('https://download938.mediafire.com/pgsuiwnvuk4g4rsA9x8NAAoMwmJDTg-aNrAXUJuI1wXdL14huApR6qNqu7sRH8ZqALHNgZ7jgSgCLdrVHIstbsDJbCxMRVyZMBYKfnRmdmjL7Dm0ueBIjVJe87e42Hp0IJNLlihoE55QyJjdpaZgYle2Bl2fqXPMdeAByB4ciFzs/qob85dyzjpiqfdn/download.rar', '10MB_3.zip'),
    ]
    tasks = [download(url, filename) for url, filename in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Report errors, if any
    for result, (url, _) in zip(results, urls):
        if isinstance(result, Exception):
            print(f"Error downloading {url}: {result}")


if __name__ == "__main__":
    asyncio.run(main())
