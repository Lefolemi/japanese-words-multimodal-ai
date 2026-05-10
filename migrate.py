import pandas as pd
from app import create_app, db
from app.models.vocabulary import Vocabulary
import os

def migrate_data():
    app = create_app()
    # Let's use the path that worked for you previously
    csv_path = os.path.join('data', 'jlpt_vocab.csv') 
    
    with app.app_context():
        print("--- Resetting Database ---")
        db.drop_all()
        db.create_all()
        
        print(f"Reading {csv_path}...")
        try:
            # utf-8-sig handles the 'charmap' error and BOM often found in Japanese CSVs
            # sep=None + engine='python' lets pandas guess if it's a comma or pipe
            df = pd.read_csv(csv_path, sep=None, engine='python', encoding='utf-8-sig')
            
            # Clean column names in case there are hidden spaces
            df.columns = [c.strip() for c in df.columns]
            
            words_to_insert = []
            for _, row in df.iterrows():
                # Using your proven logic: strip 'N' and 'JLPT'
                raw_level = str(row['JLPT Level']).upper().replace('N', '').replace('JLPT', '').strip()
                
                try:
                    level = int(raw_level)
                except ValueError:
                    level = 5 # Fallback
                
                word = Vocabulary(
                    original=str(row['Original']).strip(),
                    furigana=str(row['Furigana']).strip(),
                    english=str(row['English']).strip(),
                    jlpt_level=level
                )
                words_to_insert.append(word)

            if not words_to_insert:
                print("⚠️ No words found to insert. Check your CSV headers.")
                return

            print(f"Migrating {len(words_to_insert)} words...")
            db.session.bulk_save_objects(words_to_insert)
            db.session.commit()
            print("✅ Migration Complete! Everything is in the DB.")
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            db.session.rollback()

if __name__ == '__main__':
    migrate_data()