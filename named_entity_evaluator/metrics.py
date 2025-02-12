from difflib import SequenceMatcher
import pandas as pd

def is_partial_match(value1, value2, threshold=0.5):
    """
    Determines if two strings are partially similar based on the given threshold.
    
    Args:
        value1 (str): First string.
        value2 (str): Second string.
        threshold (float): Similarity threshold (default: 0.5).
    
    Returns:
        bool: True if similarity ratio is above the threshold, False otherwise.
    """
    return SequenceMatcher(None, str(value1), str(value2)).ratio() >= threshold

def compare_json_arrays_with_partials(ground_truth, predictions, partial_threshold=0.5):
    """
    Compares ground truth and predicted named entities, classifying matches into categories.
    
    Args:
        ground_truth (list of dict): Actual entity annotations.
        predictions (list of dict): Predicted entity annotations.
        partial_threshold (float): Threshold for partial matches.
    
    Returns:
        dict: Counts of COR (Correct), INC (Incorrect), PAR (Partial), MIS (Missing), SPU (Spurious).
    """
    cor, inc, par, mis, spu = 0, 0, 0, 0, 0
    
    for gt_obj, pred_obj in zip(ground_truth, predictions):
        gt_dict, pred_dict = gt_obj.copy(), pred_obj.copy()
        common_keys = set(gt_dict.keys()) & set(pred_dict.keys())

        for key in common_keys:
            if gt_dict[key] == pred_dict[key]:
                cor += 1
            elif is_partial_match(gt_dict[key], pred_dict[key], partial_threshold):
                par += 1
            else:
                inc += 1

        mis += len(set(gt_dict.keys()) - common_keys)
        spu += len(set(pred_dict.keys()) - common_keys)
    
    return {"COR": cor, "INC": inc, "PAR": par, "MIS": mis, "SPU": spu}

def calculate_metrics(metrics, partials_multiplier=0.7):
    """
    Compute precision, recall, and F1 score based on named entity prediction evaluation.

    Args:
        metrics (dict): A dictionary with keys: COR, INC, PAR, MIS, SPU.
        partials_multiplier (int): The multiplier which the partial matches are going to be multiplied with (MUST less than 1)

    Returns:
        pandas.DataFrame: A DataFrame containing Precision, Recall, and F1 Score.
    """
    
    TP = metrics["COR"] + (partials_multiplier * metrics["PAR"])
    ACT = metrics["COR"] + metrics["INC"] + metrics["SPU"] + metrics["PAR"]
    POS = metrics["COR"] + metrics["INC"] + metrics["MIS"] + metrics["PAR"]
    
    precision = TP / ACT if ACT else 0
    recall = TP / POS if POS else 0
    f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) else 0

    metrics_dict = {
        'Metric': ['Precision', 'Recall', 'F1 Score'],
        'Value (%)': [precision * 100, recall * 100, f1_score * 100]
    }
    return pd.DataFrame(metrics_dict)
