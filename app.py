import streamlit as st
import tempfile
from langchain.document_loaders import PyMuPDFLoader
from langchain.chat_models import ChatOpenAI
from langchain.prompts import HumanMessagePromptTemplate
from langchain.schema.messages import SystemMessage
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
import os


    
# Function to save uploaded file to a temporary location
@st.cache_data
def save_uploaded_file(uploaded_file):
    _, temp_file_path = tempfile.mkstemp(suffix=".pdf")
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(uploaded_file.read())
    return temp_file_path


# Enhanced Summary Prompt
summary_prompt = """
Given the provided text, create an extensive and detailed summary that captures the key points, themes, and essential details. The summary should be comprehensive yet concise, helping students understand and remember the core information. The summary will be in the SAME GERMAN language as the provided text.
-
REMEMBER: do not summarize tables or directories
-
Text:
{text}

Extensive Summary:
"""

# Enhanced Question and Answer Prompt
Qans_prompt = """
Based on the provided study material, create a set of at least ten detailed question and answer pairs. These should cover the main concepts, facts, and ideas in the text, aiding in study and review. Ensure that the questions vary in type (factual, conceptual, application-based) to facilitate a comprehensive understanding. The Q&A pairs will be in the SAME GERMAN language as the text.

Text:
{text}

Detailed Q&A Pairs:
"""

