import acoustid
import os
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Track, AcousticFingerprint

def extract_and_fingerprint(file_path: str):
    """
    Parses media files via FFmpeg and generates Chromaprint acoustic fingerprints.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Media file not found at: {file_path}")

    # Acoustid uses the fpcalc binary on system PATH to extract duration & fingerprint
    duration, fingerprint_encoded = acoustid.fingerprint_file(file_path)
    
    fingerprint_str = fingerprint_encoded.decode("utf-8") if isinstance(fingerprint_encoded, bytes) else fingerprint_encoded
    return duration, fingerprint_str

def index_track(title: str, file_path: str):
    """
    Indexes a new reference track and its fingerprint into SQLite.
    """
    db: Session = SessionLocal()
    try:
        duration, fp_string = extract_and_fingerprint(file_path)
        
        track = Track(title=title, file_path=file_path)
        db.add(track)
        db.commit()
        db.refresh(track)

        fingerprint = AcousticFingerprint(
            track_id=track.id,
            fingerprint_raw=fp_string,
            duration=int(duration)
        )
        db.add(fingerprint)
        db.commit()
        
        print(f"Successfully indexed: '{title}' (ID: {track.id}, Duration: {int(duration)}s)")
        return track
    except Exception as e:
        db.rollback()
        print(f"Indexing failed: {e}")
    finally:
        db.close()

def match_audio(query_file_path: str):
    """
    Compares a target sample against indexed fingerprints in the database.
    """
    db: Session = SessionLocal()
    try:
        _, query_fp = extract_and_fingerprint(query_file_path)
        indexed_fps = db.query(AcousticFingerprint).all()
        matches = []

        for item in indexed_fps:
            track = db.query(Track).filter(Track.id == item.track_id).first()
            
            if item.fingerprint_raw == query_fp:
                score = 100.0
            else:
                min_len = min(len(item.fingerprint_raw), len(query_fp))
                common = sum(1 for a, b in zip(item.fingerprint_raw, query_fp) if a == b)
                score = round((common / min_len) * 100, 2) if min_len > 0 else 0.0

            if score > 50.0:
                matches.append({
                    "track_id": track.id,
                    "title": track.title,
                    "match_score": score,
                    "duration": item.duration
                })

        return matches
    finally:
        db.close()