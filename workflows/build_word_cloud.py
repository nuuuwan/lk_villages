import os
import random

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from utils import Log
from wordcloud import WordCloud

from workflows.analyze_name import get_names

log = Log('build_word_cloud')

WORD_CLOUD_PATH = os.path.join("data", "word_cloud.png")
LK_PNG_PATH = os.path.join("data", "lk.png")
LK_COLOR_LIST = [
    '#ffbe29',
    '#8d153a',
    '#eb7400',
    '#00534e',
]
STOPWORDS = []


def clean_word(word: str) -> str:
    return word.strip().lower()


def lk_color_func(**_):
    n = len(LK_COLOR_LIST)
    i = random.randint(0, n - 1)
    return LK_COLOR_LIST[i]


def build_word_cloud():
    words = get_names()
    text = " ".join(words)

    mask = np.array(Image.open(LK_PNG_PATH))

    wc = WordCloud(
        background_color="white",
        repeat=True,
        mask=mask,
        width=2000,
        height=3000,
        stopwords=STOPWORDS,
    )
    wc.generate(text)
    wc.recolor(color_func=lk_color_func)

    plt.figure()
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.gcf().set_size_inches(4, 6)

    plt.savefig(WORD_CLOUD_PATH, dpi=150, bbox_inches='tight')
    log.info(f"✅ Wrote word cloud to {WORD_CLOUD_PATH}.")


if __name__ == '__main__':
    build_word_cloud()
