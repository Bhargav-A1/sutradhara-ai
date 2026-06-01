import json
import os
import re
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llama_cpp import Llama

# 1. Define the Lifespan Context to control single-instance asset allocation
@asynccontextmanager
async def lifespan(app: FastAPI):
    username = os.getlogin()
    # Forces the engine to strictly use the new file from the Invoke-WebRequest download
    model_path = f"C:/Users/{username}/Downloads/qwen_fresh_core.gguf"

    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"❌ CRITICAL ERROR: The uncorrupted file was not found at: {model_path}\n"
            f"Please run the Invoke-WebRequest download command completely first."
        )

    # Confirm the size of the fresh file
    file_size_mb = os.path.getsize(model_path) / (1024 * 1024)
    print(f"System: Confirmed fresh model file size is {file_size_mb:.2f} MB")

    print("System: Loading Qwen 1.5B engine layers with safe memory profiling...")
    
    # Optimized memory constraints for stable CPU-only local execution
    app.state.llm = Llama(
        model_path=model_path,
        n_ctx=512,        # Low context ceiling clears room in standard system RAM
        n_batch=128,      # Processes prompt sequences in small chunks
        n_threads=2,      # Utilizes 2 CPU cores to prevent thread thrashing
        f16_kv=True,      # Quantizes cache matrices
        logits_all=False, 
        verbose=False
    )
    print("AI Core successfully loaded and listening.")
    
    yield
    print("System: Shutting down core micro-service modules...")


# 2. Framework Initialization
app = FastAPI(
    title="Sutradhara AI - Analytics and Integration Micro-Service",
    version="1.0.0",
    lifespan=lifespan
)

class UserDataPayload(BaseModel):
    demographics_blob: str

# 3. Core Engine Pipeline Logic
def process_compliance_data(llm_instance: Llama, raw_input_text: str) -> dict:
    prompt = (
        "<|im_start|>system\n"
        "You are a strict financial compliance parser. Analyze the profile inputs and return "
        "a raw JSON object containing identity_confirmed (bool), profile_classification (string), "
        "and identified_risk_count (int). Do not write any conversational text, introductory sentences, or markdown wrappers.\n"
        "<|im_end|>\n"
        f"<|im_start|>user\nAnalyze this data: {raw_input_text}\n<|im_end|>\n"
        "<|im_start|>assistant\n"
    )
    
    output = llm_instance(
        prompt,
        max_tokens=256,
        temperature=0.1
    )
    
    raw_text = output["choices"][0]["text"].strip()
    
    # Regex extract to clean up potential local model markdown wrapper artifacts
    match = re.search(r"(\{.*?\})", raw_text, re.DOTALL)
    if match:
        cleaned_text = match.group(1).strip()
    else:
        cleaned_text = raw_text
        
    return json.loads(cleaned_text)

def calculate_stability_index(metrics: dict) -> int:
    score = 60  
    
    is_confirmed = str(metrics.get("identity_confirmed")).lower() == "true"
    if is_confirmed:
        score += 20
        
    classification = str(metrics.get("profile_classification", "")).strip().title()
    if classification in ["Professional", "Student"]:
        score += 20
        
    try:
        risk_count = int(metrics.get("identified_risk_count", 0))
    except (ValueError, TypeError):
        risk_count = 0
        
    score -= (risk_count * 15)
    return max(0, min(100, score))


# 4. API Endpoints
@app.get("/health")
def health_check():
    return {"status": "healthy", "engine": "Qwen-1.5B-Instruct"}

@app.post("/api/v1/analyze-stability")
def analyze_stability_endpoint(payload: UserDataPayload):
    try:
        active_llm = app.state.llm
        parsed_metrics = process_compliance_data(active_llm, payload.demographics_blob)
        stability_score = calculate_stability_index(parsed_metrics)
        
        return {
            "success": True,
            "metrics": parsed_metrics,
            "calculated_expat_stability_score": stability_score
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal pipeline processing failure: {str(e)}"
        )
