from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
from bertopic import BERTopic
import os
from werkzeug.utils import secure_filename
import json
import joblib

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Import preprocessing functions
from utils.predictions import prediksi_teks, prediksi_file
from utils.visualizations import generate_wordcloud, generate_barchart, generate_wordcloud_by_stance, generate_wordcloud_by_topic

# Topic mapping
TOPIC_MAPPING = {
    0: "Kebijakan dan Isu Sosial",
    1: "Politik dan Figur Publik",
    2: "Investasi dan Dunia Usaha",
    3: "Pertumbuhan Ekonomi dan Infrastruktur",
    4: "Strategi dan Perencanaan",
    5: "Kritik dan Tantangan Implementasi",
    6: "Transformasi dan Modernisasi"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict/text', methods=['POST'])
def predict_text():
    try:
        data = request.get_json()
        teks_input = data.get('text', '')
        
        if not teks_input:
            return jsonify({'error': 'Teks tidak boleh kosong'}), 400
        
        # Paths to models
        model_stance_path = 'model_terbaik.pkl'
        vectorizer_stance_path = 'vectorizer_terbaik.pkl'
        topic_model_path = 'model_bertopic'
        
        hasil = prediksi_teks(
            teks_input, 
            model_stance_path, 
            vectorizer_stance_path, 
            topic_model_path
        )
        
        # Add topic label
        hasil['topik_label'] = TOPIC_MAPPING.get(hasil['topik'], 'Unknown')
        
        return jsonify(hasil)
    
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"Error in predict_text: {error_detail}")
        return jsonify({'error': str(e), 'detail': error_detail}), 500

@app.route('/predict/file', methods=['POST'])
def predict_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Tidak ada file yang diupload'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'Tidak ada file yang dipilih'}), 400
        
        if file and file.filename.endswith('.csv'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Paths to models
            model_stance_path = 'model_terbaik.pkl'
            vectorizer_stance_path = 'vectorizer_terbaik.pkl'
            topic_model_path = 'model_bertopic'
            
            hasil_df = prediksi_file(
                filepath,
                model_stance_path,
                vectorizer_stance_path,
                topic_model_path
            )
            
            # Add topic labels
            hasil_df['topik_label'] = hasil_df['topik'].map(TOPIC_MAPPING)
            
            # Generate all visualizations immediately
            barchart_b64 = generate_barchart(hasil_df, TOPIC_MAPPING)
            wordcloud_stance = generate_wordcloud_by_stance(hasil_df)
            wordcloud_topic = generate_wordcloud_by_topic(hasil_df, TOPIC_MAPPING)
            
            # Convert to dict for JSON response
            hasil_list = hasil_df.to_dict('records')
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify({
                'results': hasil_list,
                'visualizations': {
                    'barchart': barchart_b64,
                    'wordcloud_stance': wordcloud_stance,
                    'wordcloud_topic': wordcloud_topic
                }
            })
        
        return jsonify({'error': 'File harus berformat CSV'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/visualize/wordcloud_stance', methods=['POST'])
def visualize_wordcloud_stance():
    try:
        data = request.get_json()
        results = data.get('results', [])
        
        if not results:
            return jsonify({'error': 'Tidak ada data untuk visualisasi'}), 400
        
        wordclouds = generate_wordcloud_by_stance(results)
        
        return jsonify({'wordclouds': wordclouds})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/visualize/wordcloud_topic', methods=['POST'])
def visualize_wordcloud_topic():
    try:
        data = request.get_json()
        results = data.get('results', [])
        
        if not results:
            return jsonify({'error': 'Tidak ada data untuk visualisasi'}), 400
        
        wordclouds = generate_wordcloud_by_topic(results, TOPIC_MAPPING)
        
        return jsonify({'wordclouds': wordclouds})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/visualize/barchart', methods=['POST'])
def visualize_barchart():
    try:
        data = request.get_json()
        results = data.get('results', [])
        
        if not results:
            return jsonify({'error': 'Tidak ada data untuk visualisasi'}), 400
        
        barchart_base64 = generate_barchart(results, TOPIC_MAPPING)
        
        return jsonify({'barchart': barchart_base64})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
