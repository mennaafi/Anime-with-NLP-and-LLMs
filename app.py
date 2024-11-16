import streamlit as st  
from theme_classifier import ThemeClassifier  
from character_network import NamedEntityRecognizer, CharacterNetworkGenerator  
from text_classification import JutsuClassifier  
from character_chatbot import CharacterChatBot  
import os  
from dotenv import load_dotenv  
load_dotenv()  

def get_themes(theme_list_str, subtitles_path, save_path):  
    theme_list = theme_list_str.split(',')  
    theme_classifier = ThemeClassifier(theme_list)  
    output_df = theme_classifier.get_themes(subtitles_path, save_path)  

    output_df = output_df[theme_list]  

    output_df = output_df[theme_list].sum().reset_index()  
    output_df.columns = ['Theme', 'Score']  

    st.bar_chart(data=output_df.set_index('Theme')['Score'], use_container_width=True)  

def get_character_network(subtitles_path, ner_path):  
    ner = NamedEntityRecognizer()  
    ner_df = ner.get_ners(subtitles_path, ner_path)  

    character_network_generator = CharacterNetworkGenerator()  
    relationship_df = character_network_generator.generate_character_network(ner_df)  
    html = character_network_generator.draw_network_graph(relationship_df)  

    st.write(html, unsafe_allow_html=True)  

def classify_text(text_classifcation_model, text_classifcation_data_path, text_to_classify):  
    jutsu_classifier = JutsuClassifier(model_path=text_classifcation_model,  
                                       data_path=text_classifcation_data_path,  
                                       huggingface_token=os.getenv('huggingface_token'))  
    
    output = jutsu_classifier.classify_jutsu(text_to_classify)  
    output = output[0]  

    return output  

def chat_with_character_chatbot(message, history):  
    character_chatbot = CharacterChatBot("mennaafif/Naruto_Llama-3-8B",  
                                         huggingface_token=os.getenv('huggingface_token'))  

    output = character_chatbot.chat(message, history)  
    output = output['content'].strip()  
    return output  


def main():  
    st.title("Anime Theme and Character Analysis Tool")  

    # Theme Classification Section  
    st.header("Theme Classification (Zero Shot Classifiers)")  
    theme_list = st.text_input("Themes (comma-separated)")  
    subtitles_path = st.text_input("Subtitles or Script Path")  
    save_path = st.text_input("Save Path")  

    if st.button("Get Themes"):  
        get_themes(theme_list, subtitles_path, save_path)  

    # Character Network Section  
    st.header("Character Network (NERs and Graphs)")  
    character_subtitles_path = st.text_input("Subtitles or Script Path for Character Network")  
    ner_path = st.text_input("NERs Save Path")  

    if st.button("Get Character Network"):  
        get_character_network(character_subtitles_path, ner_path)  

    # Text Classification with LLMs  
    st.header("Text Classification with LLMs")  
    text_classification_output = st.empty()  
    text_classifcation_model = st.text_input('Model Path')  
    text_classifcation_data_path = st.text_input('Data Path')  
    text_to_classify = st.text_area('Text input')  

    if st.button("Classify Text (Jutsu)"):  
        output = classify_text(text_classifcation_model, text_classifcation_data_path, text_to_classify)  
        text_classification_output.text(output)  

    # Character Chatbot Section  
    st.header("Character Chatbot")  
    message = st.text_input("Type a message:")  
    if 'history' not in st.session_state:  
        st.session_state.history = []  

    if st.button("Send"):  
        response = chat_with_character_chatbot(message, st.session_state.history)  
        st.session_state.history.append({"user": message, "bot": response})  
        for chat in st.session_state.history:  
            st.write(f"**You:** {chat['user']}")  
            st.write(f"**Bot:** {chat['bot']}")  

if __name__ == '__main__':  
    main()