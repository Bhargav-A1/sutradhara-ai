import json
import os
import re
from llama_cpp import Llama

# Calculate the exact Windows User path dynamically
username = os.getlogin()
base_downloads_path = f"C:/Users/{username}/Downloads/"

print(f" System: Checking your Windows user profile Downloads directory...")

# Check for standard name or the hidden .txt extension variation
target_file_normal = os.path.join(base_downloads_path, "qwen2.5-1.5b-instruct-q4_k_m.gguf")
target_file_hidden_ext = os.path.join(base_downloads_path, "qwen2.5-1.5b-instruct-q4_k_m.gguf.txt")

if os.path.exists(target_file_normal):
    model_path = target_file_normal
elif os.path.exists(target_file_hidden_ext):
    model_path = target_file_hidden_ext
else:
    raise FileNotFoundError("Model file missing from physical Downloads folder container path.")

print(f" Target Found! Loading: {model_path}")
print(" Initializing Qwen 1.5B Engine directly into system RAM...")

# Initialize the model structure straight into system RAM
llm = Llama(
    model_path=model_path,
    n_ctx=2048,   # Context window size 
    n_threads=4,  # Utilizes 4 CPU cores for processing
    verbose=False
)
print(" AI Core successfully loaded and listening.")

# 2. Pipeline processing engine (Phase 3)
def analyze_kyc_profile(clean_demographics_text):
    print(" AI is processing the anonymized demographic payload...")
    
    prompt = (
        "<|im_start|>system\n"
        "You are a strict financial compliance parser. Analyze the profile inputs and return "
        "a raw JSON object containing identity_confirmed (bool), profile_classification (string), "
        "and identified_risk_count (int). Do not write any conversational text, introductory sentences, or markdown wrappers.\n"
        "<|im_end|>\n"
        f"<|im_start|>user\nAnalyze this data: {clean_demographics_text}\n<|im_end|>\n"
        "<|im_start|>assistant\n"
    )
    
    output = llm(
        prompt,
        max_tokens=256,
        temperature=0.1
    )
    
    raw_text = output["choices"][0]["text"].strip()
    print(f" Raw Generation: {repr(raw_text)}")
    
    #  Extract ONLY the valid JSON block between the outer curly braces
    print("Cleaning output text structural formatting via regex extractor...")
    match = re.search(r"(\{.*?\})", raw_text, re.DOTALL)
    
    if match:
        cleaned_text = match.group(1).strip()
    else:
        # Fallback if no braces were found at all
        cleaned_text = raw_text
        
    print(f" Cleaned String: {repr(cleaned_text)}")
    return json.loads(cleaned_text)

# 3. Decision metric formulation formula (Phase 4)
def compute_stability_score(analysis_results):
    print(" Computing Expat Stability Score...")
    score = 60  
    
    is_confirmed = str(analysis_results.get("identity_confirmed")).lower() == "true"
    if is_confirmed:
        score += 20
        
    classification = str(analysis_results.get("profile_classification", "")).strip().title()
    if classification in ["Professional", "Student"]:
        score += 20
        
    try:
        risk_count = int(analysis_results.get("identified_risk_count", 0))
    except (ValueError, TypeError):
        risk_count = 0
        
    score -= (risk_count * 15)
    return max(0, min(100, score))

# --- Active Execution Block ---
if __name__ == "__main__":
    mock_input = "{ 'jurisdiction': 'IN', 'age': '27', 'status': 'Verified Student No Flags' }"
    
    extracted_metrics = analyze_kyc_profile(mock_input)
    final_output_score = compute_stability_score(extracted_metrics)
    
    print("\n --- SUTRADHARA AI ANALYSIS COMPLETE ---")
    print(f" Extracted Metrics Struct: {json.dumps(extracted_metrics, indent=2)}")
    print(f" Computed Expat Stability Score: {final_output_score}/100")
