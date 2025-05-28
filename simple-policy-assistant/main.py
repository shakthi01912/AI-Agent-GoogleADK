# main.py
import google.generativeai as genai
import PyPDF2
import os
import re
from dotenv import load_dotenv

class SimplePDFChat:
    def __init__(self):
        # Load environment
        load_dotenv()
        api_key = os.getenv('GOOGLE_API_KEY')
        
        if not api_key:
            print("❌ Please set GOOGLE_API_KEY in .env file")
            exit()
        
        # Setup Gemini
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.pdf_text = ""
    
    def load_pdf(self, pdf_path):
        """Load PDF content"""
        print(f"📄 Loading {pdf_path}...")
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page_num, page in enumerate(pdf_reader.pages):
                    text += f"\n--- Page {page_num + 1} ---\n"
                    text += page.extract_text()
                
                self.pdf_text = text
                print(f"✅ Loaded {len(pdf_reader.pages)} pages")
                return True
        except Exception as e:
            print(f"❌ Error loading PDF: {e}")
            return False
    
    def find_relevant_text(self, question):
        """Simple text search"""
        if not self.pdf_text:
            return ""
        
        # Split into paragraphs
        paragraphs = [p.strip() for p in self.pdf_text.split('\n') if len(p.strip()) > 30]
        
        # Simple keyword matching
        question_words = set(re.findall(r'\w+', question.lower()))
        scored_paragraphs = []
        
        for para in paragraphs:
            para_words = set(re.findall(r'\w+', para.lower()))
            score = len(question_words.intersection(para_words))
            if score > 0:
                scored_paragraphs.append((score, para))
        
        # Return top 5 most relevant paragraphs
        scored_paragraphs.sort(reverse=True)
        return '\n\n'.join([para for _, para in scored_paragraphs[:5]])
    
    def ask_question(self, question):
        """Answer question using PDF content"""
        relevant_text = self.find_relevant_text(question)
        
        if not relevant_text:
            return "I couldn't find relevant information in the PDF for your question."
        
        # Create prompt
        prompt = f"""Based on the following document content, please answer the question:

DOCUMENT CONTENT:
{relevant_text}

QUESTION: {question}

Please provide a clear and helpful answer based only on the information in the document content above."""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {e}"

def main():
    print("🏢 Simple PDF Assistant")
    print("=" * 50)
    
    # Initialize
    chat = SimplePDFChat()
    
    # Find and load PDF
    pdf_files = []
    if os.path.exists('pdfs'):
        pdf_files = [f for f in os.listdir('pdfs') if f.endswith('.pdf')]
    
    if not pdf_files:
        print("❌ No PDF files found!")
        print("Please put PDF files in a 'pdfs' folder")
        return
    
    # Load first PDF
    pdf_path = os.path.join('pdfs', pdf_files[0])
    if not chat.load_pdf(pdf_path):
        return
    
    print(f"\n💬 Ask questions about: {pdf_files[0]}")
    print("Type 'quit' to exit\n")
    
    # Chat loop
    while True:
        question = input("🤔 Your question: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        
        if not question:
            continue
        
        print("🤖 Thinking...")
        answer = chat.ask_question(question)
        print(f"\n📝 Answer: {answer}\n")

if __name__ == "__main__":
    main()