import torch
from transformers import pipeline, BertConfig, BertModel

def Bert_for_zero_shot_classification():
    """   
    Returns a pipeline function set up with HuggingFaces's zero-shot-classification 
    and Facebook's Bart Large MNLI model. It automatically chooses the best 
    device to run the model on.
    """
    device = 0 if torch.cuda.is_available() else "cpu"
    pipe = pipeline("zero-shot-classification",
        model = "facebook/bart-large-mnli",
        device = device)
    return pipe

def pipe(pipeline,
         label:str, 
         text:str):
    """
    pipeline: transformers.pipelines.zero_shot_classification.ZeroShotClassificationPipeline
    label: str
    text: str
    
    return: float
    
    It takes a label and text and returns a floating point that corresponds to the 
    score of how much that job description fits the specified label compared to how 
    much it fits the label puppies.
    
    score = how much of the label / how much of puppies"""
    result = pipeline(text, candidate_labels = [label, "puppies"])
    if result["labels"][0] == label:
        score = result["scores"][0]/result["scores"][1]
    else:
        score = result["scores"][1]/result["scores"][0]
    return score