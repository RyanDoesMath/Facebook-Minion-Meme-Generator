import random
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from aitextgen import aitextgen
from aitextgen.utils import GPT2ConfigCPU

'''
A script that uses an AI to automatically generate a minion meme.
'''

main()

# TODO - add various layouts for the meme other than text in the top left + minion in bottom right.
# TODO - Make a method that will convert the final image to jpeg, then make the jpeg to a smaller
#        size, then resize it to make it look like trash and get jpeg artifacting.

# Possible text alignments
ALIGNMENTS = ['left', 'center', 'right']

# Possible colors for the background.
BACKGROUND_COLORS = [
    '#b6a05a', '#f3f4e4', '#edf7f6', '#edeee1', '#f4f5bb',
    '#b2f6b9', '#d9dcd5', '#bdd4e0', '#e9ded8', '#f7e0bd',
    '#ebf7f1', '#efe6ee', '#dbdaab', '#edf7f6', '#e9cfb2',
    '#edebd7', '#e9ded8', '#e9ded8', '#eef6f7', '#ebe9bb']


def main():
    # Saves the final meme.
    output = combine_images()
    output.save('hilarious_minion_meme.jpg')


def make_text():
    '''
    Rebuilds the already trained AI model and returns a string split by newlines.

    Returns: a single AI generated string with newlines (roughly) after every 3 words.
    '''
    # Rebuilds the already trained AI model
    vocab_file = "aitextgen-vocab.json"
    merges_file = "aitextgen-merges.txt"
    config = GPT2ConfigCPU()
    ai = aitextgen(model="trained_model/pytorch_model.bin",
                   vocab_file=vocab_file,
                   merges_file=merges_file,
                   config=config)
    # Generates the meme text and adds newline characters so it can fit
    # on the image
    # TODO: figure out some collison detection method.
    # TODO: split after a certain number of characters, not words.
    text_list = ai.generate_one(max_length=18).split()
    for i in range(2, len(text_list), 3):
        text_list[i] += '\n'

    return ' '.join(text_list)


def make_text_image():
    '''
    Creates a 1080x720 transparent image with the text generated from make_text().

    Returns: a transparent image with randomly aligned text in the top right
    '''
    # Choose a psuedo random font size.
    font_size = random.randint(75, 95)
    # Generates a transparent image with the generated text on top.
    # TODO: randomize the font and make random words in the string bold.
    font = ImageFont.truetype('fonts/coolvetica_rg.ttf', font_size)
    transparent_box = Image.new('RGBA', (1080, 720), (0, 0, 0, 0))
    d = ImageDraw.Draw(transparent_box)
    d.multiline_text(xy=(0, 0),
                     text=make_text(),
                     fill=(0, 0, 0),
                     font=font,
                     align=random.choice(ALIGNMENTS))

    return transparent_box


def make_minion_image():
    '''
    Selects random a minion image from the transparent_minions file and randomly resizes it.

    Returns: a random resized minion image.
    '''
    # Selects the foreground minion image.
    selection_minion = str(random.randint(1, 13)).zfill(3)

    # Choose a psuedo random new height and width for the minion
    psuedo_random_height = random.randint(360 - 100, 360 + 100)
    psuedo_random_width = random.randint(540 - 100, 540 + 100)

    return Image.open('transparent_minions/' + selection_minion + '.png')\
    .resize((psuedo_random_width, psuedo_random_height))


def make_background_image():
    '''
    Makes a 1080x720 image of a random solid color from COLORS for the background of the meme.

    Returns: the background for the meme
    '''
    # Generates the background image with a random selection from colors.
    return Image.new('RGB', (1080, 720), ImageColor.getrgb(random.choice(BACKGROUND_COLORS)))


def combine_images():
    '''
    Pastes the images on top of one another with the text in the upper left and the minion in the
    lower right.
    
    Returns: the combination of all the elements of the minion meme.
    '''
    image = make_background_image()
    minion = make_minion_image()
    transparent_text = make_text_image()
    # Opens, resizes, and pastes the minion and text on top of the background.
    image.paste(minion, (540, 360), mask=minion)
    image.paste(transparent_text, (0, 0), mask=transparent_text)

    return image
