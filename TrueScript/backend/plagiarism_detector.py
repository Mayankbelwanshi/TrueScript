# backend/plagiarism_detector.py

import os

def check_plagiarism(uploaded_filepath):
    uploaded_content = open(uploaded_filepath, 'r', encoding='utf-8').read()

    # For demo: compare with existing files in uploads (excluding current file)
    similarities = []
    total_files = 0
    match_count = 0

    for filename in os.listdir('uploads'):
        filepath = os.path.join('uploads', filename)
        if filepath == uploaded_filepath:
            continue
        total_files += 1
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

            similarity = simple_similarity(uploaded_content, content)
            if similarity > 0:
                match_count += 1
                similarities.append({'file': filename, 'similarity': f'{similarity:.2f}%'})

    score = (match_count / total_files * 100) if total_files > 0 else 0

    return {
        'score': round(score, 2),
        'details': similarities
    }

def simple_similarity(text1, text2):
    # Tokenize by whitespace
    set1 = set(text1.split())
    set2 = set(text2.split())

    intersection = set1.intersection(set2)
    union = set1.union(set2)

    if not union:
        return 0

    similarity_percentage = (len(intersection) / len(union)) * 100
    return similarity_percentage
