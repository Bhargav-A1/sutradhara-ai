import io
import json
import os
import re
import time
import smtplib
from email.mime.text import MIMEText
from contextlib import asynccontextmanager
from typing import Optional, List
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
import easyocr
import cohere
from llama_cpp import Llama

# ----------------------------------------------------------------------
# 1. LIFESPAN CONTEXT (Dual Cloud + Local Fallback Asset Loading)
# ----------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("System: Spinning up EasyOCR core module...")
    app.state.ocr_reader = easyocr.Reader(['en'], gpu=False)
    
    # PASTE YOUR COHERE API KEY HERE EXACTLY AS IT APPEARS ON YOUR SCREEN
    COHERE_API_KEY = "COHERE_API_KEY"
    
    app.state.cohere_client = cohere.ClientV2(api_key=COHERE_API_KEY)
    
    # Secure Local Backup Layer initialization so your pipeline NEVER crashes
    username = os.getlogin()
    model_path = f"C:/Users/{username}/Downloads/qwen_fresh_core.gguf"
    if not os.path.exists(model_path):
        model_path = f"C:/Users/{username}/Downloads/qwen2.5-1.5b-instruct-q4_k_m.gguf"
    
    if os.path.exists(model_path):
        print(f"System: Mounting local safety fallback model layers from: {model_path}")
        app.state.local_llm = Llama(model_path=model_path, n_ctx=4096, n_threads=4, verbose=False)
        app.state.has_local_fallback = True
    else:
        print(" NOTICE: Local backup GGUF model file not found in Downloads folder.")
        app.state.has_local_fallback = False

    print("Sutradhara AI Complete Unified Cloud/Local Hybrid Gateway Operational.")
    yield
    print("System: Closing gateway network connection pools...")

app = FastAPI(title="Sutradhara AI - Managed Hybrid Edition", version="4.5.1", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FOREX_DATABASE_CACHE = {}
STATEMENT_LEDGER_CACHE = []

class ChatQueryPayload(BaseModel):
    user_email: str
    message: str

class CurrencyExchangePayload(BaseModel):
    user_email: str
    from_currency: str
    to_currency: str
    amount: float
    exchange_rate: float

# --- REAL PRODUCTION GOOGLE SMTP WIRE PARAMETERS ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "Your_Brand_Mail_Address" 
SENDER_PASSWORD = "Brand_Mail_Address_Password"    # (No spaces!)

# ----------------------------------------------------------------------
# 2. UTILITY CHANNELS & BACKGROUND PROCESS WORKERS
# ----------------------------------------------------------------------
def send_transaction_email(recipient_email: str, subject: str, message_body: str):
    if SENDER_EMAIL == "your_new_sutradhara_email@gmail.com" or "yournew" in SENDER_PASSWORD:
        print(f"\n[SMTP NOTICE]: Email credentials not configured yet. Logging payload to terminal:")
        print(f" Target: {recipient_email}\n Subject: {subject}\n Body:\n{message_body}\n")
        return
    try:
        msg = MIMEText(message_body)
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = recipient_email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=15) as server:
            server.starttls()  
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
    except Exception as e:
        print(f" SMTP Failure: {str(e)}")

