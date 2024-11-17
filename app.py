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

    # Remove dialogue from the theme list  
    theme_list = [theme for theme in theme_list if theme != 'dialogue']  
    output_df = output_df[theme_list]  

    output_df = output_df[theme_list].sum().reset_index()  
    output_df.columns = ['Theme', 'Score']  

    return output_df  

def get_character_network(subtitles_path, ner_path):  
    ner = NamedEntityRecognizer()  
    ner_df = ner.get_ners(subtitles_path, ner_path)  

    character_network_generator = CharacterNetworkGenerator()  
    relationship_df = character_network_generator.generate_character_network(ner_df)  
    html = character_network_generator.draw_network_graph(relationship_df)  

    return html  

def classify_text(text_classifcation_model, text_classifcation_data_path, text_to_classify):  
    jutsu_classifier = JutsuClassifier(model_path=text_classifcation_model,  
                                       data_path=text_classifcation_data_path,  
                                       huggingface_token=os.getenv('huggingface_token'))  
    
    output = jutsu_classifier.classify_jutsu(text_to_classify)  
    return output[0]  

def chat_with_character_chatbot(message, history):  
    character_chatbot = CharacterChatBot("mennaafif/Naruto_Llama-3-8B",  
                                         huggingface_token=os.getenv('huggingface_token'))  
    
    output = character_chatbot.chat(message, history)  
    return output['content'].strip()  

def main():  
    st.title("Anime Analysis Tool")  

    # Theme Classification Section  
    st.header("Theme Classification (Zero Shot Classifiers)")  
    theme_list = st.text_input("Enter themes (comma-separated):")  
    subtitles_path = st.text_input("Subtitles or script Path:")  
    save_path = st.text_input("Save Path:")  
    
    if st.button("Get Themes"):  
        output_df = get_themes(theme_list, subtitles_path, save_path)  
        st.bar_chart(output_df.set_index('Theme'))  

    # Character Network Section  
    st.header("Character Network (NERs and Graphs)")  
    ner_subtitles_path = st.text_input("Subtitles or Script Path:")  
    ner_path = st.text_input("NERs save path:")  
    
    if st.button("Get Character Network"):  
        network_html = get_character_network(ner_subtitles_path, ner_path)  
        st.markdown(network_html, unsafe_allow_html=True)  

    # Text Classification with LLMs  
    st.header("Text Classification with LLMs")  
    text_classification_model = st.text_input("Model Path:")  
    text_classification_data_path = st.text_input("Data Path:")  
    text_to_classify = st.text_area("Text input:")  
    
    if st.button("Classify Text (Jutsu)"):  
        classification_output = classify_text(text_classification_model, text_classification_data_path, text_to_classify)  
        st.text(f"Classification Output: {classification_output}")  

    # Character Chatbot Section  
    st.header("Character Chatbot")  
    message = st.text_input("Send a message:")  
    chat_history = st.session_state.get('history', [])  
    
    if st.button("Send"):  
        response = chat_with_character_chatbot(message, chat_history)  
        chat_history.append((message, response))  
        st.session_state.history = chat_history  
        for user_message, bot_response in chat_history:  
            st.write(f"You: {user_message}")  
            st.write(f"Bot: {bot_response}")  

if __name__ == '__main__':  
    main()