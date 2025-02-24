from transformers import pipeline
import torch
import textstat  # Replacement for pyseoanalyzer
from nltk import ngrams
import logging
import nltk

nltk.download('punkt')

# try:
#     from diffusers import StableDiffusionPipeline
# except ImportError:
#     logging.warning("Image generation disabled - install 'diffusers' package")

class ContentProcessor:
    def __init__(self):

        self.device="cpu"

        # loading the models according to the requirement into our device cpu/mps(gpu)

        self.torch_dtype =torch.float32

        self.seo_keyword_map = {
            "Uttar Pradesh": ["Lucknow", "Crime", "UP Police"],
            "Global": ["Technology", "World News"]
        }

        self.summarizer=pipeline("summarization",model="facebook/bart-large-cnn",device=self.device,torch_dtype=self.torch_dtype)

        # self.translator=pipeline("translation_en_to_hi",model="Helsinki-NLP/opus-mt-en-hi",device=self.device)

        # self.image_pipe=None
        # if 'StableDiffusionPipeline' in globals():
        #     self.image_pipe=StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0").to(self.device)

    def process_article(self, article):
        try:
            content = article['content']

            # Dynamic length calculation
            content_length = len(content.split())
            max_len = min(150, int(content_length * 0.7))
            min_len = min(30, max_len - 10)  # Ensure min < max

            summary = self.summarizer(
                content,
                max_length=max_len,
                min_length=min_len,
                do_sample=False
            )[0]['summary_text']

            return {
                'summary': summary,
                'seo_data': self._optimize_seo(summary, article['category'])
            }
        except Exception as e:
            logging.error(f"Processing failed: {str(e)}")
            return None

    def _optimize_seo(self, text, category):
        """SEO Optimization using Flesch Reading Ease (Problem Statement 3)"""
        try:
            # Calculate readability scores manually
            sentences = nltk.sent_tokenize(text)
            words = nltk.word_tokenize(text)
            num_sentences = len(sentences)
            num_words = len(words)
            num_syllables = sum(self._count_syllables(w) for w in words)

            # Flesch Reading Ease Formula (Search Result 8)
            if num_sentences > 0 and num_words > 0:
                flesch_score = 206.835 - (1.015 * (num_words / num_sentences)) - (84.6 * (num_syllables / num_words))
            else:
                flesch_score = 0  # Handle edge cases

            # Extract keywords using n-grams (Search Result 2 alternative)
            tokens = [w.lower() for w in words if w.isalnum()]
            bigrams = [' '.join(gram) for gram in ngrams(tokens, 2)]

            return {
                'meta_description': text[:150] + '...',
                'keywords': bigrams[:3] + self.seo_keyword_map.get(category, []),
                'readability_score': flesch_score
            }

        except Exception as e:
            logging.error(f"SEO optimization failed: {str(e)}")
            return {}

    def _count_syllables(self, word):
        """Custom syllable counter (Search Result 2 implementation)"""
        word = word.lower()
        count = 0
        vowels = "aeiouy"

        if len(word) == 0:
            return 0

        # Count vowel groups
        prev_char_vowel = False
        for char in word:
            if char in vowels:
                if not prev_char_vowel:
                    count += 1
                prev_char_vowel = True
            else:
                prev_char_vowel = False

        # Handle edge cases
        if word.endswith('e'):
            count -= 1
        if count == 0:
            count = 1

        return count

    # def _get_keywords(self,category,content_keywords):
    #     return content_keywords[:3]+self.seo_keyword_map.get(category,[])  #Final keyword list = [top 3 article keywords] + [predefined category keywords]











