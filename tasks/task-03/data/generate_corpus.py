#!/usr/bin/env python3
"""
Generate deterministic document corpus with embeddings for retrieval task.
Uses a simple deterministic embedding method based on word statistics.
"""

import json
import numpy as np
from pathlib import Path


def deterministic_embedding(text: str, dim: int = 64, seed: int = 42) -> np.ndarray:
    """
    Create deterministic embedding from text using word-based features.
    This simulates a simple embedding model without requiring downloads.
    """
    # Normalize text
    text = text.lower().strip()
    words = text.split()
    
    if not words:
        return np.zeros(dim)
    
    # Use both word hash and word itself for better semantic similarity
    embedding = np.zeros(dim)
    word_count = {}
    
    # Count words
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1
    
    # Generate embedding from unique words with their frequencies
    for word, count in word_count.items():
        # Use word hash as seed for deterministic random features
        word_seed = seed + hash(word) % (2**31)
        rng = np.random.RandomState(word_seed)
        word_vec = rng.randn(dim)
        
        # Weight by word frequency (TF-like)
        weight = np.sqrt(count)  # Sublinear scaling
        embedding += word_vec * weight
    
    # Length normalization (longer documents shouldn't dominate)
    doc_length_norm = 1.0 / np.sqrt(len(words))
    embedding = embedding * doc_length_norm
    
    # Normalize to unit vector
    norm = np.linalg.norm(embedding)
    if norm > 0:
        embedding = embedding / norm
    
    return embedding


def generate_corpus():
    """Generate document corpus with metadata and embeddings."""
    
    documents = [
        {
            "id": "doc_001",
            "title": "Introduction to Machine Learning",
            "text": "Machine learning is a branch of artificial intelligence that focuses on building systems that learn from data. It uses statistical techniques to give computers the ability to learn without being explicitly programmed.",
            "category": "ml",
            "year": 2020,
            "tags": ["machine-learning", "ai", "basics"]
        },
        {
            "id": "doc_002",
            "title": "Deep Learning Fundamentals",
            "text": "Deep learning is a subset of machine learning that uses neural networks with multiple layers. These deep neural networks can learn hierarchical representations of data.",
            "category": "ml",
            "year": 2021,
            "tags": ["deep-learning", "neural-networks", "ml"]
        },
        {
            "id": "doc_003",
            "title": "Natural Language Processing Overview",
            "text": "Natural language processing enables computers to understand, interpret, and generate human language. It combines linguistics and machine learning to process text data.",
            "category": "nlp",
            "year": 2021,
            "tags": ["nlp", "text-processing", "linguistics"]
        },
        {
            "id": "doc_004",
            "title": "Computer Vision Techniques",
            "text": "Computer vision allows machines to interpret and understand visual information from the world. It uses deep learning models to analyze images and videos.",
            "category": "cv",
            "year": 2022,
            "tags": ["computer-vision", "image-processing", "deep-learning"]
        },
        {
            "id": "doc_005",
            "title": "Reinforcement Learning Basics",
            "text": "Reinforcement learning is a type of machine learning where agents learn to make decisions by interacting with an environment. The agent receives rewards or penalties based on its actions.",
            "category": "ml",
            "year": 2020,
            "tags": ["reinforcement-learning", "agents", "ml"]
        },
        {
            "id": "doc_006",
            "title": "Neural Network Architectures",
            "text": "Neural networks consist of interconnected nodes organized in layers. Different architectures like CNNs, RNNs, and transformers are designed for specific tasks.",
            "category": "ml",
            "year": 2022,
            "tags": ["neural-networks", "architectures", "deep-learning"]
        },
        {
            "id": "doc_007",
            "title": "Data Preprocessing Methods",
            "text": "Data preprocessing is crucial for machine learning success. It includes cleaning, normalization, encoding, and feature engineering to prepare raw data for models.",
            "category": "data",
            "year": 2019,
            "tags": ["preprocessing", "data-cleaning", "feature-engineering"]
        },
        {
            "id": "doc_008",
            "title": "Model Evaluation Metrics",
            "text": "Evaluating machine learning models requires appropriate metrics. Common metrics include accuracy, precision, recall, F1 score, and ROC curves for classification tasks.",
            "category": "ml",
            "year": 2020,
            "tags": ["evaluation", "metrics", "model-assessment"]
        },
        {
            "id": "doc_009",
            "title": "Transfer Learning Applications",
            "text": "Transfer learning leverages pre-trained models for new tasks. It enables faster training and better performance when labeled data is limited.",
            "category": "ml",
            "year": 2021,
            "tags": ["transfer-learning", "pre-trained", "fine-tuning"]
        },
        {
            "id": "doc_010",
            "title": "Attention Mechanisms Explained",
            "text": "Attention mechanisms allow models to focus on relevant parts of input data. They are fundamental to transformer architectures and have revolutionized natural language processing.",
            "category": "nlp",
            "year": 2022,
            "tags": ["attention", "transformers", "nlp"]
        },
        {
            "id": "doc_011",
            "title": "Unsupervised Learning Techniques",
            "text": "Unsupervised learning discovers patterns in data without labeled examples. Common techniques include clustering, dimensionality reduction, and anomaly detection.",
            "category": "ml",
            "year": 2020,
            "tags": ["unsupervised", "clustering", "anomaly-detection"]
        },
        {
            "id": "doc_012",
            "title": "Optimization Algorithms in ML",
            "text": "Optimization algorithms like gradient descent, Adam, and RMSprop are essential for training machine learning models. They minimize loss functions to find optimal parameters.",
            "category": "ml",
            "year": 2021,
            "tags": ["optimization", "gradient-descent", "training"]
        },
        {
            "id": "doc_013",
            "title": "Convolutional Neural Networks",
            "text": "Convolutional neural networks are specialized for processing grid-like data such as images. They use convolutional layers to automatically learn spatial hierarchies.",
            "category": "cv",
            "year": 2021,
            "tags": ["cnn", "convolution", "image-processing"]
        },
        {
            "id": "doc_014",
            "title": "Recurrent Neural Networks",
            "text": "Recurrent neural networks process sequential data by maintaining hidden states. They are used for time series, speech recognition, and language modeling.",
            "category": "nlp",
            "year": 2020,
            "tags": ["rnn", "sequential", "time-series"]
        },
        {
            "id": "doc_015",
            "title": "Generative Adversarial Networks",
            "text": "Generative adversarial networks consist of a generator and discriminator that compete. They can generate realistic synthetic data including images, text, and audio.",
            "category": "ml",
            "year": 2022,
            "tags": ["gan", "generative", "synthetic-data"]
        },
        {
            "id": "doc_016",
            "title": "Embedding Representations",
            "text": "Embeddings map discrete objects to continuous vector spaces. Word embeddings and sentence embeddings capture semantic relationships between text elements.",
            "category": "nlp",
            "year": 2021,
            "tags": ["embeddings", "vectors", "representation"]
        },
        {
            "id": "doc_017",
            "title": "Regularization Techniques",
            "text": "Regularization prevents overfitting in machine learning models. Techniques include L1, L2 regularization, dropout, and early stopping.",
            "category": "ml",
            "year": 2019,
            "tags": ["regularization", "overfitting", "dropout"]
        },
        {
            "id": "doc_018",
            "title": "Batch Normalization Benefits",
            "text": "Batch normalization normalizes layer inputs during training. It accelerates convergence, allows higher learning rates, and reduces sensitivity to initialization.",
            "category": "ml",
            "year": 2020,
            "tags": ["batch-norm", "normalization", "training"]
        },
        {
            "id": "doc_019",
            "title": "Ensemble Learning Methods",
            "text": "Ensemble learning combines multiple models to improve predictions. Popular methods include bagging, boosting, and stacking.",
            "category": "ml",
            "year": 2020,
            "tags": ["ensemble", "bagging", "boosting"]
        },
        {
            "id": "doc_020",
            "title": "Edge AI and Model Deployment",
            "text": "Edge AI deploys machine learning models on edge devices. It requires model compression, quantization, and optimization for resource-constrained environments.",
            "category": "deployment",
            "year": 2022,
            "tags": ["edge-ai", "deployment", "optimization"]
        }
    ]
    
    # Generate embeddings for all documents
    for doc in documents:
        # Combine title and text for embedding
        combined_text = f"{doc['title']} {doc['text']}"
        embedding = deterministic_embedding(combined_text, dim=64, seed=42)
        doc['embedding'] = embedding.tolist()
    
    return documents


