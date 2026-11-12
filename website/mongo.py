import os
import logging
from datetime import datetime, timezone
from pymongo import MongoClient
from pymongo.errors import PyMongoError, ConnectionFailure
from bson import ObjectId

logger = logging.getLogger('website.mongo')

# Default MongoDB Atlas connection URI
DEFAULT_MONGO_URI = (
    "mongodb+srv://trinial26_db_user:STTJWsGMEB1tn1vL@cluster0.unsmrqc.mongodb.net/trinials_db?retryWrites=true&w=majority&appName=Cluster0"
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
        'BREVO_API_KEY': os.environ.get('BREVO_API_KEY', '').strip(),
        'RESEND_API_KEY': os.environ.get('RESEND_API_KEY', '').strip(),
        'GMAIL_WEBHOOK_URL': os.environ.get('GMAIL_WEBHOOK_URL', '').strip(),
        'GMAIL_WEBHOOK_SECRET': os.environ.get('GMAIL_WEBHOOK_SECRET', '').strip(),
        'updated_at': datetime.now(timezone.utc)
    }

    if override_config and isinstance(override_config, dict):
        default_config.update(override_config)

    try:
        # Preserve existing API keys if already populated in Mongo
        existing = db.app_config.find_one({'_id': 'email_config'}) or {}
        for key in ['BREVO_API_KEY', 'RESEND_API_KEY', 'GMAIL_WEBHOOK_URL', 'GMAIL_WEBHOOK_SECRET']:
            if existing.get(key) and not default_config.get(key):
                default_config[key] = existing[key]

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


def get_enquiry_by_id(enquiry_id):
    """Fetch a single enquiry by its MongoDB ObjectId or string representation."""
    db = get_mongo_db()
    if db is None or not enquiry_id:
        return None
    try:
        oid = ObjectId(enquiry_id) if ObjectId.is_valid(enquiry_id) else enquiry_id
        doc = db.enquiries.find_one({'_id': oid})
        if doc:
            doc['id'] = str(doc.get('_id'))
        return doc
    except Exception as e:
        logger.error("Error retrieving enquiry %s from MongoDB: %s", enquiry_id, e)
        return None


def update_enquiry_status(enquiry_id, status=None, is_read=None):
    """Update status or read state of an enquiry."""
    db = get_mongo_db()
    if db is None or not enquiry_id:
        return False
    try:
        oid = ObjectId(enquiry_id) if ObjectId.is_valid(enquiry_id) else enquiry_id
        update_fields = {}
        if status is not None:
            update_fields['status'] = str(status).strip().lower()
        if is_read is not None:
            update_fields['is_read'] = bool(is_read)
        if update_fields:
            update_fields['updated_at'] = datetime.now(timezone.utc)
            db.enquiries.update_one({'_id': oid}, {'$set': update_fields})
            return True
        return False
    except Exception as e:
        logger.error("Error updating enquiry %s in MongoDB: %s", enquiry_id, e)
        return False


def delete_enquiry(enquiry_id):
    """Delete an enquiry permanently from MongoDB Atlas."""
    db = get_mongo_db()
    if db is None or not enquiry_id:
        return False
    try:
        oid = ObjectId(enquiry_id) if ObjectId.is_valid(enquiry_id) else enquiry_id
        result = db.enquiries.delete_one({'_id': oid})
        return result.deleted_count > 0
    except Exception as e:
        logger.error("Error deleting enquiry %s from MongoDB: %s", enquiry_id, e)
        return False


