#User Models
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Don't consider this class

genderChoice=(
   ("Male","male"),
   ("Female","female")
)
stateChoice = (
    ("Andhra Pradesh", "Andhra Pradesh"),
    ("Arunachal Pradesh", "Arunachal Pradesh"),
    ("Assam", "Assam"),
    ("Bihar", "Bihar"),
    ("Chhattisgarh", "Chhattisgarh"),
    ("Goa", "Goa"),
    ("Gujarat", "Gujarat"),
    ("Haryana", "Haryana"),
    ("Himachal Pradesh", "Himachal Pradesh"),
    ("Jharkhand", "Jharkhand"),
    ("Karnataka", "Karnataka"),
    ("Kerala", "Kerala"),
    ("Madhya Pradesh", "Madhya Pradesh"),
    ("Maharashtra", "Maharashtra"),
    ("Manipur", "Manipur"),
    ("Meghalaya", "Meghalaya"),
    ("Mizoram", "Mizoram"),
    ("Nagaland", "Nagaland"),
    ("Odisha", "Odisha"),
    ("Punjab", "Punjab"),
    ("Rajasthan", "Rajasthan"),
    ("Sikkim", "Sikkim"),
    ("Tamil Nadu", "Tamil Nadu"),
    ("Telangana", "Telangana"),
    ("Tripura", "Tripura"),
    ("Uttar Pradesh", "Uttar Pradesh"),
    ("Uttarakhand", "Uttarakhand"),
    ("West Bengal", "West Bengal"),
)
cityChoice = (
    ("Mumbai", "Mumbai"),
    ("Delhi", "Delhi"),
    ("Bangalore", "Bangalore"),
    ("Hyderabad", "Hyderabad"),
    ("Ahmedabad", "Ahmedabad"),
    ("Chennai", "Chennai"),
    ("Kolkata", "Kolkata"),
    ("Pune", "Pune"),
    ("Surat", "Surat"),
    ("Jaipur", "Jaipur"),
    ("Lucknow", "Lucknow"),
    ("Kanpur", "Kanpur"),
    ("Nagpur", "Nagpur"),
    ("Visakhapatnam", "Visakhapatnam"),
    ("Bhopal", "Bhopal"),
    ("Patna", "Patna"),
    ("Ludhiana", "Ludhiana"),
    ("Agra", "Agra"),
    ("Nashik", "Nashik"),
    ("Vadodara", "Vadodara"),
    ("Varanasi", "Varanasi"),
    ("Srinagar", "Srinagar"),
    ("Aurangabad", "Aurangabad"),
    ("Dhanbad", "Dhanbad"),
    ("Amritsar", "Amritsar"),
    ("Navi Mumbai", "Navi Mumbai"),
    ("Allahabad", "Allahabad"),
    ("Ranchi", "Ranchi"),
    ("Haora", "Haora"),
    ("Coimbatore", "Coimbatore"),
    ("Jabalpur", "Jabalpur"),
    ("Gwalior", "Gwalior"),
    ("Vijayawada", "Vijayawada"),
    ("Jodhpur", "Jodhpur"),
    ("Madurai", "Madurai"),
    ("Raipur", "Raipur"),
    ("Kota", "Kota"),
    ("Guwahati", "Guwahati"),
    ("Chandigarh", "Chandigarh"),
    ("Solapur", "Solapur"),
    ("Hubli and Dharwad", "Hubli and Dharwad"),
    ("Bareilly", "Bareilly"),
    ("Moradabad", "Moradabad"),
    ("Mysore", "Mysore"),
    ("Gurgaon", "Gurgaon"),
    ("Aligarh", "Aligarh"),
    ("Jalandhar", "Jalandhar"),
    ("Tiruchirappalli", "Tiruchirappalli"),
    ("Bhubaneswar", "Bhubaneswar"),
    ("Salem", "Salem"),
    ("Mira and Bhayander", "Mira and Bhayander"),
    ("Thiruvananthapuram", "Thiruvananthapuram"),
    ("Bhiwandi", "Bhiwandi"),
    ("Saharanpur", "Saharanpur"),
    ("Gorakhpur", "Gorakhpur"),
    ("Guntur", "Guntur"),
    ("Bikaner", "Bikaner"),
    ("Amravati", "Amravati"),
    ("Noida", "Noida"),
    ("Jamshedpur", "Jamshedpur"),
    ("Bhilai Nagar", "Bhilai Nagar"),
    ("Warangal", "Warangal"),
    ("Cuttack", "Cuttack"),
    ("Firozabad", "Firozabad"),
    ("Kochi", "Kochi"),
    ("Bhavnagar", "Bhavnagar"),
    ("Dehradun","Dehradun"),
)
roleChoice = (
    ("Software Engineer", "Software Engineer"),
    ("Product Manager", "Product Manager"),
    ("Data Analyst", "Data Analyst"),
    ("Data Scientist", "Data Scientist"),
    ("User Experience (UX) Designer", "User Experience (UX) Designer"),
    ("User Interface (UI) Designer", "User Interface (UI) Designer"),
    ("Technical Program Manager", "Technical Program Manager"),
    ("Technical Writer", "Technical Writer"),
    ("DevOps Engineer", "DevOps Engineer"),
    ("Network Engineer", "Network Engineer"),
    ("Security Engineer", "Security Engineer"),
    ("Cloud Solutions Architect", "Cloud Solutions Architect"),
    ("Machine Learning Engineer", "Machine Learning Engineer"),
    ("Artificial Intelligence (AI) Engineer", "Artificial Intelligence (AI) Engineer"),
    ("Full Stack Developer", "Full Stack Developer"),
    ("Front-End Developer", "Front-End Developer"),
    ("Back-End Developer", "Back-End Developer"),
    ("Mobile Application Developer", "Mobile Application Developer"),
    ("Quality Assurance (QA) Engineer", "Quality Assurance (QA) Engineer"),
    ("Game Developer", "Game Developer"),
    ("Graphics Designer", "Graphics Designer"),
    ("Technical Support Engineer", "Technical Support Engineer"),
    ("Sales Manager", "Sales Manager"),
    ("Marketing Manager", "Marketing Manager"),
    ("Content Strategist", "Content Strategist"),
    ("Business Analyst", "Business Analyst"),
    ("Human Resources (HR) Manager", "Human Resources (HR) Manager"),
    ("Financial Analyst", "Financial Analyst"),
    ("Project Manager", "Project Manager"),
    ("Supply Chain Manager", "Supply Chain Manager"),
    ("Operations Manager", "Operations Manager"),
    ("Executive Assistant", "Executive Assistant"),
    ("Customer Success Manager", "Customer Success Manager"),
    ("Solutions Engineer", "Solutions Engineer"),
    ("System Administrator", "System Administrator"),
    ("Database Administrator", "Database Administrator"),
    ("Network Administrator", "Network Administrator"),
    ("Web Designer", "Web Designer"),
    ("Web Developer", "Web Developer"),
    ("Information Security Analyst", "Information Security Analyst"),
    ("Data Architect", "Data Architect"),
    ("Solutions Architect", "Solutions Architect"),
    ("Cloud Engineer", "Cloud Engineer"),
    ("Video Producer", "Video Producer"),
    ("Technical Recruiter", "Technical Recruiter"),
    ("Creative Director", "Creative Director"),
    ("Product Marketing Manager", "Product Marketing Manager"),
    ("Email Marketing Manager", "Email Marketing Manager"),
    ("Social Media Manager", "Social Media Manager"),
    ("Business Development Manager", "Business Development Manager"),
    ("Account Manager", "Account Manager"),
    ("Public Relations (PR) Manager", "Public Relations (PR) Manager"),
    ("Event Planner", "Event Planner"),
    ("Brand Manager", "Brand Manager"),
    ("Community Manager", "Community Manager"),
    ("Training Manager", "Training Manager"),
    ("Corporate Trainer", "Corporate Trainer"),
    ("Talent Acquisition Manager", "Talent Acquisition Manager"),
    ("Legal Counsel", "Legal Counsel"),
    ("Intellectual Property (IP) Attorney", "Intellectual Property (IP) Attorney"),
    ("Patent Attorney", "Patent Attorney"),
    ("Environmental Health and Safety (EHS) Manager", "Environmental Health and Safety (EHS) Manager"),
    ("Sustainability Manager", "Sustainability Manager"),
    ("Facilities Manager", "Facilities Manager"),
    ("Information Technology (IT) Manager", "Information Technology (IT) Manager"),
    ("IT Project Manager", "IT Project Manager"),
    ("IT Business Analyst", "IT Business Analyst"),
    ("IT Security Analyst","IT Security Analyst"),
    ("IT Auditor","IT Auditor"),
    ("IT Consultant","IT Consultant"),
)
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_developer = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    birthDate = models.DateField(null=True,blank=True)
    address = models.CharField(max_length=100,null=True,blank=True)
    state = models.CharField(choices=stateChoice,max_length=100,null=True,blank=True)
    landmark = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(choices=cityChoice,max_length=100,null=True,blank=True)
    salary = models.IntegerField(null=True,blank=True)
    gender = models.CharField(choices=genderChoice,max_length=50)
    email = models.EmailField(unique=True,null = False)
    username = models.CharField(max_length=100,unique=True,null=False)
    profile_pic = models.ImageField(upload_to='images/',null=True,blank=True)
    jobRole = models.CharField(choices=roleChoice,max_length=50,null=True,blank=True)
    skills = models.CharField(max_length=500,blank=True,null=True)
    contact_number = PhoneNumberField(null=True, blank=True, unique=True)
    alternate_contact_number = PhoneNumberField(null=True, blank=True, unique=True)
    alternate_email = models.EmailField(blank=True,null=True)
    bio = models.TextField(max_length=200,null=True,blank=True)
    website_url = models.URLField(max_length=200,null=True,blank=True)
    linkedin_url = models.URLField(max_length=200,null=True,blank=True)
    twitter_url = models.URLField(max_length=200,null=True,blank=True)
    instagram_url = models.URLField(max_length=200,null=True,blank=True)
    facebook_url = models.URLField(max_length=200,null=True,blank=True)
    youtube_url = models.URLField(max_length=200,null=True,blank=True)
    github_url = models.URLField(max_length=200,null=True,blank=True)
    other_url = models.URLField(max_length=200,null=True,blank=True)

    def get_my_field_as_list(self):
        return [x.strip() for x in self.skills.split(',')]
    
    class Meta:
        db_table='user'
        #ordering = ('email',)

    def __str__(self):
        return self.username


class Schedule(models.Model):
    schedule_title = models.CharField(max_length=200)
    schedule_description = models.TextField()
    schedule_documents = models.FileField(upload_to='schedule_documents/',null=True,blank=True)
    users = models.ManyToManyField(User, related_name='schedules')
    schedule_meeting_url = models.URLField()
    schedule_created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table='schedule'

    def __str__(self):
        return self.title