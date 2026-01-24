# What this file will do
# Take raw text → return prediction + confidence + probabilities
# MAKE SURE TO REMOVE CONSOLES ONCE TESTED THE LOGS 


from typing import Dict,Tuple
from app.config import model,vectorizer,DEBUG
from app.text_utils import clean_text


def get_confidence_level(confidence: float) -> str:
    """
    Convert numeric confidence into human-readable level
    """
    if confidence >= 0.85:
        return "high"
    elif confidence >= 0.50:
        return "medium"
    else:
        return "low"

def get_top_k_predictions(probs:dict,k:int =3):
    sorted_probs = sorted(probs.items(), key=lambda x:x[1],reverse =True)
    return [
        {"category": cat, "confidence": float(conf)}
        for cat, conf in sorted_probs[:k]
    ]

# def predict_category(item:str)-> Tuple[str,float,str,Dict[str,float],Dict[str,float]]:
def predict_category(item: str) -> dict:
    """
    Predict expense category for a given item description.

    Returns:
        predicted_category (str)
        confidence (float)
        confidence_level (str)
        probabilities (dict[str, float])
        top_predictions (dict[str, float])
    """
    
    if not item or not item.strip():
        raise ValueError("Item description cannot be empty")
    
    # 1. Clean input text
    cleaned_item = clean_text(item)
    if DEBUG:
        print(cleaned_item)
    # 2. Vectorize Text
    item_vector = vectorizer.transform([cleaned_item])
    if DEBUG:
        print(item_vector)

    # 3. Get class probabilities
    probs = model.predict_proba(item_vector)[0]
    if DEBUG:
        print(probs)


    # 4. Map probabilities to class names
    class_labels = model.classes_
    probabilities = {
        label:float(prob)
        for label,prob in zip(class_labels,probs)
    }

    # 5. Pick best class
    predicted_index = probs.argmax()
    if DEBUG:
        print(predicted_index)
    predicted_category = class_labels[predicted_index]
    if DEBUG:
        print(predicted_category)
    confidence = float(probs[predicted_index])
    if DEBUG:
        print(confidence)
    confidence_level = get_confidence_level(confidence)
    top_predictions = get_top_k_predictions(probabilities, k=3)

    return {
        "predicted_category": predicted_category,
        "confidence": confidence,
        "confidence_level": confidence_level,
        "probabilities": probabilities,
        "top_predictions": top_predictions,
    }







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
