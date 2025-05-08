import random
import string
import uuid
from datetime import datetime, timedelta
from faker import Faker

# Initialize faker with multiple locales
fake = Faker(['en_US'])

class DataGenerator:
    """
    Utility class for generating random test data
    """
    
    @staticmethod
    def random_email(domain=None):
        """Generate a random email address"""
        if domain is None:
            return fake.email()
        username = fake.user_name()
        return f"{username}@{domain}"
    
    @staticmethod
    def random_password(length=12, include_special=True):
        """Generate a random password with specified complexity"""
        char_sets = [
            string.ascii_lowercase,
            string.ascii_uppercase,
            string.digits
        ]
        
        if include_special:
            char_sets.append("!@#$%^&*()_+-=[]{}|;:,.<>?")
        
        # Ensure at least one character from each set
        password = [random.choice(char_set) for char_set in char_sets]
        
        # Fill to desired length
        for _ in range(length - len(char_sets)):
            char_set = random.choice(char_sets)
            password.append(random.choice(char_set))
        
        # Shuffle password characters
        random.shuffle(password)
        return ''.join(password)
    
    @staticmethod
    def random_name():
        """Generate a random full name"""
        return fake.name()
    
    @staticmethod
    def random_first_name():
        """Generate a random first name"""
        return fake.first_name()
    
    @staticmethod
    def random_last_name():
        """Generate a random last name"""
        return fake.last_name()
    
    @staticmethod
    def random_phone_number():
        """Generate a random phone number"""
        return fake.phone_number()
    
    @staticmethod
    def random_address():
        """Generate a random address"""
        return {
            "street": fake.street_address(),
            "city": fake.city(),
            "state": fake.state(),
            "zip": fake.zipcode(),
            "country": fake.country()
        }
    
    @staticmethod
    def random_credit_card():
        """Generate random credit card details"""
        return {
            "number": fake.credit_card_number(),
            "expiry_date": fake.credit_card_expire(),
            "security_code": fake.credit_card_security_code(),
            "holder": fake.name()
        }
    
    @staticmethod
    def random_date(start_date=None, end_date=None):
        """Generate a random date between start_date and end_date"""
        if start_date is None:
            start_date = datetime.now() - timedelta(days=365)
        if end_date is None:
            end_date = datetime.now()
        return fake.date_between(start_date=start_date, end_date=end_date)
    
    @staticmethod
    def random_future_date(min_days=1, max_days=365):
        """Generate a random date in the future"""
        start_date = datetime.now() + timedelta(days=min_days)
        end_date = datetime.now() + timedelta(days=max_days)
        return fake.date_between(start_date=start_date, end_date=end_date)
    
    @staticmethod
    def random_past_date(min_days=1, max_days=365):
        """Generate a random date in the past"""
        start_date = datetime.now() - timedelta(days=max_days)
        end_date = datetime.now() - timedelta(days=min_days)
        return fake.date_between(start_date=start_date, end_date=end_date)
    
    @staticmethod
    def random_sentence():
        """Generate a random sentence"""
        return fake.sentence()
    
    @staticmethod
    def random_paragraph():
        """Generate a random paragraph"""
        return fake.paragraph()
    
    @staticmethod
    def random_url():
        """Generate a random URL"""
        return fake.url()
    
    @staticmethod
    def random_image_url(width=None, height=None):
        """Generate a random image URL with optional dimensions"""
        if width is None:
            width = random.randint(200, 800)
        if height is None:
            height = random.randint(200, 800)
        return f"https://picsum.photos/{width}/{height}"
    
    @staticmethod
    def random_uuid():
        """Generate a random UUID"""
        return str(uuid.uuid4())
    
    @staticmethod
    def random_hex_color():
        """Generate a random hex color code"""
        return fake.hex_color()
    
    @staticmethod
    def random_company():
        """Generate a random company name"""
        return fake.company()
    
    @staticmethod
    def random_job_title():
        """Generate a random job title"""
        return fake.job()
    
    @staticmethod
    def random_ip_address():
        """Generate a random IP address"""
        return fake.ipv4()
    
    @staticmethod
    def random_user_agent():
        """Generate a random user agent string"""
        return fake.user_agent()
    
    @staticmethod
    def random_element(elements):
        """Select a random element from a list"""
        return random.choice(elements)
    
    @staticmethod
    def random_sample(elements, count=1):
        """Select a random sample of elements from a list"""
        return random.sample(elements, min(count, len(elements))) 