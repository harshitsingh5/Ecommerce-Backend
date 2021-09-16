from enum import Enum

class AddressType(Enum):
	USERADDRESS = 0
	FACILITY = 1

class BookingTypes(Enum):
	PICKUP = 0
	RETURN = 1
	PICKUP_AND_RETURN = 2

class RequestType(Enum):
	PICKUP = 0
	RETURN = 1

class ItemStatusType(Enum):
	CREATED=0
	STORED=1
	REQUESTED=2
	RETURNED=3

class DocumentType(Enum):
	AGREEMENT=0
	PICKUP_FORM=1
	RETURN_FORM=2

class PhotoType(Enum):
	DOCUMENT=0
	USER=1

class TokenType(Enum):
	MAIL_VERIFICATION=0
	RESET_PASSWORD=1

class UserType(Enum):
	CUSTOMER=0
	ADMIN=1
