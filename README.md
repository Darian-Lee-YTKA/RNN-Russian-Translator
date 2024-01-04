# RNN-Russian-Translator
Machine translation for simple Russian sentences. 
## Demo:
<img src="demoTranslateApp.gif" width=300>

## About Data:
The original data I used can be found [here](https://www.manythings.org/anki/)  (click to download rus-en.zip). The text was preprocessed by splitting the sentences and removing punctuation and capitalization. The Russian data was then lemmatized to remove unnessecary mophological destinctions that English does not have and tagged for past tense. Both the Russian and English were padded and encoded using the keras tokenizer and the english ouput was one hot encoded
## About Model:
The actual machine translation model code can be found in the .ipynb file here. 
I used a RNN model with LSTM. The file model has 400 units and uses a Russian vocabulary size of just under 6,000 and an English vocabulary size of around 3,000. The max token size for the Russian input that my model can translate is 10 tokens, and the maximum size of the english output is 5 tokens. 
## About App: 
I download my trained model as well as the English and Russian encoders and a [python program] on my local computer for accepting user input and generating a translation using the model. The program then uses fast API to connect to an [iOS app in Swift], allowing the text that user inputs in the text field to be automatically translated. 
