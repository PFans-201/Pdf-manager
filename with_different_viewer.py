import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton,
    QFileDialog, QMessageBox, QDialog, QLabel, QLineEdit
)
from PyPDF2 import PdfReader
import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from PyDictionary import PyDictionary
from collections import defaultdict
from rasa.core.agent import Agent
from rasa.core.interpreter import RasaNLUInterpreter
import nlpaug.augmenter.word as naw
import requests

# Ensure NLTK packages are downloaded
Nltk.download(‘popular’, quiet=True)

class RasaChatbot:
    '''A class representing a Rasa chatbot.'''

    def __init__(self, model_directory):
        '''
        Initialize the RasaChatbot.

        Args:
            Model_directory (str): Path to the directory containing the Rasa chatbot model.
        '''
        Self.interpreter = RasaNLUInterpreter(model_directory)
        Self.agent = Agent.load(model_directory, interpreter=self.interpreter)

    def get_response(self, message):
        '''
        Get the response from the Rasa chatbot for a given message.

        Args:
            Message (str): Input message.

        returns:
            Str: Response from the Rasa chatbot.
        '''
        Responses = self.agent.handle_text(message)
        return responses

class NLPAugRephraser:
    '''A class representing na NLPAug rephraser.'''

    def __init__(self):
        '''Initialize the NLPAugRephraser'''
        Self.aug = naw.SynonymAug(aug_src=’wordnet’)

    def rephrase(self, text):
        '''
        Rephrase the given text.

        Args:
            Text (str): Input text to be rephrased.

        returns:
            Str: Rephrased text.
        '''
        return self.aug.augment(text)

class MyMemoryTranslator:
    '''A class representing a MyMemory translator'''

    def translate(self, text, source_lang, target_lang):
        '''
        Translate the given text from source language to target language using MyMemory translator API.

        Args:
            Text (str): Text to be translated.
            Source_lang (str): Source language code.
            Target_lang (str): Target language code.

        returns:
            Str: Translated text.
        '''
        url = fhttps://api.mymemory.translated.net/get?q={text}&langpair={source_lang}|{target_lang}
        response = requests.get(url)
        data = response.json()
        return data[‘responseData’][‘translatedText’]

class PDFManager:
    '''A class representing a PDF manager.'''

    def __init__(self):
        '''Initialize the PDFManager.'''
        Self.pdf_files = []
        Self.pdf_contents = defaultdict(str)

    def upload_pdf(self, file_path: str):
        '''
        Upload a PDF file and store its contents.

        Args:
            File_path (str): Path to the PDF file.
        '''
        Self.pdf_files.append(file_path)
        Self.pdf_contents[file_path] = self.read_pdf(file_path)

    def read_pdf(self, file_path: str):
        '''
        Read the contents of a PDF file.

        Args:
            File_path (str): Path to the PDF file.

        returns:
            Str: Contents of the PDF file.
        '''
        With open(file_path, ‘rb’) as file:
            Pdf_reader = PdfReader(file)
            Text = “”
            For page_num in range(len(pdf_reader.pages)):
                Page = pdf_reader.pages[page_num]
                Text += page.extract_text()
        return text

    def summarize_pdf(self, file_path: str, num_sentences: int = 3):
        '''
        Summarize the contents of a PDF file.

        Args:
            File_path (str): Path to the PDF file.
            Num_sentences (int): Number of sentences for the summary.

        returns:
            Str: Summary of the PDF file contents.
        '''
        Text = self.pdf_contents[file_path]
        Sentences = text.split(‘. ‘)
        Summarized_text = ‘. ‘.join(sentences[:num_sentences]) + ‘.’
        return summarized_text

    def search_keywords(self, user_input: str):
        '''
        Search for keywords in the PDF files.

        Args:
            User_input (str): Keyword to search for.

        returns:
            Dict: Dictionary containing PDF file paths and matching sentences.
        '''
        definitions = {}
        For file_path, content in self.pdf_contents.items():
            if user_input.lower() in content.lower():
                Sentences = [sentence+’.’ For sentence in content.split(‘.’) if user_input.lower() in sentence.lower()]
                definitions[file_path] = ‘ ‘.join(sentences)
        return definitions

    def get_definitions(self, terms: list):
        '''
        Get definitions for terms using PyDictionary.

        Args:
            Terms (list): List of terms to get definitions for.

        returns:
            Dict: Dictionary containing terms and their definitions.
        '''
        Dictionary = PyDictionary()
        definitions = {}
        For term in terms:
            definition = dictionary.meaning(term)
            if definition:
                Formatted_definition = ‘, ‘.join(definition.get(‘Noun’, [‘No definition found’]))
                definitions[term] = formatted_definition
            else:
                definitions[term] = “No definition found”
        return definitions