def get_enquiry_stats():
    """Compute dashboard analytics and metrics across all enquiries."""
    db = get_mongo_db()
    stats = {
        'total': 0,
        'today': 0,
        'unread': 0,
        'new': 0,
        'contacted': 0,
        'in_progress': 0,
        'closed': 0,
        'team_dispatched': 0,
        'client_dispatched': 0,
    }
    if db is None:
        return stats
    try:
        now = datetime.now(timezone.utc)
        today_start = datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=timezone.utc)
        today_end = datetime(now.year, now.month, now.day, 23, 59, 59, 999999, tzinfo=timezone.utc)

        stats['total'] = db.enquiries.count_documents({})
        stats['today'] = db.enquiries.count_documents({'created_at': {'$gte': today_start, '$lte': today_end}})
        stats['unread'] = db.enquiries.count_documents({'is_read': False})
        stats['new'] = db.enquiries.count_documents({'status': 'new'})
        stats['contacted'] = db.enquiries.count_documents({'status': 'contacted'})
        stats['in_progress'] = db.enquiries.count_documents({'status': 'in_progress'})
        stats['closed'] = db.enquiries.count_documents({'status': 'closed'})
        stats['team_dispatched'] = db.enquiries.count_documents({'email_dispatch.team_dispatched': True})
        stats['client_dispatched'] = db.enquiries.count_documents({'email_dispatch.client_dispatched': True})
    except Exception as e:
        logger.error("Error computing enquiry stats: %s", e)
    return stats