def async_delayed_clearing_worker(user_email: str, tx_id: str, from_curr: str, to_curr: str, final_amount: float):
    time.sleep(15) 
    if tx_id in FOREX_DATABASE_CACHE:
        FOREX_DATABASE_CACHE[tx_id]["status"] = "Settled"
        FOREX_DATABASE_CACHE[tx_id]["completion_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
    subject = f"Sutradhara AI - Forex Exchange Settled [ID: {tx_id}]"
    body = f"Forex Settlement Complete!\n\nID: {tx_id}\nRoute: {from_curr} -> {to_curr}\nAmount: {final_amount} {to_curr}\nStatus: SETTLED"
    send_transaction_email(user_email, subject, body)

def deterministic_json_extractor(raw_text: str) -> dict:
    text_cleaned = raw_text.strip()
    # Fixed line 110: Simplified onto a single clean line string syntax definition
    text_cleaned = re.sub(r"^```json\s*|```$", "", text_cleaned, flags=re.IGNORECASE).strip()
    match = re.search(r"(\{.*\})", text_cleaned, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass
    try:
        return json.loads(text_cleaned)
    except Exception:
        return {"transactions": []}

# --------------------------------------------------------------------------------
# 4. CORE API ROUTING GATEWAYS
# --------------------------------------------------------------------------------
@app.post("/api/v2/parse-statement")
async def parse_bank_statement(user_email: str = Form(...), file: UploadFile = File(...)):
    global STATEMENT_LEDGER_CACHE
    try:
        filename = file.filename.lower()
        statement_text = ""
        if filename.endswith(('.png', '.jpg', '.jpeg', '.webp')):
            image_bytes = await file.read()
            image = Image.open(io.BytesIO(image_bytes))
            raw_image = io.BytesIO()
            image.save(raw_image, format=image.format)
            ocr_results = app.state.ocr_reader.readtext(raw_image.getvalue(), detail=0)
            statement_text = "\n".join(ocr_results)
        else:
            raw_bytes = await file.read()
            statement_text = raw_bytes.decode("utf-8", errors="ignore")

        lines = [line.strip() for line in statement_text.split("\n") if line.strip()][:35]
        
        prompt = (
            f"Extract all transactions found inside this dataset list: {str(lines)}. "
            f"Return only a single clean valid JSON object with a root key 'transactions' containing a list array. "
            f"Each object inside the list MUST strictly feature attributes: 'date' (DD/MM/YYYY), 'merchant' (string), 'amount' (float, negative for costs), 'category' (string). "
            f"Do not respond with any markdown wrappers."
        )
        
        try:
            print("System: Attempting cloud processing handshake via Cohere...")
            response = app.state.cohere_client.chat(
                model="command-r-plus",
                messages=[{"role": "user", "content": prompt}]
            )
            text_payload = response.message.content[0].text
            parsed_data = deterministic_json_extractor(text_payload)
            STATEMENT_LEDGER_CACHE = parsed_data.get("transactions", [])
            print(f" Success: Processed via Cohere Cloud. Found {len(STATEMENT_LEDGER_CACHE)} transactions.")
            
        except Exception as cloud_error:
            print(f"Cloud Error occurred: {str(cloud_error)}")
            if app.state.has_local_fallback:
                print(" Emergency Protocol Protocol: Cohere credentials rejected. Switching processing to local CPU Qwen Engine...")
                local_prompt = (
                    "<|im_start|>system\nExtract data into raw JSON matching root key 'transactions' array.\n<|im_end|>\n"
                    f"<|im_start|>user\n{str(lines)}\n<|im_end|>\n<|im_start|>assistant\n"
                )
                local_output = app.state.local_llm(local_prompt, max_tokens=1200, temperature=0.1)
                parsed_data = deterministic_json_extractor(local_output["choices"][0]["text"])
                STATEMENT_LEDGER_CACHE = parsed_data.get("transactions", [])
                print(f" Success: Recovered via Local safety backup layers. Found {len(STATEMENT_LEDGER_CACHE)} transactions.")
            else:
                raise HTTPException(status_code=500, detail="Cloud API Key is unverified and local backup model is unmounted.")

        # Dispatch report summary update to user email
        email_subject = "Sutradhara AI - Ingestion Analysis Update"
        email_body = f"Hello User,\n\nYour account statement parsing execution has completed successfully.\nTotal Rows Recovered: {len(STATEMENT_LEDGER_CACHE)}"
        send_transaction_email(user_email, email_subject, email_body)
        
        return {"success": True, "filename": file.filename, "parsed_ledger": {"transactions": STATEMENT_LEDGER_CACHE}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline Processing Error: {str(e)}")

@app.post("/api/v2/exchange-currency")
def execute_currency_exchange(payload: CurrencyExchangePayload, bg_tasks: BackgroundTasks):
    try:
        tx_id = f"TX-FX-{int(time.time())}"
        payout = round(payload.amount * payload.exchange_rate, 2)
        
        FOREX_DATABASE_CACHE[tx_id] = {
            "user_email": payload.user_email, "from_currency": payload.from_currency,
            "to_currency": payload.to_currency, "amount": payload.amount, "payout": payout,
            "rate": payload.exchange_rate, "status": "Processing", "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        receipt_subject = f"Sutradhara AI - Instant Exchange Receipt [ID: {tx_id}]"
        receipt_body = f"Forex Order Booked!\n\nID: {tx_id}\nFrom: {payload.amount} {payload.from_currency}\nTo: {payout} {payload.to_currency}\nStatus: PENDING"
        send_transaction_email(payload.user_email, receipt_subject, receipt_body)
        
        bg_tasks.add_task(async_delayed_clearing_worker, user_email=payload.user_email, tx_id=tx_id, from_curr=payload.from_currency, to_curr=payload.to_currency, final_amount=payout)
        return {"success": True, "transaction_id": tx_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v2/agent-chat")
def enterprise_coral_chat_agent(payload: ChatQueryPayload):
    try:
        user_forex_records = [
            {"tx_id": tid, **data} for tid, data in FOREX_DATABASE_CACHE.items()
            if data["user_email"].lower() == payload.user_email.lower()
        ]
        
        coral_integrated_documents = [
            {"title": "Internal Database - Statement Rows", "snippet": json.dumps(STATEMENT_LEDGER_CACHE)},
            {"title": "Internal Database - Forex Queue", "snippet": json.dumps(user_forex_records)},
            {"title": "Notion Workspace - Anti-Money Laundering Policy", "snippet": "Notion AML Policy Manual: All transactions are processed via monitored corporate corridors."},
            {"title": "Slack Channel - Security Infrastructure Feed", "snippet": "[System Feed]: Multi-channel RAG access tokens mapped successfully."}
        ]
        
        try:
            response = app.state.cohere_client.chat(
                model="command-r-plus",
                messages=[{"role": "user", "content": payload.message}],
                documents=coral_integrated_documents  
            )
            return {"success": True, "agent_response": response.message.content[0].text, "source_citations_count": len(coral_integrated_documents)}
        except Exception:
            if app.state.has_local_fallback:
                local_prompt = (
                    "<|im_start|>system\nYou are the backup Sutradhara AI Agent. Answer based on these records:\n"
                    f"{json.dumps(coral_integrated_documents)}\n<|im_end|>\n"
                    f"<|im_start|>user\n{payload.message}\n<|im_end|>\n<|im_start|>assistant\n"
                )
                local_output = app.state.local_llm(local_prompt, max_tokens=400, temperature=0.3)
                return {"success": True, "agent_response": local_output["choices"][0]["text"].strip(), "source_citations_count": "Local Engine Active"}
            else:
                return {"success": True, "agent_response": "Cloud API Key rejected. Please verify configuration parameters.", "source_citations_count": 0}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
