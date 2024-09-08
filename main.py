import sys

import requests
from bs4 import BeautifulSoup
from atproto import Client, models
import time

import warnings

warnings.filterwarnings("ignore", category=UserWarning, module='pydantic')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Referer': 'https://nitter.lucabased.xyz/',
}

client = Client(base_url='https://bsky.social')

data_pages = []
data_tweets = []

config_retries = 10
config_delay=3


def fetch_user_pages(user, page=None):
    max_retries = config_retries

    if page is None:
        url = f"https://nitter.lucabased.xyz/{user}"
    else:
        url = f"https://nitter.lucabased.xyz/{user}{page}"

    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            button = soup.find_all('div', class_='show-more')
            end = soup.find_all('h2', class_='timeline-end')

            if end:
                return

            for page in button:
                if page.text == 'Load more':
                    result = page.find_next('a').get('href')
                    data_pages.append(result)
                    fetch_user_pages(user, result)
                    return
            return

        except requests.RequestException as e:
            if attempt < max_retries - 1:
                time.sleep(config_delay)
            else:
                sys.exit(1)


def fetch_user_tweets(user):
    url = f"https://nitter.lucabased.xyz"
    max_retries = config_retries

    for page in reversed(data_pages):
        page_url = f'{url}/{user}{page}'
        attempt = 0

        while attempt < max_retries:
            try:
                response = requests.get(page_url)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'html.parser')
                tweets = soup.find_all('div', class_='timeline-item')

                for tweet in tweets:
                    if tweet.find('div', class_='pinned'):
                        continue

                    if tweet.find('div', class_='retweet-header'):
                        continue

                    if tweet.find('div', class_='gallery-video'):
                        continue

                    image = tweet.find('div', class_='attachment image')
                    caption = tweet.find('div', class_='tweet-content media-body')

                    tweet_caption = caption.text.strip() if caption else ""
                    image_url = image.find('a')['href'] if image else None

                    if image_url and not image_url.startswith('http'):
                        image_url = f"https://nitter.lucabased.xyz{image_url}"

                    if tweet_caption:
                        data = [
                            {"message": tweet_caption, "image_url": image_url}
                        ]
                        data_tweets.append(data)
                break

            except requests.RequestException as e:
                attempt += 1
                if attempt >= max_retries:
                    sys.exit()


def download_twitter_image(image):
    response = requests.get(image)

    if response.status_code == 200:
        with open('downloaded_image.jpg', 'wb') as f:
            f.write(response.content)

def send_blueksy_post():
    for tweet in data_tweets:
        if tweet[0]['image_url'] is None:
            client.send_post(tweet[0]['message'])
        else:
            download_twitter_image(tweet[0]['image_url'])

            with open('downloaded_image.jpg', 'rb') as img_file:
                img_data = img_file.read()
                upload = client.upload_blob(img_data)
                images = [models.AppBskyEmbedImages.Image(alt='Image by X', image=upload.blob)]
                embed = models.AppBskyEmbedImages.Main(images=images)

                post = models.AppBskyFeedPost.Record(
                    text=tweet[0]['message'],
                    embed=embed,
                    created_at=client.get_current_time_iso()
                )
                client.com.atproto.repo.create_record(
                    models.ComAtprotoRepoCreateRecord.Data(
                        repo=client.me.did,
                        collection=models.ids.AppBskyFeedPost,
                        record=post
                    )
                )

if __name__ == '__main__':
    quest = '[Bluesky] Qual o E-mail usado para logar sua conta no Bluesky? (USE APENAS O E-MAIL)'
    user = input(quest)

    quest = '[Bluesky] Qual a senha da sua conta Bluesky? (Fique tranquilo, não armazenaremos sua senha)'
    pw = input(quest)

    try:
        client.login(user, pw)
    except Exception as e:
        print(f'[Bluesky] Erro ao realizar o Login: {e}')

    quest = '[System] Qual o usuário do Twitter da qual você deseja importar? (OBS: Apenas o usuário, NÃO USE @ Ex: Pinheiro)'
    response = input(quest)

    print('[System] Tudo certo! Iniciando o sistema de importação, o processo poderá demorar alguns minutos, avisaremos quando tudo acabar!')
    time.sleep(3)


    data_pages.append('')
    print('[System] Iniciando processo de obtenção de dados, aguarde...')
    fetch_user_pages(response)
    fetch_user_tweets(response)

    print('[System] Iniciando processo de postagem no Bluesky, aguarde...')
    send_blueksy_post()

    print('[System] Sucesso! O processo acabou sem erros, verifique sua página do Bluesky para ter certeza que tudo ocorreu bem.')