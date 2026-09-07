# Audito: Automated Audio-Visual Media Plagiarism Framework

Audito is an automated media analysis framework designed to detect background audio track reuse and spoken script copyright violations prior to public media release.

## Features
* **Acoustic Fingerprinting:** Audio stream extraction and spectral landmark matching using Chromaprint.
* **Script Overlap Matching:** Offline speech-to-text transcription paired with Jaccard Similarity indexing.
* **Database & REST API:** Built with FastAPI, SQLAlchemy, and SQLite (`audito.db`).

## Project Structure
```text
audito-backend/
├── database.py       # Database connection setup
├── models.py         # SQLAlchemy ORM schemas
├── main.py           # Core database initialization script
└── README.md         # System documentation