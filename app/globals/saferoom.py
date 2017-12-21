# Services
EVERNOTE_SERVICE = 0
ONENOTE_SERVICE = 1
DROPBOX_SERVICE = 2
SUPPORTED_SERVICES = {"evernote":EVERNOTE_SERVICE,"onenote":ONENOTE_SERVICE}

# Token validity
ONENOTE_TOKEN_VALID = 60.0

# Supported protection methods
METHOD_PASSWORD = "password"
METHOD_CMS = "cms"
PROTECTION_METHODS = [METHOD_PASSWORD,METHOD_CMS]

# Prefixes/Suffixes
PREFIX_ENCRYPTED = "TUFNTU9USEVOQ1JZUFRFRE5PVEU=__"
PREFIX_ONENOTE_PAGE = "<html><head><title>%s</title><link type=\"text/css\" rel=\"stylesheet\" href=\"/static/css/bootstrap.min.css\"/></head><body style='font-size:12px'>%s</body></html>"
PREFIX_EVERNOTE_NOTE = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><!DOCTYPE en-note SYSTEM \"http://xml.evernote.com/pub/enml2.dtd\"><en-note>%s</en-note>" 
PREFIX_MIME = "MIME-Version: 1.0\nContent-Disposition: attachment; filename=\"smime.p7m\"\nContent-Type:application/x-pkcs7-mime; smime-type=enveloped-data; name=\"smime.p7m\nContent-Transfer-Encoding: base64\n\n"
SUFFIX_ENCRYPTED = "__TUFNTU9USEVOQ1JZUFRFRE5PVEU="

# Styles
APP_STYLES = "<style>.attachment{width:90%;padding:10px 10px 10px 10px;margin-bottom:10px;border:1px solid #dddddd;border-radius: 10px 10px 10px 10px;}</style><link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css\" integrity=\"sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u\" crossorigin=\"anonymous\"></link>";

# Titles
TASK_ENCRYPTNOTEBOOK_TITLE = "Notebook(s) encryption"
TASK_ENCRYPTNOTEBOOK_DSCR = "Procedure used to encrypt all notes from specified notebooks"
TASK_CREATENOTE_TITLE = "Creating [%s] note"
TASK_CREATENOTE_DSCR = "Creating the encrypted note [%s] and uploading it to specified service";
TASK_ENCRYPTNOTES_TITLE = "Encrypting multiple notes"
TASK_ENCRYPTNOTES_DSCR = "Procedure used to encrypt multiple notes with specific GUIDs. Already encrypted notes are skipped. During the encryption procedure app creates a backup copy of original note, so it can be restored later"
TASK_BATCHCREATE_TITLE = "Batch Encryption"
TASK_BATCHCREATE_DSCR = "Procedure the encrypt multiple files and upload them into specified service"

# MIME types
MIME_PDF = "application/pdf"
MIME_DOC = "application/msword"
MIME_DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
MIME_XLS = "application/vnd.ms-excel"
MIME_XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
MIME_PPT = "application/vnd.ms-powerpoint"
MIME_PPTX = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
MIME_JPEG = "image/jpeg"
MIME_GIF = "image/gif"
MIME_PNG = "image/png"
MIME_DEFAULT = "text/*"
MIME_MP3 = "audio/mp3"
MIME_MP4 = "video/mp4"

MIME_TYPES = {"pdf":MIME_PDF,"docx":MIME_DOCX,"doc":MIME_DOC,"xls":MIME_XLSX,"xlsx":MIME_XLSX,"ppt":MIME_PPT,"pptx":MIME_PPTX,"jpeg":MIME_JPEG,"jpg":MIME_JPEG,"gif":MIME_GIF,"png":MIME_PNG,"mp3":MIME_MP3,"mp4":MIME_MP4}

# Media tags
MEDIA_EVERNOTE = "<en-media type='%s' hash='%s'  />"
MEDIA_ONENOTE_IMAGE = "<img src=\"name:%s\"/>"
MEDIA_ONENOTE_OBJECT = "<object data-attachment=\"%s\" data=\"name:%s\" type=\"%s\"/>"
MEDIA_IMAGE_TEMPLATE = "<img src='name:%s' data-filename='%s'/>"

# Display modes
ENCRYPTED_ONLY = "1"
UNENCRYPTED_ONLY = "2"

#### System message
ERROR_MESSAGES = {
    "NO_ACCOUNT":"Account ID is mandatory",
    "NO_ACCOUNT_NAME": "Account name is mandatory",
    "NO_SERVICE": "Service is mandatory",
    "NOT_SUPPORTED_SERVICE": "Service is not supported",
    "NO_USER_NAME":"User's name is mandatory",
    "NO_EMAIL": "Email is mandatory",
    "NO_PASSWORD":"Password is mandatory",
    "NO_SUBJECT":"Subject DN is mandatory",
    "NO_GROUP_NAME":"Group's name is mandatory",
    "NO_GUID": "GUID is mandatory",
    "NO_METHOD":"Protection method is mandatory",
    "NOT_SUPPORTED_METHOD": "Protection method is not supported",
    "NO_RECIPIENTS": "List of recipients is empty",
    "NO_TITLE": "Title is mandatory",
    "NO_NOTE_CONTENT": "Note content is mandatory",
    "NO_PRIVATE_KEY": "Private key password is mandatory",
    "NO_NOTES": "List of notes is empty",
    "NO_FILES": "File(s) not found",
    "NO_RECIPIENT":"Recipient is not specified"
}

