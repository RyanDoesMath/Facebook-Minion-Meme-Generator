"In the future, entertainment will be randomly generated!"
- Larry the Cucumber, Veggietales.

# Facebook-Minion-Meme-Generator
This is easily the worst thing I've ever coded.

Facebook minion meme generator is a program that uses an AI from aitextgen and the Python image library to automatically generate Facebook-tier minion memes.

The ai is nowhere close to speaking comprehensible English. 
Rather than simply prompting an already trained AI with minion-meme-eqsue prompts, I opted to train an AI from scratch on only the text transcribed from minion and minion like boomer mom memes. The advantage of this is that the AI can only produce text with the particular cadence and punctuation of a Facebook minion meme.
By my estimations, the AI will require around 1000 datapoints before it starts producing mostly-coherent words, and perhaps around 5000 before it starts making sentences with any actual meaning.
I have considered supplementing the training of the AI with a few thousand lines of a book or newspaper, but I want this AI to be incapable of producing anything other than a Facebook meme, so for now I am not training it on anything other than memes.

We are currently at 366 datapoints. I keep the code for training the AI off of this repo, but I added the CSV containing the transcribed memes so others can see the kind of data that the AI is working with.

Here are some examples of the current output.
![alt text](https://github.com/RyanDoesMath/Facebook-Minion-Meme-Generator/blob/main/Sample_Output/hilarious_minion_meme_01.jpg)
![alt text](https://github.com/RyanDoesMath/Facebook-Minion-Meme-Generator/blob/main/Sample_Output/hilarious_minion_meme_02.jpg)
![alt text](https://github.com/RyanDoesMath/Facebook-Minion-Meme-Generator/blob/main/Sample_Output/hilarious_minion_meme_03.jpg)

AI used https://github.com/minimaxir/aitextgen
