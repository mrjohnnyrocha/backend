from hashlib import sha256

import logging
from transformers import RagTokenizer, RagTokenForGeneration
from neo4j import GraphDatabase

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class Neo4jClient:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()
    
    # Add methods for querying the knowledge graph as needed

def load_rag_model(model_name="facebook/rag-token-nq"):
    tokenizer = RagTokenizer.from_pretrained(model_name)
    model = RagTokenForGeneration.from_pretrained(model_name)
    return tokenizer, model

def generate_response(question, tokenizer, model):
    input_ids = tokenizer(question, return_tensors="pt").input_ids
    outputs = model.generate(input_ids)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer

def anonymize_identifier(identifier):
    return sha256(identifier.encode()).hexdigest()

def detect_oov_terms(query, known_vocabulary):
    words = query.split()  # Simple tokenization, consider using more sophisticated tokenization
    oov_terms = [word for word in words if word not in known_vocabulary]
    return oov_terms