class PDFManagerApp(QMainWindow):
    '''A class representing the PDF Manager application.'''

    def __init__(self, rasa_bot_path):
        '''
        Initialize the PDFManagerApp.

        Args:
            Rasa_bot_path (str): Path to the Rasa chatbot model directory.
        '''
        Super().__init__()

        Self.setWindowTitle(“PDF Manager”)

        Self.pdf_manager = PDFManager()
        Self.rasa_chatbot = RasaChatbot(rasa_bot_path)
        Self.nlpaug_rephraser = NLPAugRephraser()
        Self.mymemory_translator = MyMemoryTranslator()

        Layout = QVBoxLayout()

        Upload_button = QPushButton(“Upload PDFs and Summarize”)
        Upload_button.clicked.connect(self.upload_and_summarize)
        Layout.addWidget(upload_button)

        Explain_button = QPushButton(“Explain a Keyword or Concept”)
        Explain_button.clicked.connect(self.ask_for_explanation)
        Layout.addWidget(explain_button)

        Central_widget = QWidget()
        Central_widget.setLayout(layout)
        Self.setCentralWidget(central_widget)

    def upload_and_summarize(self):
        '''Upload PDF files and summarize their contents.'''
        Folder_path = QFileDialog.getExistingDirectory(self, “Select Directory”)
        if folder_path:
            For file_name in os.listdir(folder_path):
                if file_name.endswith(‘.pdf’):
                    Pdf_path = os.path.join(folder_path, file_name)
                    Self.pdf_manager.upload_pdf(pdf_path)
                    Summary = self.pdf_manager.summarize_pdf(pdf_path)
                    QMessageBox.information(self, “Summary”, f”Summary for {file_name}:\n{summary}”)

    def ask_for_explanation(self):
        '''Ask for user input and provide explanations.'''
        Keyword, ok = QInputDialog.getText(self, “Input”, “Enter the keyword or concept you need help with:”)
                if ok and keyword:
            definitions = self.pdf_manager.search_keywords(keyword)
            if definitions:
                Message = f”{keyword} found in the following documents:\n\n”
                Message += ‘\n’.join([f”{file_path}: {definition}” for file_path, definition in definitions.items()])
                QMessageBox.information(self, “Explanation”, message)
            else:
                definition = self.pdf_manager.get_definitions([keyword])
                QMessageBox.information(self, “Explanation”, f”{keyword}: {definition[keyword]}”)

            Rasa_response = self.rasa_chatbot.get_response(keyword)
            QMessageBox.information(self, “Rasa Chatbot Response”, rasa_response)

            Rephrased_text = self.nlpaug_rephraser.rephrase(keyword)
            QMessageBox.information(self, “Rephrased Text”, rephrased_text)

            Translated_text = self.mymemory_translator.translate(keyword, ‘en’, ‘pt’)
            QMessageBox.information(self, “Translated Text”, translated_text)


if __name__ == “__main__”:
    import sys
    App = QApplication(sys.argv)
    Window = PDFManagerApp(‘/path/to/your/rasa_bot_model_directory’)
    Window.show()
    Sys.exit(app.exec_())
