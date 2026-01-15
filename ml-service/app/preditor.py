# What this file will do
# Take raw text → return prediction + confidence + probabilities
# MAKE SURE TO REMOVE CONSOLES ONCE TESTED THE LOGS 

from typing import Dict,Tuple
from config import model,vectorizer
from text_utils import clean_text


def predict_category(item:str)-> Tuple[str,float,Dict[str,float]]:
    """
    Predict expense category for a given item description.

    Returns:
        predicted_category (str)
        confidence (float)
        probabilities (dict[str, float])
    """
    # 1. Clean input text
    cleaned_item = clean_text(item)
    print(cleaned_item)
    # 2. Vectorize Text
    item_vector = vectorizer.transform([cleaned_item])
    print(item_vector)

    # 3. Get class probabilities
    probs = model.predict_proba(item_vector)[0]
    print(probs)


    # 4. Map probabilities to class names
    class_labels = model.classes_
    probabilities = {
        label:float(prob)
        for label,prob in zip(class_labels,probs)
    }

    # 5. Pick best class
    predicted_index = probs.argmax()
    print(predicted_index)
    predicted_category = class_labels[predicted_index]
    print(predicted_category)
    confidence = float(probs[predicted_index])
    print(confidence)

    return predicted_category,confidence,probabilities







# 3. Get class probabilities
    # probs = model.predict_proba(item_vector)[0]
    # print(probs)
    # predict_proba returns (number_of_samples, number_of_classes)

# In Our case it is 
# [
#     [0.05, 0.87, 0.08] 
# ]
# so [0] will give us [0.05, 0.87, 0.08]




 # 4. Map probabilities to class names
 # class_labels = model.classes_
 # probabilities = {
 #     label:float(prob)
 #     for label,prob in zip(class_labels,probs)
 # }

# probs = [0.05, 0.87, 0.08]
# class_labels = ["Entertainment", "Food", "Transport"]
# Then: zip(class_labels, probs) will do
# ("Entertainment", 0.05)
# ("Food", 0.87)
# ("Transport", 0.08)

# ABOVE probalilities is equivalen to
# probabilities = {}
# for label, prob in zip(class_labels, probs):
#     probabilities[label] = float(prob)
