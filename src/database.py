# src/database.py
import chromadb
import uuid
from typing import Optional, List, Tuple
from .config import config

# Load database configuration
DB_PATH = config['database']['persist_directory']
COLLECTION_NAME = config['database']['collection_name']
RECOGNITION_THRESHOLD = config['recognition']['threshold']

class DatabaseManager:
    def __init__(self):
        # Initialize a persistent ChromaDB client
        self.client = chromadb.PersistentClient(path=DB_PATH)
        self.collection = self.client.get_or_create_collection(name=COLLECTION_NAME)
        print(f"DatabaseManager initialized. Collection: {COLLECTION_NAME}")

    def add_user(self, name: str, embeddings: List[list[float]], profile_image_path: str) -> str:
        """
        Adds a new user and their embeddings to the database.
        Corresponds to FR-2.4 [cite: 14]
        """
        user_id = str(uuid.uuid4())
        
        # We need to store multiple embeddings per user
        # We'll create unique IDs for each embedding, linked to the user_id in metadata
        embedding_ids = [f"{user_id}_{i}" for i in range(len(embeddings))]
        
        # Create metadata for each embedding
        # This matches the UserProfile model in the SRS [cite: 32]
        metadatas = [{
            "user_id": user_id,
            "name": name,
            "profile_image_path": profile_image_path,
            "registration_timestamp": "ISO_TIMESTAMP_HERE" # Add datetime logic
        } for _ in range(len(embeddings))]
        
        self.collection.add(
            embeddings=embeddings,
            metadatas=metadatas,
            ids=embedding_ids
        )
        print(f"Added user {name} with ID {user_id}")
        return user_id

    def search_user(self, query_embedding: list[float]) -> Optional[dict]:
        """
        Searches for the closest matching user to the given embedding.
        Corresponds to FR-1.3 [cite: 10] and Recognition Flow [cite: 43]
        """
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=1
            )
            
            if not results['ids'][0]:
                return None # No match found

            # Chroma returns 'distance', not 'similarity'. 
            # For cosine similarity (which InsightFace uses), distance = 1 - similarity
            # A lower distance is better.
            distance = results['distances'][0][0]
            similarity = 1 - distance
            
            # Use the confidence threshold from FR-1.3.5 [cite: 10] (e.g., 60%)
            # Your config.json has 0.6
            if similarity >= RECOGNITION_THRESHOLD:
                match_metadata = results['metadatas'][0][0]
                match_metadata['confidence'] = similarity
                return match_metadata
            else:
                return None # Match found but below confidence threshold

        except Exception as e:
            print(f"Error during user search: {e}")
            return None

# Singleton instance to be used by the API
db_manager = DatabaseManager()