def search_enquiries(query="", status_filter="", date_from=None, date_to=None, limit=100, skip=0):
    """
    Search and filter enquiries with pagination, calendar date range, and substring query.
    Supports substring match on name, email, phone, and subject.
    """
    db = get_mongo_db()
    if db is None:
        return [], 0
    try:
        filter_criteria = {}
        if status_filter:
            s_clean = status_filter.strip().lower()
            if s_clean == 'unread':
                filter_criteria['is_read'] = False
            elif s_clean != 'all':
                filter_criteria['status'] = s_clean

        if query:
            q_clean = query.strip()
            filter_criteria['$or'] = [
                {'name': {'$regex': q_clean, '$options': 'i'}},
                {'email': {'$regex': q_clean, '$options': 'i'}},
                {'phone': {'$regex': q_clean, '$options': 'i'}},
                {'subject': {'$regex': q_clean, '$options': 'i'}},
            ]

        # Calendar date range filter
        date_query = {}
        if date_from:
            try:
                from_str = str(date_from).strip()[:10]
                dt_from = datetime.strptime(from_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
                date_query['$gte'] = dt_from
            except Exception as d_err:
                logger.warning("Could not parse date_from '%s': %s", date_from, d_err)

        if date_to:
            try:
                to_str = str(date_to).strip()[:10]
                dt_to = datetime.strptime(to_str, "%Y-%m-%d").replace(
                    hour=23, minute=59, second=59, microsecond=999999, tzinfo=timezone.utc
                )
                date_query['$lte'] = dt_to
            except Exception as d_err:
                logger.warning("Could not parse date_to '%s': %s", date_to, d_err)

        if date_query:
            filter_criteria['created_at'] = date_query

        total_matching = db.enquiries.count_documents(filter_criteria)
        cursor = db.enquiries.find(filter_criteria).sort('created_at', -1).skip(skip).limit(limit)
        results = []
        for doc in cursor:
            doc['id'] = str(doc.get('_id'))
            results.append(doc)
        return results, total_matching
    except Exception as e:
        logger.error("Error querying enquiries from MongoDB: %s", e)
        return [], 0


def delete_enquiries_by_filter(date_from=None, date_to=None, status_filter=None):
    """
    Bulk delete enquiries matching a date range and optional status filter.
    Returns integer count of deleted documents.
    """
    db = get_mongo_db()
    if db is None:
        return 0

    query = {}
    date_query = {}

    if date_from:
        try:
            from_str = str(date_from).strip()[:10]
            dt_from = datetime.strptime(from_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            date_query['$gte'] = dt_from
        except Exception:
            pass

    if date_to:
        try:
            to_str = str(date_to).strip()[:10]
            dt_to = datetime.strptime(to_str, "%Y-%m-%d").replace(
                hour=23, minute=59, second=59, microsecond=999999, tzinfo=timezone.utc
            )
            date_query['$lte'] = dt_to
        except Exception:
            pass

    if date_query:
        query['created_at'] = date_query

    if status_filter and status_filter.strip().lower() not in ('all', ''):
        s_clean = status_filter.strip().lower()
        if s_clean == 'unread':
            query['is_read'] = False
        else:
            query['status'] = s_clean

    if not query:
        # Require at least one date or status criterion to prevent unintentional full wipe
        return 0

    try:
        result = db.enquiries.delete_many(query)
        logger.info("Bulk deleted %d enquiries matching query: %s", result.deleted_count, query)
        return result.deleted_count
    except Exception as e:
        logger.error("Error performing bulk deletion in MongoDB Atlas: %s", e)
        return 0


def get_admin_credentials():
    """Retrieve admin login configuration from MongoDB or environment."""
    import hashlib
    db = get_mongo_db()
    default_user = os.environ.get('ADMIN_USERNAME', 'trinial26@gmail.com').strip()
    default_pass = os.environ.get('ADMIN_PASSWORD', 'Trinialjo@2026').strip()

    if db is not None:
        try:
            doc = db.app_config.find_one({'_id': 'admin_auth'})
            if doc and doc.get('password_hash'):
                return {
                    'username': doc.get('username', default_user),
                    'password_hash': doc.get('password_hash'),
                    'salt': doc.get('salt', 'trinials_auth_salt'),
                }
        except Exception as e:
            logger.warning("Could not read admin_auth from MongoDB Atlas: %s", e)

    salt = 'trinials_auth_salt'
    pwd_hash = hashlib.sha256((default_pass + salt).encode('utf-8')).hexdigest()
    return {
        'username': default_user,
        'password_hash': pwd_hash,
        'salt': salt,
    }


def seed_admin_credentials_to_mongo(username=None, password=None):
    """
    Persist administrator login credentials directly in MongoDB Atlas collection 'app_config'.
    """
    import hashlib
    db = get_mongo_db()
    if db is None:
        return False

    uname = (username or os.environ.get('ADMIN_USERNAME') or 'trinial26@gmail.com').strip().lower()
    pwd = (password or os.environ.get('ADMIN_PASSWORD') or 'Trinialjo@2026').strip()
    salt = 'trinials_auth_salt'
    pwd_hash = hashlib.sha256((pwd + salt).encode('utf-8')).hexdigest()

    auth_doc = {
        '_id': 'admin_auth',
        'username': uname,
        'password_hash': pwd_hash,
        'salt': salt,
        'updated_at': datetime.now(timezone.utc)
    }

    try:
        db.app_config.replace_one({'_id': 'admin_auth'}, auth_doc, upsert=True)
        logger.info("Successfully updated admin_auth in MongoDB Atlas for user '%s'", uname)
        return True
    except Exception as e:
        logger.error("Failed to update admin_auth in MongoDB Atlas: %s", e)
        return False


def verify_admin_credentials(username, password):
    """
    Verify submitted credentials against stored admin credentials.
    Strictly permits only trinial26@gmail.com as the administrator login identity.
    """
    import hashlib
    if not username or not password:
        return False

    # Strictly permit ONLY trinial26@gmail.com
    submitted_user = str(username).strip().lower()
    if submitted_user != 'trinial26@gmail.com':
        return False

    creds = get_admin_credentials()
    salt = creds.get('salt', 'trinials_auth_salt')
    submitted_hash = hashlib.sha256((password.strip() + salt).encode('utf-8')).hexdigest()

    # Match against stored hash or fallback password
    env_pass = os.environ.get('ADMIN_PASSWORD', 'Trinialjo@2026').strip()
    env_hash = hashlib.sha256((env_pass + salt).encode('utf-8')).hexdigest()

    return submitted_hash == creds.get('password_hash') or submitted_hash == env_hash

