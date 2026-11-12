import os
import logging
from datetime import datetime, timezone
from pymongo import MongoClient
from pymongo.errors import PyMongoError, ConnectionFailure
from bson import ObjectId

logger = logging.getLogger('website.mongo')

# Default MongoDB Atlas connection URI
DEFAULT_MONGO_URI = (
    "mongodb+srv://kuriankurian405_db_user:KpqwSMq9uHFXDAMA@cluster0.0yqlygw.mongodb.net/trinials_db?appName=Cluster0"
)

_client_cache = None


def get_mongo_uri():
    """Retrieve MongoDB URI from environment or fallback."""
    return os.environ.get('MONGO_URI', '').strip() or DEFAULT_MONGO_URI


def get_mongo_client():
    """Return a cached, thread-safe MongoClient instance."""
    global _client_cache
    if _client_cache is None:
        uri = get_mongo_uri()
        try:
            _client_cache = MongoClient(
                uri,
                serverSelectionTimeoutMS=4000,
                connectTimeoutMS=4000,
                socketTimeoutMS=5000,
                maxPoolSize=20,
            )
        except Exception as e:
            logger.error("Failed to initialize MongoClient: %s", e)
            return None
    return _client_cache


def get_mongo_db():
    """Return the database instance."""
    client = get_mongo_client()
    if client is None:
        return None
    try:
        # If database name is in the URI, get_default_database() uses it
        db = client.get_default_database()
        if db is not None:
            return db
    except Exception:
        pass
    return client['trinials_db']


def seed_email_config_to_mongo(override_config=None):
    """
    Seed or update the email configuration and credentials in MongoDB Atlas.
    Ensures credentials and notification lists exist in the cloud database.
    """
    db = get_mongo_db()
    if db is None:
        return False

    default_config = {
        '_id': 'email_config',
        'EMAIL_HOST': os.environ.get('EMAIL_HOST', 'smtp.gmail.com'),
        'EMAIL_PORT': int(os.environ.get('EMAIL_PORT', 465)),
        'EMAIL_USE_SSL': os.environ.get('EMAIL_USE_SSL', 'True').lower() in ('true', '1', 'yes'),
        'EMAIL_USE_TLS': os.environ.get('EMAIL_USE_TLS', 'False').lower() in ('true', '1', 'yes'),
        'EMAIL_HOST_USER': os.environ.get('EMAIL_HOST_USER') or os.environ.get('GMAIL_EMAIL') or 'dummy11248@gmail.com',
        'EMAIL_HOST_PASSWORD': os.environ.get('EMAIL_HOST_PASSWORD') or os.environ.get('GMAIL_APP_PASSWORD') or 'sxtu ldyf aayl yyvb',
        'DEFAULT_FROM_EMAIL': os.environ.get('DEFAULT_FROM_EMAIL', 'Trinials <dummy11248@gmail.com>'),
        'CONTACT_NOTIFICATION_EMAIL': os.environ.get(
            'CONTACT_NOTIFICATION_EMAIL',
            'johnpaulalex85@gmail.com, trinial26@gmail.com, Jojogeorge.trinials@gmail.com, joejoseph1235@gmail.com'
        ),
        'CONTACT_EMAIL': os.environ.get('CONTACT_EMAIL', 'trinial26@gmail.com'),
        'CONTACT_PHONE_NUMBER': os.environ.get('CONTACT_PHONE_NUMBER', '+91 85908 21155'),
        'CONTACT_PHONE_NUMBER_SECONDARY': os.environ.get('CONTACT_PHONE_NUMBER_SECONDARY', '+91 94003 25570'),
        'updated_at': datetime.now(timezone.utc)
    }

    if override_config and isinstance(override_config, dict):
        default_config.update(override_config)

    try:
        db.app_config.replace_one({'_id': 'email_config'}, default_config, upsert=True)
        logger.info("Successfully synced email_config into MongoDB Atlas app_config collection.")
        return True
    except Exception as e:
        logger.error("Failed to seed email_config to MongoDB Atlas: %s", e)
        return False


def get_email_config_from_mongo():
    """
    Fetch email credentials and notification list from MongoDB Atlas.
    Returns dictionary with email settings or None if unavailable.
    """
    try:
        db = get_mongo_db()
        if db is None:
            return None
        doc = db.app_config.find_one({'_id': 'email_config'})
        if doc:
            return doc
    except Exception as e:
        logger.warning("Could not fetch email_config from MongoDB Atlas: %s", e)
    return None


def save_enquiry_to_mongo(enquiry_data):
    """
    Insert a contact enquiry into the MongoDB Atlas 'enquiries' collection.
    Returns the string ID of the inserted document, or None if failed.
    """
    db = get_mongo_db()
    if db is None:
        return None

    doc = {
        'name': str(enquiry_data.get('name', '')).strip(),
        'email': str(enquiry_data.get('email', '')).strip(),
        'phone': str(enquiry_data.get('phone', '')).strip(),
        'subject': str(enquiry_data.get('subject', '')).strip(),
        'message': str(enquiry_data.get('message', '')).strip(),
        'ip_address': enquiry_data.get('ip_address'),
        'user_agent': enquiry_data.get('user_agent'),
        'status': 'new',
        'is_read': False,
        'created_at': datetime.now(timezone.utc),
        'email_dispatch': {
            'team_dispatched': False,
            'client_dispatched': False,
            'timestamp': None,
            'errors': []
        }
    }

    try:
        result = db.enquiries.insert_one(doc)
        mongo_id = str(result.inserted_id)
        logger.info("Saved enquiry to MongoDB Atlas (id=%s) for %s", mongo_id, doc['email'])
        return mongo_id
    except Exception as e:
        logger.error("Failed to save enquiry to MongoDB Atlas: %s", e)
        return None


def log_email_dispatch_status_to_mongo(mongo_id, team_dispatched=False, client_dispatched=False, errors=None):
    """
    Update an enquiry document in MongoDB Atlas with the email dispatch result.
    """
    if not mongo_id:
        return False

    db = get_mongo_db()
    if db is None:
        return False

    update_payload = {
        'email_dispatch.team_dispatched': bool(team_dispatched),
        'email_dispatch.client_dispatched': bool(client_dispatched),
        'email_dispatch.timestamp': datetime.now(timezone.utc),
    }

    if errors:
        update_payload['email_dispatch.errors'] = errors if isinstance(errors, list) else [str(errors)]

    try:
        oid = ObjectId(mongo_id) if ObjectId.is_valid(mongo_id) else mongo_id
        db.enquiries.update_one({'_id': oid}, {'$set': update_payload})
        return True
    except Exception as e:
        logger.warning("Could not update email dispatch status in MongoDB Atlas for %s: %s", mongo_id, e)
        return False


def list_recent_enquiries(limit=50):
    """Fetch recent enquiries from MongoDB Atlas."""
    db = get_mongo_db()
    if db is None:
        return []
    try:
        cursor = db.enquiries.find().sort('created_at', -1).limit(limit)
        results = []
        for doc in cursor:
            doc['id'] = str(doc.get('_id'))
            results.append(doc)
        return results
    except Exception as e:
        logger.error("Could not fetch enquiries from MongoDB Atlas: %s", e)
        return []
