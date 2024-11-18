

<div align="center">  

# Naruto series with NLP an LLMs

Welcome to the project ! , In this project, I will leverage AI, Large Language Models (LLMs), and Natural Language Processing (NLP) techniques to analyze and play with naruto anime series.

![Project Overview](https://github.com/user-attachments/assets/3a275525-3005-4641-a5e1-a45ac20b6baf)  
 
 
  
</div>



## All about data :
### In this project , I will use three datasets.

 
- subtitles : https://subtitlist.com/subs/naruto-season-1/english/2206507
- transcripts : https://www.kaggle.com/datasets/leonzatrax/naruto-ep-1-transcript
- classification_dataset : https://naruto.fandom.com/wiki/Special:BrowseData/Jutsu?limit=250&offset=0&_cat=Jutsu

### Datasets Overview  

- **Subtitles Dataset:**  
  This comprehensive dataset contains subtitles for all episodes, making it ideal for training our **theme classification** and **named entity recognition** models. Its extensive size ensures rich insights can be extracted, powering **two models** in total.  

- **Transcripts Dataset:**  
  While this dataset is limited in size and does not encompass all episodes, it will still play a crucial role in our **chatbot** model. Despite this limitation, it offers valuable dialogue for character interactions, contributing to **one model**.  

- **Classification Dataset:**  
  This dataset will be crawled specifically to categorize ninja attacks into three distinct categories: **ninjutsu, genjutsu,** and **taijutsu**. This focused dataset will support the development of **one model** dedicated to classifying these attack types.



 
    <img src="https://github.com/user-attachments/assets/19ca670c-28ca-40fb-907e-905eeead69c7" alt="ninja_attacks_cats" width="300"/>  



 > - ### I started by crawling a classification dataset from the Naruto Fandom website using `Scrapy and BeautifulSoup`. The focus was to extract detailed information about Jutsu, including their names, descriptions, and types of attacks.  












# Now Lets's start explain our Models  :






 ###   In this project, we have created 4 models, each containing the code for a different aspect of the project 

- `theme_classifier` :  is designed to classify themes from textual subtitles dataset which contains all episodes , using `a zero-shot learning` approach. Leveraging the pre-trained `facebook/bart-large-mnli` model from Hugging Face's Transformers library, this class allows for the identification of various themes based on user-defined categories.


#### Given this theme list :
  -  theme_list = ["friendship", "hope", "sacrifice", "battle", "self development", "betrayal", "love", "dialogue"] 
  - Model output    : 
  ![Screenshot 50](https://github.com/user-attachments/assets/e5c48aa5-c74b-467d-9cdc-e1d0eac0383c)




  - `named_entity_recognizer` :  focuses on identifying and extracting named entities, specifically person names, from a script. Utilizing the `spaCy` library and its transformer-based model `en_core_web_trf`, this model processes the text efficiently to enhance the overall understanding of character interactions within the scripts.  

  - `character_netowork_generator` : To understand the relationships between characters extracted by the `NamedEntityRecognizer`, the `CharacterNetworkGenerator` class helps visualize these connections through a network graph.  

  Together, the `NamedEntityRecognizer` and `CharacterNetworkGenerator` provide a comprehensive framework for analyzing character interactions in scripts. By extracting named entities and visualizing their relationships, this project enables a deeper understanding of character dynamics and story development, enriching the analysis of narratives within the datasets.  





You can view the character network visualization   [here](character_network/naruto.html)


![Screenshot](https://github.com/user-attachments/assets/6e9fecdd-236c-4834-a5c1-d8d6736029fb) 


- `jutsu_classifier` :  is designed to classify types of `jutsu`, which are ninja attack categories from the Naruto franchise. It utilizes a pre-trained Transformer model, such as `DistilBERT`, to leverage advanced natural language processing techniques. `By fine-tuning` this model for the `specific task of jutsu classification`,  ensuring accurate classification of various jutsu types. 









- `character_chatbot` :  is designed to create an interactive chatbot that mimics Naruto, a character from the anime "Naruto." The bot leverages advanced language models to generate responses that reflect Naruto's personality and speech patterns based on conversational history.  



1. **Pre-Trained Model Utilization** :  
   - The chatbot uses a pre-trained model (`meta-llama/Meta-Llama-3-8B-Instruct`) as its foundational layer. This model has already been trained on a diverse set of text data, allowing it to understand and generate coherent and contextually relevant language.  

2. **Quantization for Efficiency** :  
   - The model is configured to be loaded in a quantized format (using 4-bit representation) through the `BitsAndBytesConfig` class, which improves loading speed and reduces memory consumption. 

3. **Fine-Tuning via PEFT (Parameter Efficient Fine-Tuning)** :  
   - The training process incorporates `PEFT` techniques, specifically the `LORA` (Low-Rank Adaptation) approach. This allows for fewer parameters to be updated during training while still enabling the model to acquire specific behaviors and knowledge related to the Naruto character.  
   - The `train` method fine-tunes the pre-trained base model using conversation transcripts from Naruto, adjusting its knowledge and responses to better emulate Naruto's speech and personality.  

4. **Response Generation** :  
   - When receiving a user message, the model generates responses by taking into account the current conversation's context. The `chat` method constructs the `prompt` incorporating this context, allowing the model to generate relevant replies reflective of Naruto's character traits.  






   







### Install Dependencies :

 > - Before running the code, make sure you have all the required dependencies installed. 

```
pip install -r requirements.txt  
```


 


   

