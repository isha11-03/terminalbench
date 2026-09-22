"""
Generate a deterministic trained model and test data for the inference pipeline.
This ensures reproducibility across all test runs.
"""
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from pathlib import Path
import json


def set_seed(seed=42):
    """Set random seed for reproducibility."""
    np.random.seed(seed)


def generate_training_data():
    """Generate synthetic but realistic training data."""
    # Positive sentiment examples
    positive = [
        "excellent product highly recommend amazing quality",
        "love this item works perfectly great value",
        "fantastic experience wonderful service happy customer",
        "best purchase ever outstanding performance",
        "incredible quality exceeded expectations delighted",
        "superb product worth every penny satisfied",
        "amazing results highly satisfied wonderful",
        "perfect exactly what needed great quality",
        "outstanding value excellent choice recommended",
        "brilliant product very happy great purchase",
    ]
    
    # Negative sentiment examples
    negative = [
        "terrible product waste money disappointed",
        "horrible quality broke immediately awful",
        "worst purchase ever completely useless regret",
        "poor quality unreliable terrible experience",
        "disappointing product failed expectations bad",
        "awful service terrible quality unhappy",
        "waste money poor performance disappointed",
        "terrible experience bad quality regret buying",
        "horrible product unreliable poor value",
        "worst quality terrible waste disappointed",
    ]
    
    # Neutral sentiment examples
    neutral = [
        "product okay average quality acceptable",
        "standard item nothing special adequate",
        "average product decent quality okay",
        "acceptable quality reasonable price standard",
        "okay product average performance adequate",
        "decent quality standard item acceptable",
        "average purchase okay quality reasonable",
        "standard quality acceptable product okay",
        "reasonable quality average item adequate",
        "okay value standard quality acceptable",
    ]
    
    # Combine all data
    texts = positive + negative + neutral
    labels = [2] * len(positive) + [0] * len(negative) + [1] * len(neutral)
    
    return texts, labels


def generate_test_data():
    """Generate deterministic test data."""
    test_samples = [
        "excellent product very satisfied happy",
        "terrible quality waste money",
        "average product okay quality",
        "amazing wonderful fantastic love",
        "horrible awful terrible worst",
        "standard acceptable adequate okay",
        "perfect brilliant outstanding superb",
        "disappointing poor bad regret",
        "decent reasonable standard",
        "incredible exceeded expectations",
    ]
    
    expected_labels = [
        'positive', 'negative', 'neutral', 'positive', 'negative',
        'neutral', 'positive', 'negative', 'neutral', 'positive'
    ]
    
    return test_samples, expected_labels


def main():
    set_seed(42)
    
    # Create output directory
    output_dir = Path(__file__).parent / "model"
    output_dir.mkdir(exist_ok=True)
    
    # Generate training data
    train_texts, train_labels = generate_training_data()
    
    # Train TF-IDF vectorizer
    print("Training TF-IDF vectorizer...")
    vectorizer = TfidfVectorizer(
        max_features=100,
        ngram_range=(1, 2),
        min_df=1,
        random_state=42
    )
    X_train = vectorizer.fit_transform(train_texts)
    
    # Train logistic regression model
    print("Training logistic regression model...")
    model = LogisticRegression(
        random_state=42,
        max_iter=1000,
        solver='lbfgs',
        multi_class='multinomial'
    )
    model.fit(X_train, train_labels)
    
    # Save model and vectorizer
    print("Saving model artifacts...")
    with open(output_dir / "vectorizer.pkl", 'wb') as f:
        pickle.dump(vectorizer, f)
    
    with open(output_dir / "model.pkl", 'wb') as f:
        pickle.dump(model, f)
    
    # Generate and save test data
    test_samples, expected_labels = generate_test_data()
    test_data = {
        'samples': test_samples,
        'expected_labels': expected_labels
    }
    
    with open(output_dir / "test_data.json", 'w') as f:
        json.dump(test_data, f, indent=2)
    
    # Generate baseline predictions for correctness validation
    print("Generating baseline predictions...")
    from inference_pipeline import InferencePipeline
    
    pipeline = InferencePipeline(model_dir=str(output_dir))
    baseline_predictions = pipeline.predict(test_samples)
    
    with open(output_dir / "baseline_predictions.json", 'w') as f:
        json.dump(baseline_predictions, f, indent=2)
    
    print("Model and test data generated successfully!")
    print(f"Output directory: {output_dir}")
    print(f"Training samples: {len(train_texts)}")
    print(f"Test samples: {len(test_samples)}")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    main()
