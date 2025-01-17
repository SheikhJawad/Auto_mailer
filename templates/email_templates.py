from database.db import EmailDatabase
from config.settings import DB_PATH

EMAIL_TEMPLATES = [
    {
        "subject": "Deutics Global: Your AI Partner for Tomorrow",
        "body": """
        <html>
        <body>
            <p>Dear {company_name} team,</p>
            <p>At Deutics Global, we specialize in delivering cutting-edge AI solutions that redefine business operations. From real-time data analysis to predictive modeling, we help companies like yours unlock new opportunities.</p>
            <p>Would you be interested in a discussion to explore how we can help {company_name} achieve its goals?</p>
            <p>Best regards,<br>Your Name</p>
        </body>
        </html>
        """
    },
    {
        "subject": "Transformative AI Surveillance Solutions for Buisness intelligence",
        "body": """
        <html>
        <body>
            <p>Hello {company_name} team,</p>
            <p>Deutics Global provides advanced AI-powered surveillance solutions that ensure safety, efficiency, and peace of mind. Our technologies are trusted by top organizations globally.</p>
            <p>We’d love to discuss how {company_name} can leverage our solutions to enhance its security infrastructure.</p>
            <p>Best regards,<br>Your Name</p>
        </body>
        </html>
        """
    },
    {
        "subject": "Deutics Global: AI-Powered Innovations for DIgital Era",
        "body": """
        <html>
        <body>
            <p>Dear {company_name} team,</p>
            <p>We at Deutics Global specialize in delivering AI innovations tailored to businesses like yours. From automated workflows to intelligent systems, we empower companies to stay ahead of the curve.</p>
            <p>Let’s connect and explore how we can drive innovation together at {company_name}.</p>
            <p>Best regards,<br>Your Name</p>
        </body>
        </html>
        """
    },
    {
        "subject": "Boost Efficiency with AI at Deutics Global",
        "body": """
        <html>
        <body>
            <p>Hello {company_name} team,</p>
            <p>Did you know that Deutics Global’s AI services can improve efficiency by up to 50%? Our expertise in AI-driven automation and analytics delivers unparalleled value.</p>
            <p>Are you ready to revolutionize {company_name}’s operations?</p>
            <p>Best regards,<br>Your Name</p>
        </body>
        </html>
        """
    },
    {
        "subject": "Exclusive AI Solutions for every business by Deutics Global",
        "body": """
        <html>
        <body>
            <p>Hello {company_name} team,</p>
            <p>As a leader in AI innovation, Deutics Global offers bespoke AI solutions tailored to industry leaders like {company_name}. From AI-powered customer insights to advanced automation, we deliver measurable results.</p>
            <p>Let’s explore how our exclusive offerings can elevate {company_name}.</p>
            <p>Best regards,<br>Your Name</p>
        </body>
        </html>
        """
    },
    {
        "subject": "Revolutionize your consumers growth with AI Surveillance",
        "body": """
        <html>
        <body>
            <p>Dear {company_name} team,</p>
            <p>Our AI surveillance systems are designed to provide unparalleled security and efficiency. Deutics Global ensures precision, adaptability, and cost-effectiveness in every solution we deliver.</p>
            <p>Let’s discuss how {company_name} can benefit from state-of-the-art surveillance technologies.</p>
            <p>Best regards,<br>Your Name</p>
        </body>
        </html>
        """
    },
    {
        "subject": "AI-Driven Growth Opportunities at Deutics",
        "body": """
        <html>
        <body>
            <p>Dear {company_name} team,</p>
            <p>Deutics Global empowers businesses like yours to unlock growth with AI-powered insights and analytics. Our solutions drive informed decision-making and strategic advantages.</p>
            <p>Can we schedule a time to discuss the growth opportunities we can bring to {company_name}?</p>
            <p>Best regards,<br>Your Name</p>
        </body>
        </html>
        """
    },
    {
        "subject": "Deutics Global: Partnering with you for AI Success",
        "body": """
        <html>
        <body>
            <p>Hello {company_name} team,</p>
            <p>Deutics Global has helped businesses across industries achieve breakthroughs with our AI expertise. From smart decision systems to AI-powered risk management, we enable success.</p>
            <p>We’d love to show you how we can bring the same success to {company_name}.</p>
            <p>Best regards,<br>Your Name</p>
        </body>
        </html>
        """
    }
]


def populate_templates():
    db = EmailDatabase(DB_PATH)
    for template in EMAIL_TEMPLATES:
        db.add_template(template["subject"], template["body"])