# Automated News agent

## Project Overview
This project is an autonomous AI agent designed to:

- Search and crawl news articles from reliable sources.
- Summarize the extracted content into concise, well-structured articles.
- Optimize the content for SEO to improve discoverability.
- Save the generated articles locally due to hosting limitations.

## Key Features
### Automated Web Crawling:
- Fetches news articles from global and local sources.
- Example topics: Uttar Pradesh news (Lucknow news as a sub-topic), global technology news, etc.

### Summarization & Content Generation:
- Processes extracted text into concise summaries using a transformer-based summarization model (`facebook/bart-large-cnn`).
- Ensures factual accuracy and coherence.

### SEO Optimization:
- Adds metadata, keywords, and readability improvements.
- Generates engaging titles and meta descriptions for better ranking.

### Draft Saving:
- Articles are saved locally in `output.json` as drafts due to hosting restrictions (InfinityFree).

## Limitations
Due to InfinityFree's restrictions, REST API requests for publishing posts are blocked.

### Workaround:
- Articles are saved locally in `output.json`.
- These drafts can be manually copied into WordPress or another CMS.

## Deployment Instructions
Follow these steps to set up and run the application:

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the project root directory with the following variables:

```text
WP_SITE_ID="flipr-news.infy.uk"
WP_AUTH_TOKEN="your_generated_password"
```
**Note:** Replace `your_generated_password` with the application password generated in WordPress.

### 4. Run the Pipeline
Execute the main script to fetch, process, and save articles:
```bash
python main.py
```

### 5. View Generated Drafts
Check the `output.json` file for saved drafts in JSON format:

```json
{
    "title": "Test Title",
    "content": "This is a summarized article.",
    "seo_data": {
        "meta_description": "This is a summarized article...",
        "keywords": ["test", "article", "summary"],
        "readability_score": 70.5
    }
}
```

## Future Improvements
- Deploy on a hosting provider that supports REST APIs (e.g., 000WebHost or AwardSpace).
- Fix SSL chain issues for InfinityFree hosting.
- Add direct publishing functionality once REST API access is available.
- Implement multilingual support (e.g., Hindi translations).
- Add AI-generated images for enhanced blog posts.

## Repository Structure
```
.
├── main.py          # Main execution script
├── scraper.py       # Web scraping logic
├── processor.py     # Content processing and summarization logic
├── publisher.py     # Draft saving logic (local storage)
├── requirements.txt # Python dependencies
├── README.md        # Project documentation
└── output.json      # Generated drafts (local storage)
```

## Submission Notes
Due to hosting restrictions, the system currently saves drafts locally instead of publishing them directly to WordPress. The system has been tested and works as intended on other hosting providers or local WordPress installations.
