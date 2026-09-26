from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import io
import base64
import pandas as pd
import numpy as np

def generate_wordcloud(texts):
    """
    Generate wordcloud from a list of texts
    """
    # Combine all texts
    combined_text = ' '.join(texts)
    
    # Generate wordcloud
    wordcloud = WordCloud(
        width=800, 
        height=400,
        background_color='white',
        colormap='viridis',
        max_words=100,
        relative_scaling=0.5,
        min_font_size=10
    ).generate(combined_text)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    plt.tight_layout(pad=0)
    
    # Convert to base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return image_base64

def generate_barchart(results, topic_mapping):
    """
    Generate barchart for stance and topic distribution
    """
    df = pd.DataFrame(results)
    
    # Create subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Color palette from the image (gold/tan colors)
    colors = ['#C9A55B', '#B8945A', '#A78359', '#967258', '#856157']
    
    # Stance distribution
    stance_counts = df['stance'].value_counts()
    ax1.bar(stance_counts.index, stance_counts.values, color=colors[0])
    ax1.set_xlabel('Stance', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Jumlah', fontsize=12, fontweight='bold')
    ax1.set_title('Distribusi Stance', fontsize=14, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # Topic distribution
    topic_counts = df['topik'].value_counts().sort_index()
    topic_labels = [topic_mapping.get(t, f'Topic {t}') for t in topic_counts.index]
    
    ax2.barh(topic_labels, topic_counts.values, color=colors[1])
    ax2.set_xlabel('Jumlah', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Topik', fontsize=12, fontweight='bold')
    ax2.set_title('Distribusi Topik', fontsize=14, fontweight='bold')
    ax2.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    
    # Convert to base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return image_base64

def generate_wordcloud_by_stance(results):
    """
    Generate separate wordclouds for each stance
    """
    df = pd.DataFrame(results)
    wordclouds = {}
    
    # Color maps for different stances
    colormaps = {
        'Favor': 'Greens',
        'Against': 'Reds',
        'Neutral': 'Blues',
        'None': 'Greys'
    }
    
    for stance in df['stance'].unique():
        stance_data = df[df['stance'] == stance]
        texts = stance_data['teks_preprocessing'].tolist()
        
        if texts and len(texts) > 0:
            combined_text = ' '.join(texts)
            
            if combined_text.strip():
                # Generate wordcloud
                colormap = colormaps.get(stance, 'viridis')
                wordcloud = WordCloud(
                    width=600, 
                    height=400,
                    background_color='white',
                    colormap=colormap,
                    max_words=80,
                    relative_scaling=0.5,
                    min_font_size=8
                ).generate(combined_text)
                
                # Create figure
                fig, ax = plt.subplots(figsize=(8, 5))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                plt.tight_layout(pad=0)
                
                # Convert to base64
                buffer = io.BytesIO()
                plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
                buffer.seek(0)
                image_base64 = base64.b64encode(buffer.getvalue()).decode()
                plt.close()
                
                wordclouds[stance] = image_base64
    
    return wordclouds

def generate_wordcloud_by_topic(results, topic_mapping):
    """
    Generate separate wordclouds for each topic
    """
    df = pd.DataFrame(results)
    wordclouds = {}
    
    # Colormap for topics
    colormaps = ['autumn', 'winter', 'spring', 'summer', 'cool', 'hot', 'copper']
    
    for idx, topic_id in enumerate(df['topik'].unique()):
        topic_data = df[df['topik'] == topic_id]
        texts = topic_data['teks_preprocessing'].tolist()
        topic_label = topic_mapping.get(topic_id, f'Topic {topic_id}')
        
        if texts and len(texts) > 0:
            combined_text = ' '.join(texts)
            
            if combined_text.strip():
                # Generate wordcloud
                colormap = colormaps[idx % len(colormaps)]
                wordcloud = WordCloud(
                    width=600, 
                    height=400,
                    background_color='white',
                    colormap=colormap,
                    max_words=80,
                    relative_scaling=0.5,
                    min_font_size=8
                ).generate(combined_text)
                
                # Create figure
                fig, ax = plt.subplots(figsize=(8, 5))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                plt.tight_layout(pad=0)
                
                # Convert to base64
                buffer = io.BytesIO()
                plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
                buffer.seek(0)
                image_base64 = base64.b64encode(buffer.getvalue()).decode()
                plt.close()
                
                wordclouds[topic_label] = image_base64
    
    return wordclouds
