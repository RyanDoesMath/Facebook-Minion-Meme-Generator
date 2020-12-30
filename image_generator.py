import random
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from aitextgen import aitextgen
from aitextgen.utils import GPT2ConfigCPU

class image_generator:
    '''
    A class that generates a minion meme from AI text.
    '''

    #TODO - add various layouts for the meme other than text in the top left

    # Possible text alignments
    alignments = ['left', 'center', 'right']

    # Possible colors for the background.
    colors = [
                '#b6a05a', '#f3f4e4', '#edf7f6', '#edeee1', '#f4f5bb',
                '#b2f6b9', '#d9dcd5', '#bdd4e0', '#e9ded8', '#f7e0bd',
                '#ebf7f1', '#efe6ee', '#dbdaab', '#edf7f6', '#e9cfb2',
                '#edebd7', '#e9ded8', '#e9ded8', '#eef6f7', '#ebe9bb']

    # Selects the foreground minion image.
    selection_minion = str(random.randint(1, 13)).zfill(3)

    # Choose a psuedo random new height and width for the minion
    psuedo_random_height = random.randint(360 - 100, 360 + 100)
    psuedo_random_width = random.randint(540 - 100, 540 + 100)
    # Choose a psuedo random font size.
    font_size = random.randint(75, 95)

    # Rebuilds the already trained AI model
    vocab_file = "aitextgen-vocab.json"
    merges_file = "aitextgen-merges.txt"
    config = GPT2ConfigCPU()
    ai = aitextgen(model="trained_model/pytorch_model.bin",
                   vocab_file=vocab_file,
                   merges_file=merges_file,
                   config=config)

    # Generates the image text and adds newline characters so it can fit
    # on the image
    # TODO: figure out some collison detection method.
    text_list = ai.generate_one(max_length=18).split()
    for i in range(2, len(text_list), 3):
        text_list[i] += '\n'
    text = ' '.join(text_list)

    # Generates a transparent image with the generated text on top.
    # TODO: randomize the font and make random words boldface.
    font = ImageFont.truetype('fonts/coolvetica_rg.ttf', font_size)
    transparent_text = Image.new('RGBA', (1080, 720), (0, 0, 0, 0))
    d = ImageDraw.Draw(transparent_text)
    d.multiline_text(xy=(0, 0),
                     text=text,
                     fill=(0, 0, 0),
                     font=font,
                     align=random.choice(alignments))

    # Generates the background image.
    im_out = Image.new('RGB', (1080, 720), ImageColor.getrgb(random.choice(colors)))

    # Opens, resizes, and pastes the minion and text on top of the background.
    minion = Image.open('transparent_minions/' + selection_minion + '.png')\
    .resize((psuedo_random_width, psuedo_random_height))
    im_out.paste(minion, (540, 360), mask=minion)
    im_out.paste(transparent_text, (0, 0), mask=transparent_text)

    # Saves the final meme.
    # TODO: convert the final image to jpeg, then make the jpeg to a smaller size,
    # then resize it to make it look like trash and get jpeg artifacting.
    im_out.save('hilarious_minion_meme.jpg')
