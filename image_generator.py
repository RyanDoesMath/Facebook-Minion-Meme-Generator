import random
import numpy
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from aitextgen import aitextgen
from aitextgen.TokenDataset import TokenDataset
from aitextgen.tokenizers import train_tokenizer
from aitextgen.utils import GPT2ConfigCPU

class image_generator:
    
    #TODO - add various layouts for the meme other than text in the top left
    # and minion in the bottom right
    bottom_right = (540, 360)
    
    # Randomizes text alignment.
    alignments = ['left', 'center', 'right']
    alignment_generator = random.randint(0, 2)
    
    # Possible colors for the background.
    colors = [
              '#b6a05a', '#f3f4e4', '#edf7f6', '#edeee1', '#f4f5bb', 
              '#b2f6b9', '#d9dcd5', '#bdd4e0', '#e9ded8', '#f7e0bd', 
              '#ebf7f1', '#efe6ee', '#dbdaab', '#edf7f6', '#e9cfb2', 
              '#edebd7', '#e9ded8', '#e9ded8', '#eef6f7', '#ebe9bb'
              ]
    
    # Selects the background color and the foreground minion image.
    selection_bg = random.randint(0, len(colors) - 1)
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
    ai = aitextgen(model = "trained_model/pytorch_model.bin", 
                   vocab_file = vocab_file,
                   merges_file = merges_file,
                   config = config)
    
    # Generates the image text and adds newline characters so it can fit
    # on the image
    # TODO: figure out some collison detection method.
    text = ai.generate_one(max_length = 15)
    text_list = text.split()
    newline_inserted_text = ''
    for i in range(len(text_list)):
        if (i + 1) % 3 == 2:
            text_list[i] = text_list[i]+'\n'
    for i in text_list:
        newline_inserted_text = newline_inserted_text + i + " "
    text = newline_inserted_text
    
    # Generates a transparent image with the generated text on top.
    # TODO: randomize the font and make random words boldface.
    font = ImageFont.truetype('fonts/coolvetica_rg.ttf', font_size)
    transparent_text = Image.new('RGBA', (1080, 720), (0, 0, 0, 0))
    d = ImageDraw.Draw(transparent_text)
    d.multiline_text(xy = (0, 0), 
                     text = text, 
                     fill = (0, 0, 0), 
                     font = font, 
                     align = alignments[alignment_generator])
    
    # Generates the background image.
    im_out = Image.new('RGB', (1080, 720), ImageColor.getrgb(colors[selection_bg]))
    
    # Opens, resizes, and pastes the minion and text on top of the background.
    minion = Image.open('transparent_minions/' + selection_minion + '.png')
    minion = minion.resize((psuedo_random_width, psuedo_random_height))
    im_out.paste(minion, (540, 360), mask = minion)
    im_out.paste(transparent_text, (0, 0), mask = transparent_text)
    
    # Saves the final meme.
    im_out.save('hilarious_minion_meme.jpg')
    
