import re
import pandas as pd
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# Setup stopwords
try:
    from nltk.corpus import stopwords as nltk_stopwords
    stopwords_nltk = set(nltk_stopwords.words('indonesian'))
except:
    stopwords_nltk = set()

pabrik_sastrawi = StopWordRemoverFactory()
stopwords_sastrawi = set(pabrik_sastrawi.get_stop_words())
stopwords_gabungan = stopwords_nltk.union(stopwords_sastrawi)

stopwords_kustom = {
    'halo', 'hai', 'terima', 'kasih', 'permisi', 'selamat',
    'pagi', 'siang', 'sore', 'malam', 'mohon', 'ijin', 'maaf',
    'assalamualaikum', 'wrwb', 'nya', 'sih', 'aja', 'dong', 'deh',
    'kak', 'gan', 'min', 'bang', 'pak', 'bu', 'mas', 'mbak', 'yg', 'yang', 'kok', 'gak', 'ga', 'dan', 'di',
    'banget', 'pakai', 'baik', 'kalo', 'pas', 'ganti', 'kali', 'coba', 'livin', 'bagu', 'apk'
}
stopwords_gabungan = stopwords_gabungan.union(stopwords_kustom)

# Setup stemmer
pabrik_stemmer = StemmerFactory()
stemmer = pabrik_stemmer.create_stemmer()

# Load kamus normalisasi
url_kamus = "https://raw.githubusercontent.com/nasalsabila/kamus-alay/master/colloquial-indonesian-lexicon.csv"
try:
    df_normalisasi = pd.read_csv(url_kamus)
    kamus_normalisasi = dict(zip(df_normalisasi['slang'], df_normalisasi['formal']))
    # Hapus beberapa slang yang dikecualikan
    for slang in ['mbg', 'mba']:
        kamus_normalisasi.pop(slang, None)
except:
    kamus_normalisasi = {}

print(f"Jumlah stopwords: {len(stopwords_gabungan)}")
print(f"Jumlah kamus normalisasi: {len(kamus_normalisasi)}")


def proses_teks(teks):
    """Preprocessing teks lengkap: cleaning, normalisasi, stopword removal, stemming"""
    if pd.isna(teks) or teks == '':
        return '', []
    
    teks = str(teks)
    
    # Cleaning
    teks = re.sub(r'<[^>]+>', ' ', teks)

    # hapus URL http / https / www
    teks = re.sub(r'http\S+|www\S+', ' ', teks)

    # hapus domain tanpa http (contoh: faridnugroho.com/2014/06/bursa)
    teks = re.sub(r'\b[a-zA-Z0-9.-]+\.(com|id|org|net|co)(/\S*)?', ' ', teks)

    # hapus email
    teks = re.sub(r'\S+@\S+', ' ', teks)

    # hapus mention & hashtag
    teks = re.sub(r'@\w+', ' ', teks)
    teks = re.sub(r'#\w+', ' ', teks)

    # hapus angka
    teks = re.sub(r'\d+', ' ', teks)

    # hapus karakter aneh non-ascii (misalnya â€¦)
    teks = teks.encode('ascii', 'ignore').decode('ascii')

    # sisakan huruf saja
    teks = re.sub(r'[^a-zA-Z\s]', ' ', teks)

    # rapikan spasi & lowercase
    teks = re.sub(r'\s+', ' ', teks).strip().lower()
    
    # Tokenisasi
    teks = re.sub(r'(.)\1{2,}', r'\1', teks)
    tokens = teks.split()
    
    # Normalisasi slang
    if kamus_normalisasi:
        tokens = [kamus_normalisasi.get(kata, kata) for kata in tokens]
    
    # Stopword removal
    tokens = [kata for kata in tokens if kata not in stopwords_gabungan and len(kata) > 2]
    
    # Stemming
    tokens = [stemmer.stem(kata) for kata in tokens]
    
    teks_bersih = ' '.join(tokens)
    
    return teks_bersih, tokens


# # Backward compatibility functions for existing code
# def cleaning(text):
#     """Clean text by removing URLs, mentions, hashtags, and special characters"""
#     text = re.sub(r'<[^>]+>', ' ', text)
#     text = re.sub(r'http\S+|www\S+', '', text)
#     text = re.sub(r'\S+@\S+', '', text)
#     text = re.sub(r'@\w+', '', text)
#     text = re.sub(r'#\w+', '', text)
#     text = re.sub(r'\d+', '', text)
#     text = re.sub(r'[^a-zA-Z\s]', ' ', text)
#     text = re.sub(r'\s+', ' ', text).strip()
#     return text

# def casefolding(text):
#     """Convert text to lowercase"""
#     return text.lower()

# def tokenize(text):
#     """Tokenize text into words"""
#     text = re.sub(r'(.)\1{2,}', r'\1', text)
#     return text.split()

# def normalize(tokens):
#     """Normalize tokens using normalization dictionary"""
#     if kamus_normalisasi:
#         return [kamus_normalisasi.get(token, token) for token in tokens]
#     return tokens

# def remove_stopwords(tokens):
#     """Remove stopwords from tokens"""
#     if not tokens or len(tokens) == 0:
#         return []
#     return [kata for kata in tokens if kata not in stopwords_gabungan and len(kata) > 2]

# def stem(tokens):
#     """Stem tokens using Sastrawi stemmer"""
#     if not tokens or len(tokens) == 0:
#         return []
#     return [stemmer.stem(kata) for kata in tokens]