# Extractive summarization function
@st.cache_data
def generate_summ(text, template):
    prompt = ChatPromptTemplate.from_template(template)
    model = ChatOpenAI(model_name="gpt-3.5-turbo-1106", temperature=0.5, model_kwargs={'top_p':0.9})
    chain = (
        {"text": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    return chain.invoke(text)

# Extractive QA function
@st.cache_data
def generate_QA(text, template):
    prompt = ChatPromptTemplate.from_template(template)
    model = ChatOpenAI(model_name="gpt-3.5-turbo-1106", temperature=0.7,model_kwargs={'frequency_penalty': 0.2, 'top_p': 0.9})
    chain = (
        {"text": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    return chain.invoke(text)

# Streamlit app
def main():
    st.session_state.active_section = 'New sesion(Home)'
    st.title("PDF Uploader and Processor")
    def go_home():
        st.session_state.active_section = None

    # Function to navigate back to the main screen
    def go_back():
        st.session_state.active_section = None
    

    with st.sidebar:
        st.header("Menu")
        if st.button('Home'):  # <-- Add this line for the Home button
            go_home() 
        
        if st.button('Api'):  # <-- Add this line for the Home button
            st.session_state.active_section="api"
            
        if st.button('Terms and Conditions'):
            st.session_state.active_section = 'terms'

        if st.button('Privacy Policy'):
            st.session_state.active_section = 'privacy'

        if st.button('FAQ'):
            st.session_state.active_section = 'faq'

        if st.button('Login'):
            st.session_state.active_section = 'login'

    # Main area of the app
    if st.session_state.active_section == 'api':
        st.header("API for PDF Processing")

        api_content = """
        We're excited to announce that we are planning to introduce an API for PDF processing in the future. This API will empower developers and businesses to integrate our powerful PDF processing capabilities into their own applications.

        **Key Features of the API:**
        - **PDF Upload and Processing:** Developers can programmatically upload PDF documents and leverage our processing capabilities.
        - **Document Conversion:** Convert PDFs to various formats like Word, Excel, and more.
        - **Text Extraction:** Extract text and data from PDF documents using our API endpoints.
        - **Editing and Annotation:** Perform editing and annotation tasks programmatically.
        - **Secure and Scalable:** The API will be designed with security and scalability in mind to handle large volumes of PDFs.

        **Usage Scenarios:**
        - Integration into document management systems.
        - Automation of document processing workflows.
        - Enhancing existing applications with PDF manipulation capabilities.

        We're working diligently on developing and testing the API to ensure it meets the highest standards. Stay tuned for updates on the API release!

        For inquiries or early access to the API, please reach out to our support team!
        """

        st.write(api_content)
        if st.button("Back"):
            go_back()
        
    if st.session_state.active_section == 'terms':
        st.header("Terms and Conditions")
    
        terms_and_conditions = """
        Welcome to our website. These terms and conditions outline the rules and regulations for the use of our website.

        By accessing this website, we assume you accept these terms and conditions. Do not continue to use this website if you do not agree to all the terms and conditions stated on this page.
        
        The following terminology applies to these Terms and Conditions, Privacy Statement, and Disclaimer Notice and all agreements: "Client", "You", and "Your" refers to you, the person log on this website and compliant to the Company’s terms and conditions. "The Company", "Ourselves", "We", "Our", and "Us", refers to our Company. "Party", "Parties", or "Us", refers to both the Client and ourselves.

        Cookies: We employ the use of cookies. By accessing our website, you agreed to use cookies in agreement with our Privacy Policy.

        if you have any  questions , you can feel free to message us.
        """
        
        st.write(terms_and_conditions)
        if st.button("Back"):
            go_back()

    elif st.session_state.active_section == 'privacy':
        st.header("Privacy Policy")
    
        privacy_policy_content = """
        We value your privacy at [Your Company Name]. This Privacy Policy outlines the types of personal information that we receive and collect when you use our services, as well as how we use, disclose, and safeguard that information.

        Information Collection and Use:
        - When you use our services, we may collect personal information such as your name, email address, and other contact details that you provide voluntarily.
        - We may also automatically collect information such as your IP address, browser type, and operating system for analytics and service improvement purposes.

        Use of Information:
        - We may use the information collected for purposes such as providing and improving our services, sending promotional communications, and personalizing user experience.

        Disclosure of Information:
        - We do not sell, trade, or otherwise transfer your personal information to outside parties unless we provide you with advance notice.

        """

        st.write(privacy_policy_content)
        if st.button("Back"):
            go_back()

    elif st.session_state.active_section == 'faq':
        st.header("FAQ")
    
        faq_content = """
        **Q: How do I upload a PDF document?**
        A: To upload a PDF, click on the 'Upload' button, select the PDF file from your device, and then click 'Submit'.

        **Q: What file size limit is allowed for PDF uploads?**
        A: Currently, we allow PDF uploads of up to 50MB in size.

        **Q: Which types of PDF files can be processed?**
        A: Our software can process standard PDF files with text, images, and basic formatting. Encrypted or password-protected PDFs may not be supported.

        **Q: Can I edit or modify the content of the uploaded PDF?**
        A: Yes, our software offers features for editing, annotating, and extracting content from PDFs.

        **Q: Is there a limit to the number of PDFs I can upload?**
        A: No, you can upload multiple PDFs for processing within a single session.

        **Q: How secure is my uploaded PDF document?**
        A: We take security seriously. Your uploaded PDFs are encrypted, and our system ensures data privacy and protection.

        **Q: Can I convert PDFs to other file formats using your software?**
        A: Yes, our software supports PDF conversion to various formats like Word, Excel, and more.

        **Q: Is the processing of PDFs done on the client-side or server-side?**
        A: Our processing primarily takes place on our secure servers to ensure efficient and accurate results.

        **Q: What happens to my uploaded files after processing?**
        A: Your processed files are available for download for a limited time. We don't store files indefinitely for privacy reasons.

        **Q: Do you provide customer support in case of any issues or questions?**
        A: Yes, our support team is available to assist you with any queries or technical difficulties.
        """

        st.write(faq_content)
        if st.button("Back"):
            go_back()

    elif st.session_state.active_section == 'login':
        st.header("Login")
        st.write("Content for Login...")
        if st.button("Back"):
            go_back()

    else:
        # st.write("Please select an option from the sidebar.")
        # display_pdf_processing_section()
        
        # Upload PDF file through Streamlit
        uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

        if uploaded_file is not None:
            # Save the uploaded file to a temporary location
            temp_file_path = save_uploaded_file(uploaded_file)

            # Display uploaded file details
            st.success(
                f"File uploaded: {uploaded_file.name} ({round(uploaded_file.size / 1024, 2)} KB)"
            )

            # Process the PDF using langchain
            loader = PyMuPDFLoader(temp_file_path)
            pages = loader.load()

            # Display page count
            st.info(f"Number of pages in the PDF: {len(pages)}")

            # Choose the page number
            starting_page = st.number_input("Starting page", value=1, min_value=1, max_value=len(pages))

            option = st.radio(
            "choose your option👇",
            ["summary", "Q&A", "both"],
            key="visibility")


            if option == "summary":
                if "summary_generated" not in st.session_state:
                    st.session_state.summary_generated = False
                
                if st.button(f"Generate Summary"):
                    summary1 = " "
                    for i in range(starting_page,starting_page+3):
                        summary1 += generate_summ(pages[i].page_content, summary_prompt) + "\n\n"
                    st.text_area(f"Summary for page {starting_page}-{starting_page+2}:", summary1)
                    st.session_state.summary_generated = True
                    st.download_button(':orange[Download]', summary1)
                    st.session_state.summary_generated = True
                    st.session_state.summary2 = summary1
                if st.session_state.summary_generated and st.button(f"Continue summary for page {starting_page+3}-{len(pages)}"):
                        remaining_summary = " "
                        for i in range(starting_page+3, len(pages)):
                            remaining_summary += generate_summ(pages[i].page_content, summary_prompt) + "\n\n"
                        st.text_area("Remaining Summary:", st.session_state.summary2 +' ' +remaining_summary)
                        st.download_button(':orange[Download]',st.session_state.summary2 +' ' + remaining_summary)
                        st.session_state.summary_generated = False

            elif option== "Q&A":
                if "QanAns_generated" not in st.session_state:
                    st.session_state.QanAns_generated = False
                
                if st.button(f"Generate Q&A"):
                    QanAns = " "
                    for i in range(starting_page,starting_page+3):
                        QanAns += generate_QA(pages[i].page_content, Qans_prompt) + "\n\n"
                    st.text_area(f"Q&A for page {starting_page}-{starting_page+2}:", QanAns)
                    st.download_button(':orange[Download]', QanAns)
                    st.session_state.QanAns_generated = True
                    st.session_state.QanAns2 = QanAns
                if st.session_state.QanAns_generated and st.button(f"Continue Q&A for page {starting_page+3}-{len(pages)}"):
                        remaining_QanAns = " "
                        for i in range(starting_page+3, len(pages)):
                            remaining_QanAns += generate_QA(pages[i].page_content, Qans_prompt) + "\n\n"
                        st.text_area("Remaining QanAns:", st.session_state.QanAns2 +' ' +remaining_QanAns)
                        st.download_button(':orange[Download]',st.session_state.QanAns2 + ' ' + remaining_QanAns)
                        st.session_state.QanAns_generated = False

            elif option== "both":
                if "summary_generated" not in st.session_state:
                    st.session_state.summary_generated = False
                if "QanAns_generated" not in st.session_state:
                    st.session_state.QanAns_generated = False
                summary =  " "
                QanAns = " "
                if st.button(f"Generate both"):
                    for i in range(starting_page,starting_page+3):
                        # Generate and display the summary for the selected page
                        summary += generate_summ(pages[i].page_content, summary_prompt) + "\n\n"
                        QanAns += generate_QA(summary, Qans_prompt) + "\n\n"
                    # Display the combined summary and Q&A in the same text area
                    st.text_area(f"Summary and Q&A for page {starting_page}-{starting_page+2}:", f"{summary}\n\n{QanAns}")
                    st.download_button(':orange[Download]', f"{summary}\n\n{QanAns}")
                    st.session_state.summary_generated = True
                    st.session_state.summary3 = summary
                    st.session_state.QanAns_generated = True
                    st.session_state.QanAns3 = QanAns
                if st.session_state.QanAns_generated and st.button(f"Continue for page {starting_page+3}-{len(pages)}"):
                        remaining_QanAns3 = " "
                        remaining_summary = " "
                        for i in range(starting_page+3, len(pages)):
                            remaining_summary += generate_summ(pages[i].page_content, summary_prompt) + "\n\n"
                            remaining_QanAns3 += generate_QA(pages[i].page_content,Qans_prompt)  + "\n\n"
                        st.text_area("Remaining QanAns:",f"{st.session_state.summary3 +' ' + remaining_summary}\n\n{st.session_state.QanAns3 +' ' +remaining_QanAns3}")
                        st.download_button(':orange[Download]',f"{st.session_state.summary3 +' ' + remaining_summary}\n\n{st.session_state.QanAns3 +' ' + remaining_QanAns3}")
                        st.session_state.summary_generated = False
                        st.session_state.QanAns_generated = False


if __name__ == "__main__":
    main()