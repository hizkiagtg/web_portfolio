import pickle
import re
import logging
from functools import lru_cache
from pathlib import Path
from typing import Dict, Optional
from django.conf import settings
from sklearn.feature_extraction.text import TfidfVectorizer
from mpstemmer import MPStemmer
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import nltk

logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


class SpamClassificationService:
    """Service class for handling spam classification with ML models"""
    
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.X_train = None
        self._load_model()
    
    def _load_model(self):
        """Load the trained model and required components"""
        try:
            base_dir = Path(settings.BASE_DIR)
            model_path = base_dir / 'best_svc.pickle'
            x_train_path = base_dir / 'X_train.pickle'
            
            if model_path.exists() and x_train_path.exists():
                self.model = pickle.load(open(model_path, 'rb'))
                self.X_train = pickle.load(open(x_train_path, 'rb'))
                
                # Initialize and fit vectorizer
                self.vectorizer = TfidfVectorizer(tokenizer=self._preprocessing)
                self.vectorizer.fit_transform(self.X_train)
                
                logger.info("ML model loaded successfully")
            else:
                logger.warning("ML model files not found")
                
        except Exception as e:
            logger.error(f"Error loading ML model: {e}")
    
    def _preprocessing(self, sentence: str) -> list:
        """Preprocess text for classification"""
        try:
            stop_factory = StopWordRemoverFactory()
            stop_words_list = stop_factory.get_stop_words()
            stop_words_set = set(stop_words_list)
            result = []

            # Regex for tokenization
            tokenizer_pattern = r'\w+'

            # For stemming and lemmatization
            stemmer = MPStemmer()

            # Tokenization, stemming, and stopword removal
            tokens = re.findall(tokenizer_pattern, sentence)
            for token in tokens:
                token = stemmer.stem(token).lower()
                if token and token not in stop_words_set:
                    result.append(token)
            return result
        except Exception as e:
            logger.error(f"Error in preprocessing: {e}")
            return []
    
    @lru_cache(maxsize=1000)
    def predict(self, text: str) -> Dict[str, any]:
        """
        Predict if text is spam or not
        
        Args:
            text: Input text to classify
            
        Returns:
            Dict containing prediction and confidence
        """
        if not self.model or not self.vectorizer:
            return {
                'prediction': 'unknown',
                'confidence': 0.0,
                'error': 'Model not loaded'
            }
        
        try:
            # Transform text
            text_vector = self.vectorizer.transform([text])
            
            # Get prediction
            prediction = self.model.predict(text_vector)[0]
            
            # Get confidence if model supports it
            confidence = None
            if hasattr(self.model, 'predict_proba'):
                probabilities = self.model.predict_proba(text_vector)[0]
                confidence = max(probabilities)
            elif hasattr(self.model, 'decision_function'):
                decision_score = self.model.decision_function(text_vector)[0]
                confidence = abs(decision_score)
            
            result = 'spam' if prediction == 1 else 'not_spam'
            
            return {
                'prediction': result,
                'confidence': confidence,
                'message': self._get_prediction_message(result)
            }
            
        except Exception as e:
            logger.error(f"Error in prediction: {e}")
            return {
                'prediction': 'unknown',
                'confidence': 0.0,
                'error': str(e)
            }
    
    def _get_prediction_message(self, prediction: str) -> str:
        """Get human-readable message for prediction"""
        if prediction == 'spam':
            return 'This message is SPAM'
        elif prediction == 'not_spam':
            return 'This message is not SPAM'
        else:
            return 'Unable to classify this message'
    
    def is_model_loaded(self) -> bool:
        """Check if model is properly loaded"""
        return self.model is not None and self.vectorizer is not None


# Global instance
spam_classifier = SpamClassificationService()