def generate_queries():
    """Generate test queries with expected relevant documents."""
    
    queries = [
        {
            "id": "q_001",
            "text": "neural networks deep learning",
            "expected_relevant": ["doc_002", "doc_006", "doc_013"],  # Should rank highly
            "category_filter": None
        },
        {
            "id": "q_002",
            "text": "natural language processing text",
            "expected_relevant": ["doc_003", "doc_010", "doc_016"],
            "category_filter": "nlp"
        },
        {
            "id": "q_003",
            "text": "machine learning fundamentals",
            "expected_relevant": ["doc_001", "doc_008", "doc_012"],
            "category_filter": None
        },
        {
            "id": "q_004",
            "text": "image processing computer vision",
            "expected_relevant": ["doc_004", "doc_013"],
            "category_filter": "cv"
        },
        {
            "id": "q_005",
            "text": "training optimization algorithms",
            "expected_relevant": ["doc_012", "doc_018"],
            "category_filter": None
        },
        {
            "id": "q_006",
            "text": "",  # Empty query edge case
            "expected_relevant": [],
            "category_filter": None
        },
        {
            "id": "q_007",
            "text": "embeddings vectors representation",
            "expected_relevant": ["doc_016"],
            "category_filter": "nlp"
        },
        {
            "id": "q_008",
            "text": "generative models synthetic data",
            "expected_relevant": ["doc_015"],
            "category_filter": None
        },
        {
            "id": "q_009",
            "text": "reinforcement learning agents",
            "expected_relevant": ["doc_005"],
            "category_filter": "ml"
        },
        {
            "id": "q_010",
            "text": "data preprocessing cleaning",
            "expected_relevant": ["doc_007"],
            "category_filter": None
        }
    ]
    
    # Generate embeddings for queries
    for query in queries:
        embedding = deterministic_embedding(query['text'], dim=64, seed=42)
        query['embedding'] = embedding.tolist()
    
    return queries


def main():
    """Generate and save corpus and queries."""
    output_dir = Path(__file__).parent
    
    # Generate corpus
    corpus = generate_corpus()
    corpus_file = output_dir / "corpus.json"
    with open(corpus_file, 'w') as f:
        json.dump(corpus, f, indent=2)
    print(f"Generated {len(corpus)} documents -> {corpus_file}")
    
    # Generate queries
    queries = generate_queries()
    queries_file = output_dir / "queries.json"
    with open(queries_file, 'w') as f:
        json.dump(queries, f, indent=2)
    print(f"Generated {len(queries)} queries -> {queries_file}")
    
    print("\nCorpus statistics:")
    categories = {}
    for doc in corpus:
        cat = doc['category']
        categories[cat] = categories.get(cat, 0) + 1
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count} documents")


if __name__ == "__main__":
    main()
