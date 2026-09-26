import pickle
import pandas as pd
from bertopic import BERTopic
from .preprocessing import proses_teks
import warnings
warnings.filterwarnings('ignore')

def prediksi_teks(teks_input, model_stance_path, vectorizer_stance_path, topic_model_path):
    """
    Predict stance and topic for a single text input
    """
    # Load models
    with open(model_stance_path, 'rb') as f:
        model_stance = pickle.load(f)
    with open(vectorizer_stance_path, 'rb') as f:
        vectorizer_stance = pickle.load(f)

    topic_model_loaded = BERTopic.load(topic_model_path)

    # Preprocessing dengan fungsi baru
    teks_final, tokens = proses_teks(teks_input)
    
    # Fallback jika hasil preprocessing kosong
    if not teks_final or teks_final.strip() == '':
        teks_final = teks_input.lower()

    # Stance prediction
    teks_vectorized = vectorizer_stance.transform([teks_final])
    prediksi_stance = model_stance.predict(teks_vectorized)[0]

    # Topic prediction with error handling
    try:
        topik, _ = topic_model_loaded.transform([teks_final])
        prediksi_topik = topik[0]
    except (IndexError, RuntimeError) as e:
        print(f"Warning: transform failed, using approximate_distribution: {e}")
        try:
            topic_distr, _ = topic_model_loaded.approximate_distribution([teks_final])
            prediksi_topik = topic_distr[0].argmax()
        except:
            prediksi_topik = 0

    # Convert numpy types to Python native types for JSON serialization
    if hasattr(prediksi_topik, 'item'):
        prediksi_topik = prediksi_topik.item()
    if hasattr(prediksi_stance, 'item'):
        prediksi_stance = prediksi_stance.item()

    return {
        'teks_asli': teks_input,
        'teks_preprocessing': teks_final,
        'stance': str(prediksi_stance),
        'topik': int(prediksi_topik)
    }

def prediksi_file(file_path, model_stance_path, vectorizer_stance_path, topic_model_path):
    """
    Predict stance and topic for multiple texts from a CSV file
    """
    # Load models
    with open(model_stance_path, 'rb') as f:
        model_stance = pickle.load(f)
    with open(vectorizer_stance_path, 'rb') as f:
        vectorizer_stance = pickle.load(f)

    topic_model_loaded = BERTopic.load(topic_model_path)

    # Read CSV file
    df = pd.read_csv(file_path)
    
    # Try to find the text column
    text_column = None
    for col in ['text', 'full_text', 'tweet', 'content', 'teks', 'Komentar']:
        if col in df.columns:
            text_column = col
            break
    
    if text_column is None:
        text_column = df.columns[0]
    
    results = []
    
    for idx, row in df.iterrows():
        teks_input = str(row[text_column])
        
        # Preprocessing dengan fungsi baru
        teks_final, tokens = proses_teks(teks_input)
        
        # Fallback jika hasil preprocessing kosong
        if not teks_final or teks_final.strip() == '':
            teks_final = teks_input.lower()

        # Stance prediction
        teks_vectorized = vectorizer_stance.transform([teks_final])
        prediksi_stance = model_stance.predict(teks_vectorized)[0]

        # Topic prediction with error handling
        try:
            topik, _ = topic_model_loaded.transform([teks_final])
            prediksi_topik = topik[0]
        except (IndexError, RuntimeError) as e:
            try:
                topic_distr, _ = topic_model_loaded.approximate_distribution([teks_final])
                prediksi_topik = topic_distr[0].argmax()
            except:
                prediksi_topik = 0

        # Convert numpy types to Python native types for JSON serialization
        if hasattr(prediksi_topik, 'item'):
            prediksi_topik = prediksi_topik.item()
        if hasattr(prediksi_stance, 'item'):
            prediksi_stance = prediksi_stance.item()

        results.append({
            'no': idx + 1,
            'teks_asli': teks_input,
            'teks_preprocessing': teks_final,
            'stance': str(prediksi_stance),
            'topik': int(prediksi_topik)
        })
    
    return pd.DataFrame(results)
