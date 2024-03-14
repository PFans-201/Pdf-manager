import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PyPDF2 import PdfReader
import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from PyDictionary import PyDictionary
from collections import defaultdict
from rasa_chatbot import RasaChatbot

from nlpaug_rephraser import NLPAugRephraser

from mymemory-tr-free import MyMemoryTranslator



# Ensure NLTK packages are downloaded
nltk.download('popular', quiet=True)

class PDFManager:
    def __init__(self):
        self.pdf_files = []
        self.pdf_contents = defaultdict(str)

    def upload_pdf(self, file_path: str):
        self.pdf_files.append(file_path)
        self.pdf_contents[file_path] = self.read_pdf(file_path)

    def read_pdf(self, file_path: str):
        with open(file_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        return text

    def summarize_pdf(self, file_path: str, num_sentences: int = 3):
        text = self.pdf_contents[file_path]
        sentences = text.split('. ')
        summarized_text = '. '.join(sentences[:num_sentences]) + '.'
        return summarized_text

    def search_keywords(self, user_input: str):
        definitions = {}
        for file_path, content in self.pdf_contents.items():
            if user_input.lower() in content.lower():
                sentences = [sentence+'.' for sentence in content.split('.') if user_input.lower() in sentence.lower()]
                definitions[file_path] = ' '.join(sentences)
        return definitions

    def get_definitions(self, terms: list):
        dictionary = PyDictionary()
        definitions = {}
        for term in terms:
            definition = dictionary.meaning(term)
            if definition:
                # Format the definition for display
                formatted_definition = ', '.join(definition.get('Noun', ['No definition found']))
                definitions[term] = formatted_definition
            else:
                definitions[term] = "No definition found"
        return definitions

class PDFManagerApp:
    def __init__(self, root):

        self.root = root

        self.root.title("PDF Manager")

        self.pdf_manager = PDFManager()

        self.rasa_chatbot = RasaChatbot('path_to_your_rasa_model')

        self.nlpaug_rephraser = NLPAugRephraser()

        self.mymemory_translator = MyMemoryTranslator()


        # Create GUI elements
        self.upload_button = tk.Button(root, text="Upload PDFs and Summarize", command=self.upload_and_summarize)
        self.upload_button.pack()

        self.explain_button = tk.Button(root, text="Explain a Keyword or Concept", command=self.ask_for_explanation)
        self.explain_button.pack()

    def upload_and_summarize(self):
        folder_path = filedialog.askdirectory()
        if folder_path:  # Check if a folder path is selected
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.pdf'):
                    pdf_path = os.path.join(folder_path, file_name)
                    self.pdf_manager.upload_pdf(pdf_path)
                    summary = self.pdf_manager.summarize_pdf(pdf_path)
                    messagebox.showinfo("Summary", f"Summary for {file_name}:\n{summary}")
    def ask_for_explanation(self):

        keyword = simpledialog.askstring("Input", "Enter the keyword or concept you need help with:")

        if keyword:

            definitions = self.pdf_manager.search_keywords(keyword)

            if definitions:

                messagebox.showinfo("Explanation", f"{keyword} found in the following documents:\n\n" + '\n'.join([f"{file_path}: {definition}" for file_path, definition in definitions.items()]))

            else:

                definition = self.pdf_manager.get_definitions([keyword])

                messagebox.showinfo("Explanation", f"{keyword}: {definition[keyword]}")



            # Get Rasa chatbot response

            rasa_response = self.rasa_chatbot.get_response(keyword)

            messagebox.showinfo("Rasa Chatbot Response", rasa_response)



            # Get rephrased text

            rephrased_text = self.nlpaug_rephraser.rephrase(keyword)

            messagebox.showinfo("Rephrased Text", rephrased_text)



            # Get translated text

            translated_text = self.mymemory_translator.translate(keyword, 'en', 'pt')

            messagebox.showinfo("Translated Text", translated_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFManagerApp(root)
    root.mainloop()
