# AI Attendance Management System — Hugging Face edition

Terminal-only attendance manager for five students. Python remains responsible for attendance calculations and JSON updates; the Hugging Face model only converts natural-language requests into structured commands.

## Setup (Windows / VS Code)

1. Install Python 3.10 or newer.
2. Open this extracted folder in VS Code, then open Terminal → New Terminal.
3. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

4. Copy the example environment file and edit it:

```powershell
Copy-Item .env.example .env
code .env
```

Set your own Hugging Face token and model, for example:

```env
HF_TOKEN=hf_your_actual_token_here
HF_MODEL=Qwen/Qwen2.5-7B-Instruct-1M
```

The example model may not be served by a provider enabled for your account. If so, change `HF_MODEL` to a model currently shown as available for chat completion in the Hugging Face Inference Providers catalog. Listing a model on Hugging Face does not guarantee that a provider serves it for your account.

5. Test the API before starting the app:

```powershell
python test_huggingface.py
```

6. If the test succeeds, run the attendance app:

```powershell
python main.py
```

Type `help` to see example commands; type `exit` to quit.

## Example commands

- `Was Aarav Sharma present on 10 Oct 2026?`
- `Mark Priya Verma present on 9 Oct 2026`
- `Remove Rahul Kumar attendance on 11 Oct 2026`
- `What is Aarav Sharma's attendance percentage?`
- `Show all attendance percentages`
- `What is the class attendance average?`

## Important notes

- Your real `.env` is ignored by Git; never upload or share your API token.
- Hugging Face Inference Providers have account-level usage/credit limits. Using a token from another account uses that account's own access and allowance; changing models does not reset credits.
- Errors such as `model_not_supported` mean the configured model is not served by an enabled provider for that request. `insufficient credits` means the account's available inference allowance is insufficient.
- Attendance dates are configured for 8–14 October 2026. Python validates and updates the data in `json/students.json`; the AI does not directly edit the file.
