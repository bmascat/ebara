# Literature Review Assistant (LRA)

## Introduction

The Literature Review Assistant (LRA) is a tool designed to assist researchers and healthcare professionals in retrieving and analyzing scientific articles from PubMed. It leverages advanced language models to generate optimized search queries and provide evidence-based responses to user queries about diseases, treatments, and pharmaceuticals.

## Installation

To install the Literature Review Assistant (LRA), follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/literature-review-assistant.git
   cd lit-review-assistant
   ```

2. **Install the required dependencies:**

   Ensure you have Python installed, then run:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface

To use the CLI version of the assistant, run:
```bash
python src/cli.py
```

You will be prompted to enter your question about diseases, treatments, or pharmaceuticals. Type your question and press Enter. To exit, type `exit`.

### Web Interface

The assistant also provides a web interface using Streamlit. To start the web server, run:

```bash
streamlit run src/streamlit_app.py
```
Open your web browser and navigate to `http://localhost:8501` to access the interface.

### FastAPI Endpoint

To start the FastAPI endpoint, run:

```bash
uvicorn src.main:app --reload
```
Open your web browser and navigate to `http://localhost:8000` to access the endpoint.

## Features

- **Advanced Query Generation:** Converts user questions into optimized PubMed search queries.
- **Article Retrieval:** Fetches relevant articles from PubMed using the generated queries.
- **Embedding Processing:** Processes article abstracts to find the most relevant documents.
- **Response Generation:** Provides evidence-based answers to user queries.
- **Database Storage:** Saves queries, responses, and context for future reference.

## Contributing

We welcome contributions to the PubMed AI Research Assistant. To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with clear messages.
4. Push your changes to your fork.
5. Submit a pull request to the main repository.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

### Code References

- CLI Implementation: `src/cli.py`
- Streamlit Web Interface: `src/streamlit_app.py`
- FastAPI Endpoint Implementation: `src/main.py`
- Model Manager and Query Generation: `src/models/model_manager.py`
- Embedding Processing: `src/models/embedding_processor.py`
- Database Management: `src/models/database_manager.py`

This documentation provides a comprehensive overview of the software, including how to install, use, and contribute to it. Adjust the contact information and repository URL as needed.